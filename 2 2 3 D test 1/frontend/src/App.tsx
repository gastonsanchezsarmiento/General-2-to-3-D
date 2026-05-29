import { startTransition, useEffect, useMemo, useState } from 'react'
import type { FormEvent, ReactNode } from 'react'
import './App.css'
import type {
  CandidateObject,
  Observation,
  PageRecord,
  PlaybookSummary,
  ProjectDetail,
  ProjectRecord,
  RunSnapshot,
  Stage5BCard,
} from './types'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

type WorkspaceMode = 'review' | 'developer'
type ReviewActionType = 'approve' | 'reject' | 'request_reread' | 'note' | 'discard_card' | 'discard_sheet'
type SpecificityLevel = 'board' | 'candidate' | 'relationship' | 'conflict' | 'unresolved' | 'observation' | 'support'
type TaskTrackerStatus = 'pending' | 'running' | 'completed'

interface CollapsiblePanelProps {
  title: string
  summary?: ReactNode
  defaultOpen?: boolean
  actions?: ReactNode
  className?: string
  contentClassName?: string
  children: ReactNode
}

interface ReviewActionOptions {
  targetIds?: string[]
  decisionScope?: string
  note?: string
  extensions?: Record<string, unknown>
}

interface ExplorerOption {
  id: string
  label: string
}

const STAGE_SEQUENCE = ['stage0', 'stage1', 'stage2', 'stage3', 'stage4', 'stage5a', 'stage5b'] as const

