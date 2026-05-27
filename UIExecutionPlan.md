# UI And Execution Plan

## 0. Purpose

This document translates the architecture into a UI and workspace execution plan.

It is a supporting plan, not the top-level product execution brief.

`ExecutionPlan.md` is the main whole-product execution plan for Codex.

This file should be used as the narrower companion for UI, review workspace, and developer workspace decisions.

It exists because the stage documents intentionally define backend contracts and artifact flows, but they do not define the full product UI or the implementation sequence.

Use this file to keep the implementation aligned with:

- [MainPlan3.md](MainPlan3.md)
- the stage contracts under `Stages/`
- the milestone intentions captured in `Notes.txt`

Core rule:

- `MainPlan3.md` remains the architectural source of truth
- the stage files remain the contract source of truth
- this document is the execution and UI alignment layer

---

## 1. Working Position

The product should be built as one system with two surfaces, not as two disconnected products.

### 1.1 Review UI

The review UI is for judging interpretation quality.

Its job is to let a human quickly answer:

- what does the system think this drawing pack is
- what is on each page
- what evidence supports that belief
- what is still uncertain or conflicting
- is the first milestone good enough to approve

### 1.2 Developer Console

The developer console is for flow visibility and debugging.

Its job is to let a developer quickly answer:

- which stage is running now
- what artifacts were produced
- which prompts and models were used
- where a failure happened
- what changed between reruns
- what the token, latency, and cost profile looks like

### 1.3 Why this should be one application

These two surfaces should share the same backend APIs, event stream, run IDs, artifact registry, and authentication model.

That avoids building two different data access paths for the same system state.

Recommended structure:

- one backend pipeline and artifact API
- one web application shell
- one review workspace
- one developer workspace

---

## 2. Milestone Mapping

The milestone notes are useful, but they should be mapped onto the current stage architecture rather than followed literally as a separate architecture.

### 2.1 Milestone 1 from Notes

"Initial readthrough by GPT-5.5 and broad understanding of what is on each page, shown in a UI."

Current architecture mapping:

- Stage 0 ingestion and page manifests
- Stage 1 reconnaissance pass
- Stage 2 read planning

UI proof needed:

- pack summary
- page gallery
- page role guesses
- high-level confidence and unresolved notes

Exit rule:

- a human agrees that the broad pack understanding is directionally correct

### 2.2 Milestone 2 from Notes

"A detailed sub-agent reads drawings in detail and we sample-check accuracy."

Current architecture mapping:

- Stage 3 targeted reading
- Stage 4 support extraction when useful
- Stage 5A packaging inputs

UI proof needed:

- sampled sheet inspector
- evidence-linked extracted findings
- comparison between page evidence and extracted claims

Exit rule:

- sampled evaluation passes the chosen acceptance threshold

Important note:

The 95 percent target requires a real benchmark set, not only intuition.

### 2.3 Milestone 3 from Notes

"Inspect the returned JSON and ask another AI to explain what it thinks is in it."

Current architecture mapping:

- Stage 5A coherent observation package

UI proof needed:

- raw artifact inspector
- human-readable package summary
- AI explanation panel for the selected artifact
- evidence and lineage links back to source pages and crops

Exit rule:

- the package is understandable, evidence-linked, and does not collapse into one opaque blob

### 2.4 Milestone 4 from Notes

"First attempt at the graph and how a human verifies it."

Current architecture mapping:

- later Stage 8 scene graph
- later Stage 8A richer review model

Important scope rule:

This should not be pulled into the first build if the first build is explicitly limited to Stage 5A and Stage 5B.

For the first implementation phase, the correct substitute for this milestone is the Stage 5B interpretation board.

### 2.5 Milestone 5 from Notes

"3JS drawing of footings, columns, and beams."

Current architecture mapping:

- Stage 6 neutral model
- Stage 7 verification
- Stage 8 publication
- Stage 8A Three.js review model

Important scope rule:

This is a later proof that the upstream interpretation and model are strong enough.

It is not the first implementation target.

---

## 3. First Build Scope

The first execution focus should end at the first milestone checkpoint.

That means the first build should include enough of the system to reach:

- broad pack understanding
- targeted reading and evidence capture
- coherent observation packaging in Stage 5A
- low-resolution visual review in Stage 5B
- explicit human approval or correction routing

The first build should not yet require:

- Stage 6 neutral-model synthesis
- Stage 7 verification loop
- Stage 8 scene graph publication
- Stage 8A Three.js review model
- Stage 10 final browser correction loop

This is the right cut because it proves the AI can interpret the pack in a way a human can inspect before the heavier geometry and model pipeline exists.

---

## 4. Review UI Plan

The review UI should grow with the process.

Do not try to design the final browser product at the start.

Build the smallest review surface that can prove each milestone.

### 4.1 Review UI for the first build

The first review workspace should include:

- run selector
- pack summary header
- page gallery with page roles and quick confidence labels
- page detail viewer
- evidence crop viewer
- Stage 5A package summary panel
- Stage 5A candidate object and relationship inspector
- Stage 5A unresolved and conflict panel
- Stage 5B visual interpretation board
- human approval and correction action panel

### 4.2 What the user should be able to do in the first build

The user should be able to:

