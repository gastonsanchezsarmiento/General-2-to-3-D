export interface ArtifactRef {
  artifact_id: string
  artifact_type: string
  schema_id?: string | null
  schema_version?: string | null
  run_id?: string | null
  path?: string | null
}

export interface ProjectRecord {
  project_id: string
  name: string
  description?: string | null
  created_at: string
}

export interface SourceDocumentRecord {
  source_document_id: string
  project_id: string
  original_filename: string
  stored_path: string
  checksum: string
  file_size: number
  page_count?: number | null
  created_at: string
}

export interface RunRecord {
  run_id: string
  project_id: string
  source_document_ids: string[]
  status: string
  current_stage?: string | null
  current_stage_status?: string | null
  decision_status?: string | null
  playbook_override?: string | null
  selected_playbook?: string | null
  feedback_source_run_id?: string | null
  relaunch_scope?: string | null
  created_at: string
  updated_at: string
}

export interface EvidenceRef {
  source_type: string
  page_id?: string | null
  confidence_tier: string
  note?: string | null
}

export interface PlaybookSummary {
  key: string
  label: string
  description: string
  default: boolean
}

export interface StageEvent {
  event_id: string
  run_id: string
  stage: string
  status: string
  message: string
  created_at: string
  payload: Record<string, unknown>
}

export interface PageRecord {
  page_id: string
  source_document_id: string
  page_number: number
  preview_artifact?: ArtifactRef | null
  master_artifact?: ArtifactRef | null
  sheet_number_hint?: string | null
  title_hint?: string | null
  text_layer_available?: boolean | null
  vector_content_available?: boolean | null
  likely_scanned?: boolean | null
  extensions: Record<string, unknown>
}

export interface PageAtlasEntry {
  page_id: string
  page_number: number
  page_role: string
  role_confidence: string
  importance_rank: number
  title_hint?: string | null
  sheet_number_hint?: string | null
  object_families: string[]
  summary: string
  preview_artifact?: ArtifactRef | null
}

export interface Stage1Reconnaissance {
  run_id: string
  pack_type_hypothesis: string
  discipline_hypothesis: string
  project_type_hypothesis: string
  candidate_object_families: string[]
  page_atlas: PageAtlasEntry[]
  anchor_page_ids: string[]
  schedule_page_ids: string[]
  detail_page_ids: string[]
  unresolved_questions: string[]
  recommended_next_pages: string[]
  selected_playbook?: string | null
  playbook_source?: string | null
  playbook_rationale?: string | null
  playbook_focus: string[]
  playbook_focus_page_ids: string[]
}

export interface ReadTask {
  task_id: string
  task_type: string
  target_page_ids: string[]
  prompt_family: string
  expected_output_schema_id: string
  support_eligible: boolean
  escalation_rule?: string | null
  extensions: Record<string, unknown>
}

export interface ReadPlan {
  plan_id: string
  run_id: string
  working_project_hypothesis: string
  collection_goals: string[]
  tasks: ReadTask[]
  playbook_key?: string | null
  playbook_guidance: string[]
  priority_page_ids: string[]
}

export interface Observation {
  observation_id: string
  run_id: string
  task_id?: string | null
  observation_type: string
  object_family?: string | null
  page_id?: string | null
  summary?: string | null
  observed_values: Record<string, unknown>
  supporting_evidence: EvidenceRef[]
  confidence_tier: string
  epistemic_status: string
  linked_candidate_ids: string[]
}

export interface Stage3TaskResult {
  run_id: string
  task_id: string
  page_ids: string[]
  prompt_family: string
  summary: string
  direct_observations: Observation[]
  inferred_observations: Observation[]
  unresolved_questions: string[]
  support_recommended: boolean
}

export interface Stage4SupportArtifact {
  run_id: string
  task_id: string
  extraction_objective: string
  page_ids: string[]
  snippets: string[]
  dimension_candidates: string[]
  warnings: string[]
}

export interface CandidateObject {
  candidate_object_id: string
  run_id: string
  object_family: string
  display_label?: string | null
  supporting_observation_ids: string[]
  supporting_evidence: EvidenceRef[]
  confidence_tier: string
  spatial_hints: Record<string, unknown>
  conflict_ids: string[]
  unresolved_ids: string[]
}

export interface CandidateRelationship {
  candidate_relationship_id: string
  run_id: string
  relationship_family: string
  source_candidate_object_ids: string[]
  target_candidate_object_ids: string[]
  supporting_observation_ids: string[]
  supporting_evidence: EvidenceRef[]
  confidence_tier: string
}

export interface ConflictRecord {
  conflict_id: string
  run_id: string
  conflict_type: string
  severity: string
  related_ids: string[]
  summary: string
  impact_scope?: string | null
}

export interface UnresolvedRecord {
  unresolved_id: string
  unresolved_type: string
  target_ids: string[]
  blocking_reason?: string | null
  recommended_next_action: string
  may_proceed: boolean
}

export interface Stage5AReadiness {
  ready_for_human_review: boolean
  ready_for_stage6: boolean
  coverage_summary: string
  blockers: string[]
  warnings: string[]
  synthesize_now: string[]
  synthesize_later: string[]
}

export interface Stage5APackage {
  run_id: string
  package_id: string
  packaging_cycle_id: string
  packaging_profile: string
  readiness: Stage5AReadiness
  overall_description: string
  precise_understanding: string[]
  candidate_objects: CandidateObject[]
  candidate_relationships: CandidateRelationship[]
  conflicts: ConflictRecord[]
  unresolved: UnresolvedRecord[]
  observation_ids: string[]
  playbook_key?: string | null
  playbook_label?: string | null
  coverage_hits: string[]
  coverage_misses: string[]
}

export interface Stage5BCard {
  card_id: string
  card_type: 'candidate' | 'relationship' | 'conflict' | 'unresolved' | 'page'
  title: string
  subtitle?: string | null
  confidence_tier: string
  image_asset?: ArtifactRef | null
  linked_ids: string[]
  page_id?: string | null
  reason?: string | null
}

export interface Stage5BBoard {
  run_id: string
  board_id: string
  summary: string
  cards: Stage5BCard[]
  feedback_targets: Array<Record<string, unknown>>
}

export interface HumanReviewAction {
  action_id: string
  run_id: string
  review_stage: string
  action_type: string
  decision_scope?: string | null
  target_ids: string[]
  created_at: string
  note?: string | null
  extensions: Record<string, unknown>
}

export interface ProjectDetail {
  project: ProjectRecord
  documents: SourceDocumentRecord[]
  runs: RunRecord[]
}

export interface RunSnapshot {
  project: ProjectRecord
  run: RunRecord
  documents: SourceDocumentRecord[]
  pages: PageRecord[]
  stage_events: StageEvent[]
  review_actions: HumanReviewAction[]
  stage1?: Stage1Reconnaissance | null
  stage2?: ReadPlan | null
  stage3: Stage3TaskResult[]
  stage4: Stage4SupportArtifact[]
  stage5a?: Stage5APackage | null
  stage5b?: Stage5BBoard | null
  artifacts: Array<Record<string, unknown>>
  config: Record<string, unknown>
}