interface LiveProgressState {
  currentStage: string
  currentStageStatus: string
  latestMessage: string
  latestUpdatedAt: string | null
  completedStages: number
  totalStages: number
  pipelinePercent: number
  totalTasks: number
  completedTasks: number
  stage3Percent: number
  activeTaskId: string | null
  activeTaskType: string | null
  taskStatusById: Record<string, TaskTrackerStatus>
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed with status ${response.status}`)
  }

  return response.json() as Promise<T>
}

function formatDate(value?: string | null) {
  if (!value) {
    return 'Unknown'
  }

  const parsed = new Date(value)
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString()
}

function artifactUrl(path?: string | null) {
  return path ? `${API_BASE}/artifacts/${path}` : ''
}

function stageLabel(value?: string | null) {
  return (value ?? 'orchestrator').replace('stage', 'Stage ').replace('a', 'A').replace('b', 'B')
}

function deriveStageStatus(snapshot?: RunSnapshot | null) {
  const result = new Map<string, string>()
  for (const event of snapshot?.stage_events ?? []) {
    result.set(event.stage, event.status)
  }
  return result
}

function payloadNumber(payload: Record<string, unknown> | undefined, key: string) {
  const value = payload?.[key]
  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function payloadString(payload: Record<string, unknown> | undefined, key: string) {
  const value = payload?.[key]
  return typeof value === 'string' && value.trim() ? value : null
}

function deriveLiveProgress(snapshot?: RunSnapshot | null): LiveProgressState | null {
  if (!snapshot) {
    return null
  }

  const stageStatus = deriveStageStatus(snapshot)
  const currentStage = snapshot.run.current_stage ?? 'orchestrator'
  const currentStageStatus = snapshot.run.current_stage_status ?? stageStatus.get(currentStage) ?? snapshot.run.status
  const latestEvent = snapshot.stage_events.at(-1) ?? null
  const latestStage3Event = [...snapshot.stage_events].reverse().find((event) => event.stage === 'stage3') ?? null
  const completedTaskIds = new Set(snapshot.stage3.map((task) => task.task_id))
  const totalTasks = payloadNumber(latestStage3Event?.payload, 'total_tasks') ?? snapshot.stage2?.tasks.length ?? snapshot.stage3.length
  const completedTasks = Math.max(
    completedTaskIds.size,
    Math.min(payloadNumber(latestStage3Event?.payload, 'completed_tasks') ?? completedTaskIds.size, totalTasks),
  )
  const activeTaskIdCandidate = payloadString(latestStage3Event?.payload, 'task_id')
  const activeTaskId =
    currentStage === 'stage3' && currentStageStatus === 'running' && activeTaskIdCandidate && !completedTaskIds.has(activeTaskIdCandidate)
      ? activeTaskIdCandidate
      : null
  const activeTaskType = activeTaskId ? payloadString(latestStage3Event?.payload, 'task_type') : null
  const taskStatusById = Object.fromEntries(
    (snapshot.stage2?.tasks ?? []).map((task) => [
      task.task_id,
      completedTaskIds.has(task.task_id) ? 'completed' : activeTaskId === task.task_id ? 'running' : 'pending',
    ]),
  ) as Record<string, TaskTrackerStatus>

  const stage3Fraction = totalTasks > 0 ? (stageStatus.get('stage3') === 'completed' ? 1 : completedTasks / totalTasks) : 0
  const completedStages = STAGE_SEQUENCE.filter((stage) => stageStatus.get(stage) === 'completed').length
  const pipelineUnits = completedStages + (currentStage === 'stage3' && stageStatus.get('stage3') !== 'completed' ? stage3Fraction : 0)

  return {
    currentStage,
    currentStageStatus,
    latestMessage: latestStage3Event?.message ?? latestEvent?.message ?? 'Waiting for live updates.',
    latestUpdatedAt: latestStage3Event?.created_at ?? latestEvent?.created_at ?? snapshot.run.updated_at ?? null,
    completedStages,
    totalStages: STAGE_SEQUENCE.length,
    pipelinePercent: Math.round((Math.min(pipelineUnits, STAGE_SEQUENCE.length) / STAGE_SEQUENCE.length) * 100),
    totalTasks,
    completedTasks,
    stage3Percent: totalTasks > 0 ? Math.round(stage3Fraction * 100) : 0,
    activeTaskId,
    activeTaskType,
    taskStatusById,
  }
}

function parsePlaybookSummaries(value: unknown): PlaybookSummary[] {
  if (!Array.isArray(value)) {
    return []
  }

  return value.flatMap((item): PlaybookSummary[] => {
    if (!item || typeof item !== 'object') {
      return []
    }
    const candidate = item as Record<string, unknown>
    if (typeof candidate.key !== 'string' || typeof candidate.label !== 'string' || typeof candidate.description !== 'string') {
      return []
    }
    return [
      {
        key: candidate.key,
        label: candidate.label,
        description: candidate.description,
        default: Boolean(candidate.default),
      },
    ]
  })
}

function humanizeToken(value?: string | null) {
  return (value ?? 'unknown').replaceAll('_', ' ')
}

function truncateText(value: string, maxLength = 88) {
  return value.length <= maxLength ? value : `${value.slice(0, maxLength - 1)}…`
}

function toStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return []
  }
  return value.flatMap((item) => (typeof item === 'string' && item.trim() ? [item] : []))
}

function candidateLabel(candidate: CandidateObject) {
  return candidate.display_label || humanizeToken(candidate.object_family)
}

function observationLabel(observation: Observation) {
  return truncateText(observation.summary || humanizeToken(observation.observation_type))
}

function App() {
  const [projects, setProjects] = useState<ProjectRecord[]>([])
  const [projectDetail, setProjectDetail] = useState<ProjectDetail | null>(null)
  const [selectedProjectId, setSelectedProjectId] = useState<string>('')
  const [selectedRunId, setSelectedRunId] = useState<string>('')
  const [runSnapshot, setRunSnapshot] = useState<RunSnapshot | null>(null)
  const [workspaceMode, setWorkspaceMode] = useState<WorkspaceMode>('review')
  const [config, setConfig] = useState<Record<string, unknown>>({})
  const [createProjectName, setCreateProjectName] = useState('')
  const [createProjectDescription, setCreateProjectDescription] = useState('')
  const [uploadFiles, setUploadFiles] = useState<FileList | null>(null)
  const [reviewNote, setReviewNote] = useState('')
  const [selectedPageId, setSelectedPageId] = useState('')
  const [selectedCardId, setSelectedCardId] = useState('')
  const [selectedPlaybookOverride, setSelectedPlaybookOverride] = useState('')
  const [connectionState, setConnectionState] = useState<'idle' | 'live' | 'error'>('idle')
  const [busy, setBusy] = useState<string>('')
  const [error, setError] = useState<string>('')

  useEffect(() => {
    void (async () => {
      try {
        const [projectList, backendConfig] = await Promise.all([
          fetchJson<ProjectRecord[]>('/api/projects'),
          fetchJson<Record<string, unknown>>('/api/config'),
        ])
        setProjects(projectList)
        setConfig(backendConfig)
        if (projectList[0]) {
          startTransition(() => {
            setSelectedProjectId(projectList[0].project_id)
          })
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load application state')
      }
    })()
  }, [])

  useEffect(() => {
    if (!selectedProjectId) {
      return
    }

    void (async () => {
      try {
        const detail = await fetchJson<ProjectDetail>(`/api/projects/${selectedProjectId}`)
        setProjectDetail(detail)
        if (!selectedRunId && detail.runs[0]) {
          startTransition(() => {
            setSelectedRunId(detail.runs[0].run_id)
          })
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load project detail')
      }
    })()
  }, [selectedProjectId, selectedRunId])

  useEffect(() => {
    if (!selectedRunId) {
      return
    }

    let closed = false
    void (async () => {
      try {
        const snapshot = await fetchJson<RunSnapshot>(`/api/runs/${selectedRunId}`)
        if (!closed) {
          setRunSnapshot(snapshot)
        }
      } catch (err) {
        if (!closed) {
          setError(err instanceof Error ? err.message : 'Failed to load run snapshot')
        }
      }
    })()

    const source = new EventSource(`${API_BASE}/api/runs/${selectedRunId}/stream`)
    source.onopen = () => setConnectionState('live')
    source.onmessage = (event) => {
      const payload = JSON.parse(event.data) as RunSnapshot
      setRunSnapshot(payload)
    }
    source.onerror = () => {
      setConnectionState('error')
      source.close()
    }

    return () => {
      closed = true
      source.close()
      setConnectionState('idle')
    }
  }, [selectedRunId])

  useEffect(() => {
    if (runSnapshot?.pages?.[0] && !selectedPageId) {
      setSelectedPageId(runSnapshot.pages[0].page_id)
    }
    if (runSnapshot?.stage5b?.cards?.[0] && !selectedCardId) {
      setSelectedCardId(runSnapshot.stage5b.cards[0].card_id)
    }
  }, [runSnapshot, selectedCardId, selectedPageId])

  const stageStatus = useMemo(() => deriveStageStatus(runSnapshot), [runSnapshot])
  const liveProgress = useMemo(() => deriveLiveProgress(runSnapshot), [runSnapshot])
  const selectedPage = useMemo(
    () => runSnapshot?.pages.find((page) => page.page_id === selectedPageId) ?? runSnapshot?.pages[0] ?? null,
    [runSnapshot, selectedPageId],
  )
  const selectedCard = useMemo(
    () => runSnapshot?.stage5b?.cards.find((card) => card.card_id === selectedCardId) ?? runSnapshot?.stage5b?.cards[0] ?? null,
    [runSnapshot, selectedCardId],
  )
  const availablePlaybooks = useMemo(() => parsePlaybookSummaries(config.available_playbooks), [config])
  const selectedPlaybookSummary = useMemo(
    () => availablePlaybooks.find((playbook) => playbook.key === selectedPlaybookOverride) ?? null,
    [availablePlaybooks, selectedPlaybookOverride],
  )

  async function refreshProjects() {
    const projectList = await fetchJson<ProjectRecord[]>('/api/projects')
    setProjects(projectList)
  }

  async function refreshProjectDetail(projectId: string) {
    const detail = await fetchJson<ProjectDetail>(`/api/projects/${projectId}`)
    setProjectDetail(detail)
  }

  async function handleCreateProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!createProjectName.trim()) {
      return
    }

    setBusy('project')
    setError('')
    try {
      const project = await fetchJson<ProjectRecord>('/api/projects', {
        method: 'POST',
        body: JSON.stringify({
          name: createProjectName.trim(),
          description: createProjectDescription.trim() || undefined,
        }),
      })
      setCreateProjectName('')
      setCreateProjectDescription('')
      await refreshProjects()
      setSelectedProjectId(project.project_id)
      setSelectedRunId('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project')
    } finally {
      setBusy('')
    }
  }

  async function handleUploadDocuments(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedProjectId || !uploadFiles?.length) {
      return
    }

    setBusy('upload')
    setError('')
    try {
      const formData = new FormData()
      Array.from(uploadFiles).forEach((file) => formData.append('files', file))
      const response = await fetch(`${API_BASE}/api/projects/${selectedProjectId}/documents`, {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) {
        throw new Error(await response.text())
      }
      setUploadFiles(null)
      await refreshProjectDetail(selectedProjectId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload documents')
    } finally {
      setBusy('')
    }
  }

  async function handleStartRun() {
    if (!selectedProjectId) {
      return
    }
    setBusy('run')
    setError('')
    try {
      const run = await fetchJson<{ run_id: string }>(`/api/projects/${selectedProjectId}/runs`, {
        method: 'POST',
        body: JSON.stringify(selectedPlaybookOverride ? { playbook_override: selectedPlaybookOverride } : {}),
      })
      await refreshProjectDetail(selectedProjectId)
      setSelectedRunId(run.run_id)
      setWorkspaceMode('review')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create run')
    } finally {
      setBusy('')
    }
  }

  async function handleReviewAction(actionType: ReviewActionType, options: ReviewActionOptions = {}) {
    if (!runSnapshot) {
      return
    }

    setBusy(actionType)
    setError('')
    try {
      const selectedPageContext = selectedPage?.page_id ?? selectedCard?.page_id ?? null
      const defaultDecisionScope =
        actionType === 'request_reread' || actionType === 'discard_sheet'
          ? 'region'
          : actionType === 'discard_card'
            ? 'slice'
            : actionType === 'note'
              ? 'object'
              : 'checkpoint'
      const targetIds =
        options.targetIds ??
        (actionType === 'approve' || actionType === 'reject'
          ? [runSnapshot.run.run_id]
          : actionType === 'request_reread'
            ? selectedPageContext
              ? [selectedPageContext]
              : selectedCard?.linked_ids?.length
                ? selectedCard.linked_ids
                : [runSnapshot.run.run_id]
            : selectedCard?.linked_ids?.length
              ? selectedCard.linked_ids
              : selectedPageContext
                ? [selectedPageContext]
                : [runSnapshot.run.run_id])
      await fetchJson(`/api/runs/${runSnapshot.run.run_id}/review-actions`, {
        method: 'POST',
        body: JSON.stringify({
          action_type: actionType,
          decision_scope: options.decisionScope ?? defaultDecisionScope,
          target_ids: targetIds,
          note: (options.note ?? reviewNote).trim() || undefined,
          extensions: {
            selected_page_id: selectedPage?.page_id ?? null,
            selected_card_id: selectedCard?.card_id ?? null,
            card_page_id: selectedCard?.page_id ?? null,
            linked_ids: selectedCard?.linked_ids ?? [],
            ...(options.extensions ?? {}),
          },
        }),
      })
      setReviewNote('')
      const updatedSnapshot = await fetchJson<RunSnapshot>(`/api/runs/${runSnapshot.run.run_id}`)
      setRunSnapshot(updatedSnapshot)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to record review action')
    } finally {
      setBusy('')
    }
  }

  async function handleRelaunchRun() {
    if (!runSnapshot || !selectedProjectId) {
      return
    }

    setBusy('relaunch')
    setError('')
    try {
      const payload: Record<string, unknown> = {
        source_document_ids: runSnapshot.run.source_document_ids,
        feedback_source_run_id: runSnapshot.run.run_id,
        relaunch_scope: 'stage2_to_stage5',
      }
      const playbookOverride = runSnapshot.run.playbook_override ?? runSnapshot.run.selected_playbook ?? undefined
      if (playbookOverride) {
        payload.playbook_override = playbookOverride
      }

      const run = await fetchJson<{ run_id: string }>(`/api/projects/${selectedProjectId}/runs`, {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      await refreshProjectDetail(selectedProjectId)
      setSelectedRunId(run.run_id)
      setWorkspaceMode('review')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to relaunch run')
    } finally {
      setBusy('')
    }
  }

  return (
    <div className="app-shell">
      <header className="masthead">
        <div>
          <p className="eyebrow">Execution Plan / Milestone 1</p>
          <h1>Plan To 3D Review Console</h1>
          <p className="lede">
            One application, two workspaces: milestone review on the left edge of the process and internal pipeline visibility on the right.
          </p>
        </div>
        <div className="status-strip">
          <StatusPill label="Backend" value={String(config.frontend_origin ? 'ready' : 'unknown')} tone="neutral" />
          <StatusPill
            label="Model Mode"
            value={String(config.model_mode ?? 'mock')}
            tone={String(config.model_mode ?? 'mock') === 'mock' ? 'warning' : 'success'}
          />
          <StatusPill
            label="OpenAI Key"
            value={Boolean(config.openai_configured) ? 'configured' : 'set in .env when needed'}
            tone={Boolean(config.openai_configured) ? 'success' : 'neutral'}
          />
          <StatusPill label="Live Stream" value={connectionState} tone={connectionState === 'live' ? 'success' : 'warning'} />
        </div>
      </header>

      {error ? <div className="error-banner">{error}</div> : null}

      <div className="layout-grid">
        <aside className="sidebar">
          <CollapsiblePanel
            title="Projects"
            actions={
              <button type="button" className="ghost-button" onClick={() => void refreshProjects()}>
                Refresh
              </button>
            }
          >
            <form className="stack-form" onSubmit={(event) => void handleCreateProject(event)}>
              <label>
                <span>Name</span>
                <input value={createProjectName} onChange={(event) => setCreateProjectName(event.target.value)} placeholder="Warehouse batch 01" />
              </label>
              <label>
                <span>Description</span>
                <textarea
                  value={createProjectDescription}
                  onChange={(event) => setCreateProjectDescription(event.target.value)}
                  placeholder="Portal-frame structural pack for milestone review"
                />
              </label>
              <button type="submit" className="primary-button" disabled={busy === 'project'}>
                {busy === 'project' ? 'Creating...' : 'Create project'}
              </button>
            </form>
            <div className="project-list">
              {projects.map((project) => (
                <button
                  key={project.project_id}
                  type="button"
                  className={`project-item ${project.project_id === selectedProjectId ? 'is-active' : ''}`}
                  onClick={() => {
                    setSelectedProjectId(project.project_id)
                    setSelectedRunId('')
                    setRunSnapshot(null)
                  }}
                >
                  <strong>{project.name}</strong>
                  <span>{project.description || 'No description yet'}</span>
                </button>
              ))}
            </div>
          </CollapsiblePanel>

          <CollapsiblePanel title="Source Pack" summary={`${projectDetail?.documents.length ?? 0} file(s)`}>
            <form className="stack-form" onSubmit={(event) => void handleUploadDocuments(event)}>
              <label>
                <span>Upload PDFs</span>
                <input multiple type="file" accept="application/pdf" onChange={(event) => setUploadFiles(event.target.files)} />
              </label>
              <button type="submit" className="secondary-button" disabled={!selectedProjectId || busy === 'upload'}>
                {busy === 'upload' ? 'Uploading...' : 'Upload documents'}
              </button>
            </form>
            <div className="document-list">
              {projectDetail?.documents.map((document) => (
                <div key={document.source_document_id} className="document-row">
                  <strong>{document.original_filename}</strong>
                  <span>
                    {document.page_count ?? '?'} page(s) / {(document.file_size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              ))}
            </div>
            <label>
              <span>Reading Playbook</span>
              <select value={selectedPlaybookOverride} onChange={(event) => setSelectedPlaybookOverride(event.target.value)}>
                <option value="">Automatic from Stage 1</option>
                {availablePlaybooks.map((playbook) => (
                  <option key={playbook.key} value={playbook.key}>
                    {playbook.label}
                  </option>
                ))}
              </select>
              <small>
                {selectedPlaybookSummary?.description ?? 'Leave this automatic to let Stage 1 choose the playbook from the pack.'}
              </small>
            </label>
            <button type="button" className="primary-button" disabled={!selectedProjectId || busy === 'run'} onClick={() => void handleStartRun()}>
              {busy === 'run' ? 'Starting run...' : 'Start interpretation run'}
            </button>
          </CollapsiblePanel>

          <section className="panel">
            <div className="panel-heading">
              <h2>Runs</h2>
              <span>{projectDetail?.runs.length ?? 0}</span>
            </div>
            <div className="run-list">
              {projectDetail?.runs.map((run) => (
                <button
                  key={run.run_id}
                  type="button"
                  className={`run-item ${run.run_id === selectedRunId ? 'is-active' : ''}`}
                  onClick={() => setSelectedRunId(run.run_id)}
                >
                  <strong>{run.run_id}</strong>
                  <span>{run.status}</span>
                  <small>{formatDate(run.updated_at)}</small>
                </button>
              ))}
            </div>
          </section>
        </aside>

        <main className="workspace">
          <div className="workspace-toolbar">
            <div>
              <p className="eyebrow">Active Workspace</p>
              <div className="toggle-group">
                <button
                  type="button"
                  className={workspaceMode === 'review' ? 'toggle-button is-active' : 'toggle-button'}
                  onClick={() => setWorkspaceMode('review')}
                >
                  Review Workspace
                </button>
                <button
                  type="button"
                  className={workspaceMode === 'developer' ? 'toggle-button is-active' : 'toggle-button'}
                  onClick={() => setWorkspaceMode('developer')}
                >
                  Developer Workspace
                </button>
              </div>
            </div>
            <div className="run-headline">
              <strong>{runSnapshot?.project.name ?? projectDetail?.project.name ?? 'Select a project'}</strong>
              <span>
                {runSnapshot?.run.run_id ? `${runSnapshot.run.run_id} / ${runSnapshot.run.status}` : 'No run selected'}
              </span>
            </div>
          </div>

          <section className="stage-ribbon panel panel--flush">
            {STAGE_SEQUENCE.map((stage) => (
              <div key={stage} className={`stage-chip stage-chip--${stageStatus.get(stage) ?? 'pending'}`}>
                <span>{stageLabel(stage)}</span>
                <strong>{stageStatus.get(stage) ?? 'pending'}</strong>
              </div>
            ))}
          </section>

          {runSnapshot && liveProgress ? (
            <LiveProgressPanel runSnapshot={runSnapshot} liveProgress={liveProgress} connectionState={connectionState} />
          ) : null}

          {!runSnapshot ? (
            <section className="panel empty-state">
              <h2>Start with a project and a PDF pack</h2>
              <p>
                The backend is ready for uploads, Stage 0 page rendering, Stage 1 reconnaissance, Stage 2 planning, Stage 3 and 4 capture, and the Stage 5A / 5B milestone checkpoint.
              </p>
            </section>
          ) : workspaceMode === 'review' ? (
            <ReviewWorkspace
              runSnapshot={runSnapshot}
              selectedPage={selectedPage}
              selectedPageId={selectedPageId}
              setSelectedPageId={setSelectedPageId}
              selectedCard={selectedCard}
              selectedCardId={selectedCardId}
              setSelectedCardId={setSelectedCardId}
              reviewNote={reviewNote}
              setReviewNote={setReviewNote}
              busy={busy}
              onReviewAction={handleReviewAction}
              onRelaunchRun={handleRelaunchRun}
            />
          ) : (
            <DeveloperWorkspace runSnapshot={runSnapshot} liveProgress={liveProgress} />
          )}
        </main>
      </div>
    </div>
  )
}

function LiveProgressPanel({
  runSnapshot,
  liveProgress,
  connectionState,
}: {
  runSnapshot: RunSnapshot
  liveProgress: LiveProgressState
  connectionState: 'idle' | 'live' | 'error'
}) {
  const taskSummary = liveProgress.totalTasks
    ? `${liveProgress.completedTasks}/${liveProgress.totalTasks} tasks complete`
    : runSnapshot.stage2?.tasks.length
      ? 'Waiting for Stage 3 to start reading tasks'
      : 'Read plan not available yet'

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Live Progress</h2>
        <span>{formatDate(liveProgress.latestUpdatedAt)}</span>
      </div>
      <div className="two-column-panel progress-panel">
        <div className="focus-card live-progress-card">
          <div className="live-progress-header">
            <div>
              <strong>{stageLabel(liveProgress.currentStage)}</strong>
              <p>{liveProgress.latestMessage}</p>
            </div>
            <StatusPill label="Live Stream" value={connectionState} tone={connectionState === 'live' ? 'success' : 'warning'} />
          </div>
          <div className="progress-stack">
            <ProgressMeter
              label="Pipeline progress"
              value={liveProgress.pipelinePercent}
              detail={`${liveProgress.completedStages}/${liveProgress.totalStages} stages completed`}
            />
            <ProgressMeter
              label="Stage 3 task progress"
              value={liveProgress.stage3Percent}
              detail={liveProgress.activeTaskType ? `Current task: ${liveProgress.activeTaskType}` : taskSummary}
              muted={liveProgress.totalTasks === 0}
            />
          </div>
        </div>

        <div className="focus-card live-progress-card">
          <div className="live-progress-meta-grid">
            <div>
              <span>Stage status</span>
              <strong>{liveProgress.currentStageStatus}</strong>
            </div>
            <div>
              <span>Current task</span>
              <strong>{liveProgress.activeTaskType ?? 'Waiting for next task update'}</strong>
            </div>
            <div>
              <span>Stage 3 tracker</span>
              <strong>{taskSummary}</strong>
            </div>
            <div>
              <span>Artifacts so far</span>
              <strong>{runSnapshot.artifacts.length}</strong>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function ReviewWorkspace({
  runSnapshot,
  selectedPage,
  selectedPageId,
  setSelectedPageId,
  selectedCard,
  selectedCardId,
  setSelectedCardId,
  reviewNote,
  setReviewNote,
  busy,
  onReviewAction,
  onRelaunchRun,
}: {
  runSnapshot: RunSnapshot
  selectedPage: PageRecord | null
  selectedPageId: string
  setSelectedPageId: (value: string) => void
  selectedCard: Stage5BCard | null
  selectedCardId: string
  setSelectedCardId: (value: string) => void
  reviewNote: string
  setReviewNote: (value: string) => void
  busy: string
  onReviewAction: (actionType: ReviewActionType, options?: ReviewActionOptions) => Promise<void>
  onRelaunchRun: () => Promise<void>
}) {
  const pageAtlasById = useMemo(
    () => new Map((runSnapshot.stage1?.page_atlas ?? []).map((entry) => [entry.page_id, entry])),
    [runSnapshot.stage1?.page_atlas],
  )

  const selectedPageAtlasEntry = useMemo(
    () => (selectedPage ? pageAtlasById.get(selectedPage.page_id) ?? null : null),
    [pageAtlasById, selectedPage],
  )

  const selectedPageBroadDetail = selectedPageAtlasEntry
    ? `The current hypothesis is a ${humanizeToken(selectedPageAtlasEntry.page_role)} sheet at ${selectedPageAtlasEntry.role_confidence} confidence, with priority rank ${selectedPageAtlasEntry.importance_rank}${selectedPageAtlasEntry.object_families.length ? ` and likely object families ${selectedPageAtlasEntry.object_families.map((family) => humanizeToken(family)).join(', ')}` : ''}.`
    : 'Stage 1 has not written a page-level interpretation for this sheet yet.'

  return (
    <div className="workspace-stack">
      <section className="panel">
        <div className="panel-heading">
          <h2>Pack Summary</h2>
          <span>{runSnapshot.stage5a?.readiness.coverage_summary ?? 'Awaiting Stage 5A package'}</span>
        </div>
        <div className="metric-grid">
          <MetricCard label="Project hypothesis" value={runSnapshot.stage1?.project_type_hypothesis ?? 'Pending'} />
          <MetricCard label="Candidate objects" value={String(runSnapshot.stage5a?.candidate_objects.length ?? 0)} />
          <MetricCard label="Conflicts" value={String(runSnapshot.stage5a?.conflicts.length ?? 0)} />
          <MetricCard label="Unresolved" value={String(runSnapshot.stage5a?.unresolved.length ?? 0)} />
        </div>
        <p className="body-copy">{runSnapshot.stage5a?.overall_description ?? runSnapshot.stage1?.pack_type_hypothesis ?? 'No summary yet.'}</p>
        <p className="panel-note">Likely object families surfaced during the broad Stage 1 reconnaissance pass.</p>
        <div className="tag-row">
          {(runSnapshot.stage1?.candidate_object_families ?? []).map((family) => (
            <span key={family} className="tag">
              {family.replaceAll('_', ' ')}
            </span>
          ))}
        </div>
      </section>

      <CollapsiblePanel title="Page Gallery / Detail" summary={`${runSnapshot.pages.length} page(s)`} contentClassName="review-grid">
        <div className="panel panel--nested">
          <div className="panel-heading">
            <h2>Page Gallery</h2>
            <span>{runSnapshot.pages.length} page(s)</span>
          </div>
          <div className="page-grid">
            {runSnapshot.pages.map((page) => (
              <button
                key={page.page_id}
                type="button"
                className={`page-card ${selectedPageId === page.page_id ? 'is-active' : ''}`}
                onClick={() => setSelectedPageId(page.page_id)}
              >
                {page.preview_artifact?.path ? <img src={artifactUrl(page.preview_artifact.path)} alt={page.title_hint ?? `Page ${page.page_number}`} /> : null}
                <div>
                  <strong>{page.sheet_number_hint || `Page ${page.page_number}`}</strong>
                  <span>{page.title_hint || 'Untitled page'}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="panel panel--nested page-detail">
          <div className="panel-heading">
            <h2>Page Detail</h2>
            <span>{selectedPage?.sheet_number_hint || selectedPageAtlasEntry?.sheet_number_hint || `Page ${selectedPage?.page_number ?? '-'}`}</span>
          </div>
          {selectedPage?.preview_artifact?.path ? <img className="page-detail-image" src={artifactUrl(selectedPage.preview_artifact.path)} alt={selectedPage.title_hint ?? 'Selected page'} /> : null}
          <div className="focus-card">
            <span className="signal">Stage 1 broad understanding</span>
            <strong>{selectedPage?.title_hint || selectedPageAtlasEntry?.title_hint || selectedPage?.sheet_number_hint || `Page ${selectedPage?.page_number ?? '-'}`}</strong>
            <p>{selectedPageAtlasEntry?.summary ?? 'No broad Stage 1 summary is available for this page yet.'}</p>
            <p>{selectedPageBroadDetail}</p>
            {selectedPageAtlasEntry?.object_families.length ? (
              <div className="tag-row">
                {selectedPageAtlasEntry.object_families.map((family) => (
                  <span key={family} className="tag">
                    {humanizeToken(family)}
                  </span>
                ))}
              </div>
            ) : null}
          </div>
          <dl className="metadata-grid">
            <div>
              <dt>Title</dt>
              <dd>{selectedPage?.title_hint || selectedPageAtlasEntry?.title_hint || 'Not captured from Stage 0 title hints'}</dd>
            </div>
            <div>
              <dt>Text layer</dt>
              <dd>{selectedPage?.text_layer_available ? 'Available' : 'Unavailable'}</dd>
            </div>
            <div>
              <dt>Vector content</dt>
              <dd>{selectedPage?.vector_content_available ? 'Available' : 'Unknown'}</dd>
            </div>
            <div>
              <dt>Stage 0 excerpt</dt>
              <dd>{String(selectedPage?.extensions.text_excerpt ?? 'No text excerpt captured')}</dd>
            </div>
          </dl>
        </div>
      </CollapsiblePanel>

      <CollapsiblePanel title="Stage 5A Candidate Objects" summary={String(runSnapshot.stage5a?.candidate_objects.length ?? 0)} contentClassName="two-column-panel">
        <div>
          <div className="panel-heading">
            <h2>Stage 5A Candidate Objects</h2>
            <span>{runSnapshot.stage5a?.candidate_objects.length ?? 0}</span>
          </div>
          <div className="list-stack">
            {runSnapshot.stage5a?.candidate_objects.map((candidate) => (
              <div key={candidate.candidate_object_id} className="list-card">
                <strong>{candidate.display_label || candidate.object_family}</strong>
                <span>{candidate.supporting_observation_ids.length} supporting observation(s)</span>
                <small>{candidate.confidence_tier}</small>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="panel-heading">
            <h2>Relationships, Conflicts, Unresolved</h2>
            <span>{runSnapshot.stage5a?.candidate_relationships.length ?? 0} relations</span>
          </div>
          <div className="list-stack">
            {runSnapshot.stage5a?.candidate_relationships.map((relationship) => (
              <div key={relationship.candidate_relationship_id} className="list-card">
                <strong>{relationship.relationship_family}</strong>
                <span>
                  {relationship.source_candidate_object_ids.length} source / {relationship.target_candidate_object_ids.length} target
                </span>
                <small>{relationship.confidence_tier}</small>
              </div>
            ))}
            {runSnapshot.stage5a?.conflicts.map((conflict) => (
              <div key={conflict.conflict_id} className="list-card list-card--alert">
                <strong>{conflict.summary}</strong>
                <span>{conflict.impact_scope || 'Review before synthesis.'}</span>
                <small>{conflict.severity}</small>
              </div>
            ))}
            {runSnapshot.stage5a?.unresolved.map((item) => (
              <div key={item.unresolved_id} className="list-card list-card--muted">
                <strong>{item.unresolved_type.replaceAll('_', ' ')}</strong>
                <span>{item.recommended_next_action}</span>
                <small>{item.may_proceed ? 'May proceed' : 'Blocking'}</small>
              </div>
            ))}
          </div>
        </div>
      </CollapsiblePanel>

      <CollapsiblePanel title="Stage 5B Interpretation Board" summary={`${runSnapshot.stage5b?.cards.length ?? 0} card(s)`}>
        <div className="board-grid">
          {runSnapshot.stage5b?.cards.map((card) => (
            <button
              key={card.card_id}
              type="button"
              className={`board-card ${selectedCardId === card.card_id ? 'is-active' : ''}`}
              onClick={() => {
                setSelectedCardId(card.card_id)
                if (card.page_id) {
                  setSelectedPageId(card.page_id)
                }
              }}
            >
              {card.image_asset?.path ? <img src={artifactUrl(card.image_asset.path)} alt={card.title} /> : null}
              <span className={`signal signal--${card.card_type}`}>{card.card_type}</span>
              <strong>{card.title}</strong>
              <p>{card.subtitle || card.reason || 'No additional context.'}</p>
            </button>
          ))}
        </div>
      </CollapsiblePanel>

      <SpecificityExplorer runSnapshot={runSnapshot} selectedCardId={selectedCardId} setSelectedCardId={setSelectedCardId} />

      <section className="panel two-column-panel">
        <div>
          <div className="panel-heading">
            <h2>Selected Board Slice</h2>
            <span>{selectedCard?.confidence_tier || 'unknown'}</span>
          </div>
          <div className="focus-card">
            <strong>{selectedCard?.title || 'No board card selected'}</strong>
            <p>{selectedCard?.subtitle || selectedCard?.reason || 'Select a card to inspect its review target.'}</p>
            <small>{selectedCard?.linked_ids.join(', ') || 'No linked artifact IDs'}</small>
          </div>
        </div>
        <div>
          <div className="panel-heading">
            <h2>Milestone Decision Panel</h2>
            <span>{runSnapshot.run.decision_status || 'Pending'}</span>
          </div>
          <textarea
            className="decision-note"
            value={reviewNote}
            onChange={(event) => setReviewNote(event.target.value)}
            placeholder="Capture review notes or correction instructions"
          />
          <div className="action-row">
            <button type="button" className="primary-button" disabled={Boolean(busy)} onClick={() => void onReviewAction('approve')}>
              Approve checkpoint
            </button>
            <button type="button" className="secondary-button" disabled={Boolean(busy)} onClick={() => void onReviewAction('reject')}>
              Needs correction
            </button>
            <button type="button" className="ghost-button" disabled={Boolean(busy)} onClick={() => void onReviewAction('request_reread')}>
              Request reread
            </button>
            <button
              type="button"
              className="ghost-button"
              disabled={Boolean(busy) || !selectedCard}
              onClick={() =>
                selectedCard
                  ? void onReviewAction('discard_card', {
                      targetIds: [selectedCard.card_id],
                      decisionScope: 'slice',
                      extensions: { card_page_id: selectedCard.page_id ?? null },
                    })
                  : undefined
              }
            >
              Discard selected card
            </button>
            <button
              type="button"
              className="ghost-button"
              disabled={Boolean(busy) || !selectedPage}
              onClick={() =>
                selectedPage
                  ? void onReviewAction('discard_sheet', {
                      targetIds: [selectedPage.page_id],
                      decisionScope: 'region',
                      extensions: { page_id: selectedPage.page_id },
                    })
                  : undefined
              }
            >
              Discard selected sheet
            </button>
            <button type="button" className="ghost-button" disabled={Boolean(busy)} onClick={() => void onReviewAction('note')}>
              Save note
            </button>
            <button type="button" className="secondary-button" disabled={Boolean(busy)} onClick={() => void onRelaunchRun()}>
              {busy === 'relaunch' ? 'Relaunching...' : 'Relaunch 2 to 5 loop'}
            </button>
          </div>
          <p className="panel-note">Relaunch 2 to 5 loop reuses this run's stored review actions as Stage 2 planning feedback and Stage 4 support guidance.</p>
          <div className="list-stack compact-stack">
            {runSnapshot.review_actions.map((action) => (
              <div key={action.action_id} className="list-card">
                <strong>{action.action_type}</strong>
                <span>{action.note || 'No note supplied'}</span>
                <small>{`${action.decision_scope ?? 'unspecified'} / ${formatDate(action.created_at)}`}</small>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

function SpecificityExplorer({
  runSnapshot,
  selectedCardId,
  setSelectedCardId,
}: {
  runSnapshot: RunSnapshot
  selectedCardId: string
  setSelectedCardId: (value: string) => void
}) {
  const [specificityLevel, setSpecificityLevel] = useState<SpecificityLevel>('board')
  const [specificityTargetId, setSpecificityTargetId] = useState('')

  const observations = useMemo(
    () => runSnapshot.stage3.flatMap((task) => [...task.direct_observations, ...task.inferred_observations]),
    [runSnapshot.stage3],
  )

  const optionGroups = useMemo<Record<SpecificityLevel, ExplorerOption[]>>(
    () => ({
      board: (runSnapshot.stage5b?.cards ?? []).map((card) => ({ id: card.card_id, label: truncateText(card.title) })),
      candidate: (runSnapshot.stage5a?.candidate_objects ?? []).map((candidate) => ({ id: candidate.candidate_object_id, label: candidateLabel(candidate) })),
      relationship: (runSnapshot.stage5a?.candidate_relationships ?? []).map((relationship) => ({
        id: relationship.candidate_relationship_id,
        label: humanizeToken(relationship.relationship_family),
      })),
      conflict: (runSnapshot.stage5a?.conflicts ?? []).map((conflict) => ({ id: conflict.conflict_id, label: truncateText(conflict.summary) })),
      unresolved: (runSnapshot.stage5a?.unresolved ?? []).map((item) => ({
        id: item.unresolved_id,
        label: truncateText(humanizeToken(item.unresolved_type)),
      })),
      observation: observations.map((observation) => ({ id: observation.observation_id, label: observationLabel(observation) })),
      support: runSnapshot.stage4.map((artifact) => ({ id: artifact.task_id, label: truncateText(artifact.extraction_objective) })),
    }),
    [observations, runSnapshot.stage4, runSnapshot.stage5a, runSnapshot.stage5b],
  )

  const activeOptions = optionGroups[specificityLevel]

  useEffect(() => {
    if (specificityLevel === 'board' && selectedCardId) {
      setSpecificityTargetId(selectedCardId)
      return
    }
    if (!activeOptions.some((option) => option.id === specificityTargetId)) {
      setSpecificityTargetId(activeOptions[0]?.id ?? '')
    }
  }, [activeOptions, selectedCardId, specificityLevel, specificityTargetId])

  const selectedBoardCard = (runSnapshot.stage5b?.cards ?? []).find((card) => card.card_id === specificityTargetId) ?? null
  const selectedCandidate = (runSnapshot.stage5a?.candidate_objects ?? []).find((candidate) => candidate.candidate_object_id === specificityTargetId) ?? null
  const selectedRelationship = (runSnapshot.stage5a?.candidate_relationships ?? []).find((relationship) => relationship.candidate_relationship_id === specificityTargetId) ?? null
  const selectedConflict = (runSnapshot.stage5a?.conflicts ?? []).find((conflict) => conflict.conflict_id === specificityTargetId) ?? null
  const selectedUnresolved = (runSnapshot.stage5a?.unresolved ?? []).find((item) => item.unresolved_id === specificityTargetId) ?? null
  const selectedObservation = observations.find((observation) => observation.observation_id === specificityTargetId) ?? null
  const selectedSupport = runSnapshot.stage4.find((artifact) => artifact.task_id === specificityTargetId) ?? null

  const selectorLabel: Record<SpecificityLevel, string> = {
    board: 'Board slice',
    candidate: 'Candidate object',
    relationship: 'Relationship',
    conflict: 'Conflict',
    unresolved: 'Unresolved item',
    observation: 'Observation',
    support: 'Support artifact',
  }

  return (
    <section className="panel two-column-panel">
      <div>
        <div className="panel-heading">
          <h2>Specificity Explorer</h2>
          <span>{selectorLabel[specificityLevel]}</span>
        </div>
        <div className="specificity-controls">
          <label className="stack-form-label">
            <span>Specificity level</span>
            <select value={specificityLevel} onChange={(event) => setSpecificityLevel(event.target.value as SpecificityLevel)}>
              <option value="board">Board slice</option>
              <option value="candidate">Candidate object</option>
              <option value="relationship">Relationship</option>
              <option value="conflict">Conflict</option>
              <option value="unresolved">Unresolved item</option>
              <option value="observation">Observation</option>
              <option value="support">Stage 4 support</option>
            </select>
          </label>
          <label className="stack-form-label">
            <span>{selectorLabel[specificityLevel]}</span>
            <select
              value={specificityTargetId}
              onChange={(event) => {
                setSpecificityTargetId(event.target.value)
                if (specificityLevel === 'board') {
                  setSelectedCardId(event.target.value)
                }
              }}
              disabled={!activeOptions.length}
            >
              {!activeOptions.length ? <option value="">No records available</option> : null}
              {activeOptions.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
        </div>
        <p className="panel-note">Use the first dropdown to choose the level of detail, then the second to inspect the exact slice inside that level.</p>
      </div>

      <div>
        {!activeOptions.length ? (
          <div className="focus-card">
            <strong>No records available</strong>
            <p>This run does not have data for the selected specificity level yet.</p>
          </div>
        ) : specificityLevel === 'board' && selectedBoardCard ? (
          <div className="focus-card detail-stack">
            <strong>{selectedBoardCard.title}</strong>
            <p>{selectedBoardCard.subtitle || selectedBoardCard.reason || 'No additional context.'}</p>
            <div className="detail-grid">
              <div>
                <span>Card type</span>
                <strong>{humanizeToken(selectedBoardCard.card_type)}</strong>
              </div>
              <div>
                <span>Confidence</span>
                <strong>{selectedBoardCard.confidence_tier}</strong>
              </div>
              <div>
                <span>Page</span>
                <strong>{selectedBoardCard.page_id || 'Not linked'}</strong>
              </div>
              <div>
                <span>Linked IDs</span>
                <strong>{selectedBoardCard.linked_ids.join(', ') || 'None'}</strong>
              </div>
            </div>
          </div>
        ) : specificityLevel === 'candidate' && selectedCandidate ? (
          <div className="focus-card detail-stack">
            <strong>{candidateLabel(selectedCandidate)}</strong>
            <p>{humanizeToken(selectedCandidate.object_family)}</p>
            <div className="detail-grid">
              <div>
                <span>Supporting observations</span>
                <strong>{selectedCandidate.supporting_observation_ids.length}</strong>
              </div>
              <div>
                <span>Confidence</span>
                <strong>{selectedCandidate.confidence_tier}</strong>
              </div>
              <div>
                <span>Pages</span>
                <strong>{toStringArray(selectedCandidate.spatial_hints.page_ids).join(', ') || 'No page links'}</strong>
              </div>
              <div>
                <span>Conflict / unresolved</span>
                <strong>{`${selectedCandidate.conflict_ids.length} / ${selectedCandidate.unresolved_ids.length}`}</strong>
              </div>
            </div>
          </div>
        ) : specificityLevel === 'relationship' && selectedRelationship ? (
          <div className="focus-card detail-stack">
            <strong>{humanizeToken(selectedRelationship.relationship_family)}</strong>
            <p>Relationship candidates assembled in Stage 5A.</p>
            <div className="detail-grid">
              <div>
                <span>Source objects</span>
                <strong>{selectedRelationship.source_candidate_object_ids.join(', ') || 'None'}</strong>
              </div>
              <div>
                <span>Target objects</span>
                <strong>{selectedRelationship.target_candidate_object_ids.join(', ') || 'None'}</strong>
              </div>
              <div>
                <span>Supporting observations</span>
                <strong>{selectedRelationship.supporting_observation_ids.length}</strong>
              </div>
              <div>
                <span>Confidence</span>
                <strong>{selectedRelationship.confidence_tier}</strong>
              </div>
            </div>
          </div>
        ) : specificityLevel === 'conflict' && selectedConflict ? (
          <div className="focus-card detail-stack">
            <strong>{selectedConflict.summary}</strong>
            <p>{selectedConflict.impact_scope || 'Conflict preserved for review.'}</p>
            <div className="detail-grid">
              <div>
                <span>Severity</span>
                <strong>{selectedConflict.severity}</strong>
              </div>
              <div>
                <span>Conflict type</span>
                <strong>{humanizeToken(selectedConflict.conflict_type)}</strong>
              </div>
              <div>
                <span>Related IDs</span>
                <strong>{selectedConflict.related_ids.join(', ') || 'None linked'}</strong>
              </div>
              <div>
                <span>Conflict ID</span>
                <strong>{selectedConflict.conflict_id}</strong>
              </div>
            </div>
          </div>
        ) : specificityLevel === 'unresolved' && selectedUnresolved ? (
          <div className="focus-card detail-stack">
            <strong>{humanizeToken(selectedUnresolved.unresolved_type)}</strong>
            <p>{selectedUnresolved.blocking_reason || selectedUnresolved.recommended_next_action}</p>
            <div className="detail-grid">
              <div>
                <span>May proceed</span>
                <strong>{selectedUnresolved.may_proceed ? 'Yes' : 'No'}</strong>
              </div>
              <div>
                <span>Targets</span>
                <strong>{selectedUnresolved.target_ids.join(', ') || 'No targets linked'}</strong>
              </div>
              <div>
                <span>Next action</span>
                <strong>{selectedUnresolved.recommended_next_action}</strong>
              </div>
              <div>
                <span>Unresolved ID</span>
                <strong>{selectedUnresolved.unresolved_id}</strong>
              </div>
            </div>
          </div>
        ) : specificityLevel === 'observation' && selectedObservation ? (
          <div className="focus-card detail-stack">
            <strong>{selectedObservation.summary || humanizeToken(selectedObservation.observation_type)}</strong>
            <p>{`${humanizeToken(selectedObservation.object_family)} / ${humanizeToken(selectedObservation.epistemic_status)}`}</p>
            <div className="detail-grid">
              <div>
                <span>Observation type</span>
                <strong>{humanizeToken(selectedObservation.observation_type)}</strong>
              </div>
              <div>
                <span>Confidence</span>
                <strong>{selectedObservation.confidence_tier}</strong>
              </div>
              <div>
                <span>Page</span>
                <strong>{selectedObservation.page_id || 'Not linked'}</strong>
              </div>
              <div>
                <span>Candidate links</span>
                <strong>{selectedObservation.linked_candidate_ids.join(', ') || 'None'}</strong>
              </div>
            </div>
            <pre className="json-block">{JSON.stringify(selectedObservation.observed_values, null, 2)}</pre>
          </div>
        ) : specificityLevel === 'support' && selectedSupport ? (
          <div className="focus-card detail-stack">
            <strong>{selectedSupport.extraction_objective}</strong>
            <p>Deterministic support search collected during Stage 4.</p>
            <div className="detail-grid">
              <div>
                <span>Pages</span>
                <strong>{selectedSupport.page_ids.join(', ') || 'No pages linked'}</strong>
              </div>
              <div>
                <span>Dimension candidates</span>
                <strong>{selectedSupport.dimension_candidates.join(', ') || 'None captured'}</strong>
              </div>
            </div>
            <pre className="json-block">{JSON.stringify({ snippets: selectedSupport.snippets, warnings: selectedSupport.warnings }, null, 2)}</pre>
          </div>
        ) : (
          <div className="focus-card">
            <strong>No detail available</strong>
            <p>The selected record could not be resolved in the current snapshot.</p>
          </div>
        )}
      </div>
    </section>
  )
}

function DeveloperWorkspace({ runSnapshot, liveProgress }: { runSnapshot: RunSnapshot; liveProgress: LiveProgressState | null }) {
  return (
    <div className="workspace-stack">
      <section className="panel">
        <div className="panel-heading">
          <h2>Run Telemetry</h2>
          <span>{runSnapshot.run.run_id}</span>
        </div>
        <div className="metric-grid">
          <MetricCard label="Run status" value={runSnapshot.run.status} />
          <MetricCard label="Current stage" value={stageLabel(runSnapshot.run.current_stage)} />
          <MetricCard label="Artifact count" value={String(runSnapshot.artifacts.length)} />
          <MetricCard label="Model mode" value={String(runSnapshot.config.model_mode ?? 'mock')} />
          <MetricCard label="Playbook" value={runSnapshot.run.selected_playbook ?? runSnapshot.run.playbook_override ?? 'automatic'} />
        </div>
      </section>

      <section className="panel two-column-panel">
        <div>
          <div className="panel-heading">
            <h2>Stage Timeline</h2>
            <span>{runSnapshot.stage_events.length} events</span>
          </div>
          <div className="timeline">
            {runSnapshot.stage_events.map((event) => (
              <div key={event.event_id} className="timeline-row">
                <div>
                  <strong>{stageLabel(event.stage)}</strong>
                  <span>{event.status}</span>
                </div>
                <p>{event.message}</p>
                <small>{formatDate(event.created_at)}</small>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="panel-heading">
            <h2>Read Plan</h2>
            <span>{runSnapshot.stage2?.tasks.length ?? 0} tasks</span>
          </div>
          <div className="list-stack">
            {runSnapshot.stage2?.tasks.map((task) => (
              <div key={task.task_id} className="list-card">
                <div className="list-card-header">
                  <strong>{task.task_type}</strong>
                  <span className={`task-status task-status--${liveProgress?.taskStatusById[task.task_id] ?? 'pending'}`}>
                    {liveProgress?.taskStatusById[task.task_id] ?? 'pending'}
                  </span>
                </div>
                <span>{task.prompt_family}</span>
                <small>{task.target_page_ids.join(', ')}</small>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="panel two-column-panel">
        <div>
          <div className="panel-heading">
            <h2>Stage 3 Task Results</h2>
            <span>{runSnapshot.stage3.length}</span>
          </div>
          <div className="list-stack">
            {runSnapshot.stage3.map((task) => (
              <div key={task.task_id} className="list-card">
                <strong>{task.summary}</strong>
                <span>
                  {task.direct_observations.length} direct / {task.inferred_observations.length} inferred observation(s)
                </span>
                <small>{task.support_recommended ? 'Support path recommended' : 'Vision-first sufficient'}</small>
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="panel-heading">
            <h2>Stage 4 Support Artifacts</h2>
            <span>{runSnapshot.stage4.length}</span>
          </div>
          <div className="list-stack">
            {runSnapshot.stage4.map((artifact) => (
              <div key={artifact.task_id} className="list-card">
                <strong>{artifact.extraction_objective}</strong>
                <span>{artifact.dimension_candidates.join(', ') || 'No dimension candidates extracted'}</span>
                <small>{artifact.snippets[0] || artifact.warnings[0] || 'No support notes'}</small>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <h2>Artifact Browser</h2>
          <span>{runSnapshot.artifacts.length} files</span>
        </div>
        <div className="artifact-table">
          <div className="artifact-row artifact-row--header">
            <span>Path</span>
            <span>Kind</span>
            <span>Schema</span>
            <span>Size</span>
          </div>
          {runSnapshot.artifacts.map((artifact, index) => (
            <div key={`${String(artifact.path)}-${index}`} className="artifact-row">
              <span>{String(artifact.path)}</span>
              <span>{String(artifact.kind ?? '-')}</span>
              <span>{String(artifact.schema_id ?? '-')}</span>
              <span>{String(artifact.size ?? '-')}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

function CollapsiblePanel({
  title,
  summary,
  defaultOpen = false,
  actions,
  className,
  contentClassName,
  children,
}: CollapsiblePanelProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen)
  const panelClassName = ['panel', 'collapsible-panel', isOpen ? 'is-open' : '', className].filter(Boolean).join(' ')
  const contentClassNames = ['collapsible-panel-content', contentClassName].filter(Boolean).join(' ')

  return (
    <section className={panelClassName}>
      <div className="collapsible-panel-header">
        <button type="button" className="collapsible-trigger" aria-expanded={isOpen} onClick={() => setIsOpen((current) => !current)}>
          <span className="collapsible-arrow" aria-hidden="true">
            {'>'}
          </span>
          <span className="collapsible-title-group">
            <h2>{title}</h2>
            {summary ? <span className="collapsible-summary">{summary}</span> : null}
          </span>
        </button>
        {actions ? <div className="collapsible-actions">{actions}</div> : null}
      </div>
      {isOpen ? <div className={contentClassNames}>{children}</div> : null}
    </section>
  )
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function ProgressMeter({ label, value, detail, muted = false }: { label: string; value: number; detail: string; muted?: boolean }) {
  const clampedValue = Math.max(0, Math.min(100, value))
  return (
    <div className={`progress-meter ${muted ? 'progress-meter--muted' : ''}`}>
      <div className="progress-meter-header">
        <span>{label}</span>
        <strong>{clampedValue}%</strong>
      </div>
      <div className="progress-track" aria-hidden="true">
        <div className="progress-fill" style={{ width: `${clampedValue}%` }} />
      </div>
      <small>{detail}</small>
    </div>
  )
}

function StatusPill({ label, value, tone }: { label: string; value: string; tone: 'neutral' | 'success' | 'warning' }) {
  return (
    <div className={`status-pill status-pill--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

export default App