- open a run
- see what the AI thinks the pack is about
- open any page and inspect the main findings
- click a Stage 5A object group and see its supporting evidence
- click a Stage 5B card and jump to the underlying page or crop
- filter unresolved or conflict-heavy items
- approve the first milestone or request a rerun or correction

### 4.3 What should be deferred

Do not spend early time on:

- polished 3D navigation
- final Three.js scene controls
- advanced browser rendering performance work
- export workflows

Those are later-stage concerns.

---

## 5. Developer Console Plan

The developer console is necessary.

Without it, debugging an agentic multi-stage pipeline becomes slow and blind.

### 5.1 First developer-console capabilities

The first developer workspace should include:

- run timeline by stage
- current stage status
- job queue and worker state
- artifact list by stage
- prompt version and prompt input references
- model call journal
- token, latency, and cost summary
- error log panel
- raw artifact JSON viewer
- rerun controls for narrow slices

### 5.2 Later developer-console capabilities

Later the console can grow into:

- diff view between two runs
- artifact lineage graph
- stage dependency graph
- schema validation dashboard
- prompt A and B experiment tracking
- quality benchmark reports

### 5.3 Product decision

The developer console should be considered part of the product engineering surface, not an optional afterthought.

---

## 6. Execution Sequence

Recommended implementation order:

### Phase 0 - foundation

Build the minimum shared backbone:

- config loading
- secrets loading
- run ID generation
- artifact storage layout
- manifest writing
- schema validation helpers
- event stream for live status

### Phase 1 - application shell

Build one application shell with:

- review workspace route
- developer workspace route
- backend API for runs and artifacts
- live status panel

At this point the UI can be mostly placeholder data.

### Phase 2 - first reading loop

Implement enough backend flow to support:

- Stage 0 ingestion
- Stage 1 reconnaissance
- Stage 2 read planning
- Stage 3 targeted reads
- optional Stage 4 support extraction

### Phase 3 - Stage 5A

Implement the coherent observation package:

- package manifest
- overall understanding report
- observation index
- candidate groups
- conflict and unresolved registries

Then expose these in both the review workspace and the developer workspace.

### Phase 4 - Stage 5B

Implement the low-resolution interpretation board:

- card generation
- highlight overlays
- board slices
- feedback actions

Then wire first-milestone approval and correction routing.

### Phase 5 - evaluation and milestone gate

Add the measurement loop for the first milestone:

- sampled benchmark packs
- scoring rubric
- reviewer checklist
- rerun logging
- decision records

Only after this should the project move to Stage 6 and beyond.

---

## 7. Technical Direction

Recommended practical stack for the first build:

- Python backend for the pipeline and orchestration workers
- TypeScript frontend for the review and developer workspaces
- shared artifact storage on filesystem for the first POC
- JSON artifacts plus schema validation for published contracts
- server-sent events or WebSocket stream for live pipeline status

This is enough to build the first milestone without overcommitting to production infrastructure too early.

---

## 8. API Key And Model Access Plan

One company OpenAI API key is enough to start the first milestone implementation.

Recommended rule for now:

- one OpenAI key for local development and first milestone execution
- store it in environment configuration, never in code or markdown artifacts
- make model choice configurable per stage or per task

You do not need multiple OpenAI keys just to begin.

You may want separate keys later for:

- local development versus hosted deployment
- cost tracking by environment or team
- separation between experiments and stable runs

You may also need non-OpenAI credentials later if the pipeline adopts:

- OCR providers
- cloud storage
- authentication
- queue or observability services

But for the immediate first build, one OpenAI key is sufficient.

---

## 9. Huge Prompt Strategy

The huge prompt should exist, but it should not be the first thing written.

If written too early, it will become a large unstable blob that drifts from the actual implementation.

Recommended approach:

1. use `MainPlan3.md`, the stage files, this execution plan, and the schema registry as the source documents
2. implement the first milestone with smaller prompt modules and explicit task templates
3. capture what actually works during execution
4. assemble the huge prompt from proven modules, policies, references, and artifact contracts

That makes the huge prompt an execution package built from tested decisions rather than an oversized speculative brief.

---

## 10. Missing Pieces That Should Be Planned Now

The current overall plan is strong, but these pieces should be made explicit before implementation moves too far:

- benchmark pack set for milestone evaluation
- scoring rubric for the 95 percent detailed-reading target
- prompt and model version registry
- model call logging and cost reporting
- artifact retention and naming policy
- rerun policy for narrow slices versus full runs
- correction taxonomy for first-milestone human feedback
- failure-state reporting in the developer console

These are not side issues.

They determine whether progress can actually be measured and debugged.

---

## 11. Immediate Decision Summary

The practical decisions for the next step should be:

1. yes, keep a dedicated markdown file for UI and execution alignment
2. yes, build a developer console, but as a second workspace in the same application rather than a separate product
3. keep the first implementation target limited to the first milestone around Stage 5A and Stage 5B
4. treat one company OpenAI API key as enough for the initial build
5. delay the huge prompt until the first milestone execution path is clearer

---

## 12. Next Build Target

The next concrete implementation target should be:

- define the app shell
- define the shared artifact API
- define the first review workspace screens
- define the first developer workspace screens
- define the minimum backend path from ingestion through Stage 5B

That is the right bridge from planning into execution.