# Stage 10 - Structured Human Review Of The Browser Model

## 0. Purpose

Stage 10 is the structured human review layer for the browser-facing review path.

Its job is to let a human inspect the interpreted model, review the supporting evidence, and record structured actions that the orchestrator can route back into the workflow.

This stage is the final trust boundary before later export-oriented workflows.

---

## 1. Core Role

Stage 10 is the downstream human review and correction stage.

It should:

- consume reviewable browser artifacts from Stage 8 and, when present, Stage 8A
- present stable review targets and their evidence context
- capture structured human review actions rather than relying on loose free chat
- preserve explicit links between the review action and the affected scene, model, issue, and evidence artifacts
- return those actions to the orchestrator for routing, invalidation, and rerun planning

It should not:

- destructively mutate upstream artifacts in place
- become a freeform correction store with no stable IDs
- invent a second semantic truth layer separate from Stage 8 and Stage 8A
- bypass the orchestrator's control of reruns and downstream readiness

---

## 2. What This Stage Receives

Stage 10 should receive the browser-review artifacts that make structured inspection possible.

Primary inputs should include:

- run ID
- review session ID
- Stage 8 scene graph manifest
- Stage 8 scene nodes and edges relevant to the review scope
- Stage 8 issue markers and evidence links
- Stage 8 scene slice results
- Stage 8A review model manifest when present
- Stage 8A review entities, interaction indexes, issue presentations, and evidence presentations when present
- Stage 7 verification issues, findings, and review-queue items relevant to the scope
- orchestrator review instructions

Useful supporting inputs may include:

- prior human review action artifacts
- publication policy artifacts
- prior invalidation and rerun decisions
- milestone decisions and readiness notes from earlier loops

---

## 3. What This Stage Actually Does

### 3.1 Present stable review targets

Stage 10 should present review targets that are backed by stable IDs from Stage 8 and Stage 8A.

Those targets may include:

- scene nodes
- scene edges
- issue markers
- grouped review entities
- evidence-linked placeholders for unresolved or blocked content

### 3.2 Attach evidence and issue context

The reviewer should be able to see why a target exists, why it is uncertain, and which evidence or issues are attached to it.

This means the review surface should expose:

- evidence jumps
- issue state
- verification state
- geometry maturity or provisional state
- source lineage when relevant

### 3.3 Capture structured human review actions

The main output of this stage should be structured review actions.

Recommended action families include:

- approve
- reject
- mark uncertain
- request reread
- change type
- correct relation
- correct geometry
- confirm inferred value

Natural-language comments may still be allowed, but they should be attached to structured review actions rather than replacing them.

### 3.4 Return control to the orchestrator

Stage 10 should not decide rerun routing on its own.

It should publish the review actions and any session-level review state so the orchestrator can:

- decide invalidation scope
- decide rerun targets
- decide whether the reviewed content is accepted, provisional, or blocked for later use

---

## 4. Review Action Contract

Stage 10 should use a stable, structured action contract.

The canonical cross-stage review-action contract for the current registry wave lives under `Schemas/review/human-review-action.schema.json`.

Every published review action that will be consumed by the orchestrator or later stages should declare:

- `schema_id`
- `schema_version`
- stable target references
- stable actor and timestamp information
- action family
- review disposition
- attached notes or corrections when present

Stage 10 may also emit session-local helper artifacts such as review panels, annotation layouts, or temporary UI state, but those helper payloads may remain stage-local until a future `Schemas/stage10/` surface is justified.

---

## 5. Output Families

Recommended output families:

- human review action artifacts
- review session manifest
- target status index
- reviewer note attachments
- readiness or approval recommendation artifacts

For the current registry wave, only the durable human review actions need canonical cross-stage treatment.

The other review-session helpers may stay stage-local as long as the orchestrator can still read the durable review actions.

---

## 6. Relationship To Stage 8 And Stage 8A

Stage 8 owns the published semantic scene truth.

Stage 8A, when present, owns the richer review-model surface built on top of that truth.

The boundary is:

- Stage 8 and Stage 8A define what the human is reviewing
- Stage 10 defines how the human records structured decisions about that reviewable content

If Stage 10 repeatedly needs to invent missing review targets, stable IDs, or evidence jumps, the problem belongs upstream in Stage 8 or Stage 8A.

---

## 7. Relationship To The Orchestrator

Stage 10 is orchestrator-controlled.

The orchestrator should decide:

- what review scope is open for the session
- whether the session is exploratory, blocking, or approval-oriented
- how the resulting review actions map to invalidation and rerun scope
- whether the reviewed content is accepted for later downstream use

Stage 10 should publish review actions and session state back into the shared artifact space.

The orchestrator should read those actions and decide the next workflow transition.

---

## 8. Design Rules

Stage 10 should follow these rules.

### Rule 1

Use structured review actions as the primary trust boundary, not free chat alone.

### Rule 2

Attach every review action to durable target IDs.

### Rule 3

Preserve evidence and issue context at review time.

### Rule 4

Do not let review actions overwrite the original evidence history destructively.

### Rule 5

Keep human corrections in artifact space so reruns and audits remain traceable.

### Rule 6

Let the orchestrator own invalidation and rerun routing.

---

## 9. Build Guidance

Stage 10 spans both backend review-state handling and browser review interaction.

### Recommended backend runtime

- Python 3.11 or newer
- orchestrator-controlled review-action service or backend endpoint
- artifact-backed persistence on filesystem for the POC

### Recommended browser runtime

- TypeScript
- React
- the same application shell used by the review and developer workspaces
- Three.js or the Stage 8A browser viewer only when the richer review model is present

### Recommended packages

- backend: `pydantic`, `orjson`, `tenacity`
- frontend: the same React stack used by the review workspace, plus whatever state layer is already used there

### Suggested file structure

```text
pipeline/
  stage10_review/
    action_service.py
    session_manager.py
    target_index.py
    output_schema.py
    writer.py

frontend/
  review-app/
    src/
      review/
        targetPanel.tsx
        actionBar.tsx
        evidencePanel.tsx
        issuePanel.tsx
        reviewSessionStore.ts

outputs/
  runs/<run_id>/
    stage10/
      review-actions/
      sessions/
      target-status/
      logs/
```

### Implementation notes

- keep review target IDs stable and durable
- separate transient browser UI state from durable review-action artifacts
- write structured review actions immediately rather than relying on later manual transcription
- keep reviewer notes attached to the target and action they refer to
- publish durable human review actions against the canonical contract under `Schemas/review/`

---

## 10. Exit Criteria

Stage 10 should not be considered successful just because a browser screen loaded.

It is successful when:

- the reviewer can inspect the intended scope clearly
- stable targets, evidence, and issue state are navigable
- structured review actions can be recorded against durable IDs
- those actions persist into artifact space
- the orchestrator can route the result without guessing what the reviewer meant

Stage 10 may also produce partial review sessions.

That is acceptable if the recorded actions and session state make the remaining unresolved review work explicit.

---

## 11. HOW TO

Use this stage after Stage 8 or Stage 8A has produced a reviewable browser scope.

Practical execution order:

1. let the orchestrator choose the review scope and session purpose
2. load the Stage 8 scene artifacts and the Stage 8A review model artifacts when present
3. present stable review targets along with their evidence, issue, and verification context
4. let the reviewer inspect targets and record structured actions such as approve, reject, request reread, or correction
5. write each durable human review action into artifact space under the canonical review-action contract
6. write any session-level helper artifacts needed for later session continuity
7. return control to the orchestrator so it can decide invalidation, rerun, acceptance, or escalation

What to avoid:

- do not rely on unstructured chat alone to represent the human decision
- do not let transient browser state become the only record of review
- do not overwrite upstream artifacts in place
- do not let review actions point at unstable UI-only identifiers

What good looks like:

- stable review targets
- explicit human actions
- durable evidence-linked corrections
- orchestrator-readable review outputs that can drive targeted reruns