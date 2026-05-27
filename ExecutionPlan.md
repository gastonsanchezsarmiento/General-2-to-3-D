# Execution Plan

## 0. Purpose

This document is the main execution plan for the whole product.

Its job is to let a coding agent enter the repository, understand the product direction, understand the implementation order, understand the current milestone scope, and begin building without reopening settled planning questions.

This file is the top-level Codex-facing build brief.

It is not a replacement for the architectural and stage contracts.

Use it as the execution layer above those documents.

It is intentionally not self-contained.

The repository's markdown system is the real specification surface.

This file exists to control how that document system is consumed during implementation so Codex does not lose track, skip important constraints, or improvise where the repository already contains a defined answer.

---

## 1. Source Hierarchy

Use the project documents in this order.

### 1.1 Primary execution brief

- `ExecutionPlan.md`

This file defines:

- what should be built now
- what should not be built now
- how the implementation should be sequenced
- how the UI and developer surfaces fit into the product

### 1.2 Architecture source of truth

- `MainPlan3.md`

This file defines:

- the product goal
- the full workflow
- the stage boundaries
- the long-term architecture

If this file and `MainPlan3.md` ever conflict on architecture, follow `MainPlan3.md` and then update `ExecutionPlan.md`.

### 1.3 Stage contract source of truth

- `Stages/Orchestrator.md`
- `Stages/Stage - 0.md` through `Stages/Stage - 10.md` when present

These files define stage-level purpose, inputs, outputs, and guardrails.

### 1.4 Schema and artifact source of truth

- `Schemas/README.md`
- `Schemas/registry.json`
- schema files under `Schemas/`

These files define published cross-stage artifact contracts.

### 1.5 UI-specific supporting plan

- `UIExecutionPlan.md`

This file is narrower than `ExecutionPlan.md`.

It exists to guide the review UI and developer workspace implementation.

### 1.6 Research bridge and supporting references

- `ResearchNotes.md`
- the research files under `Resources/`
- `openai_vision_skills/`

These are supporting references, not the top-level execution authority.

### 1.7 Archived prompt drafts

- `Archive/HUGEPROMPT2.md`

Archived prompt drafts may be useful as structural inspiration, but they should not be followed blindly.

They were written against earlier plan assumptions.

### 1.8 Repository document system rule

The repository should be treated as a coordinated specification system.

That means:

- `ExecutionPlan.md` is the execution controller
- `MainPlan3.md` is the architecture contract
- `Stages/` contains the stage ownership contracts
- `Schemas/` contains the published artifact contracts
- `UIExecutionPlan.md` contains the UI and workspace growth plan
- `ResearchNotes.md` maps the research corpus to the current architecture
- `Resources/` and `openai_vision_skills/` contain implementation references and methodological constraints

These are not random notes.

They are the planned memory of the product.

Codex should treat the document set as the product specification, not as optional background reading.

### 1.9 Milestone 1 required source bundle

Before implementing milestone 1, Codex should read the following source bundle.

#### Control bundle

- `ExecutionPlan.md`
- `MainPlan3.md`
- `Stages/Orchestrator.md`
- `Schemas/README.md`
- `UIExecutionPlan.md`
- `ResearchNotes.md`

#### In-scope stage bundle

- `Stages/Stage - 0.md`
- `Stages/Stage - 1.md`
- `Stages/Stage - 2.md`
- `Stages/Stage - 3.md`
- `Stages/Stage - 4.md`
- `Stages/Stage - 5A.md`
- `Stages/Stage - 5B.md`

#### Method bundle

- `openai_vision_skills/README.md`
- `openai_vision_skills/skills/engineering-drawing-vision.md`
- `openai_vision_skills/skills/openai-model-calls.md`

#### Core milestone 1 research bundle

- `Resources/LLM Pipeline Run Management Design.md`
- `Resources/Sheet Classification and Extraction Pipeline.md`
- `Resources/PDF Vector and OCR Extraction Pipeline.md`
- `Resources/GPT-5.5 Structural Pack Interpretation JSON.md`
- `Resources/Deterministic Evidence Bundle for Drawings.md`
- `Resources/Agentic Synthesis Protocol Design.md`

Codex does not need to inline all of that material into this file.

It does need to treat those files as the deliberate input set for milestone 1 implementation.

### 1.10 Stage ownership and adjacency rule

When implementing any in-scope stage, Codex should not read only that stage file in isolation.

It should read:

- the owning stage file
- the orchestrator specification
- the immediate upstream stage contract
- the immediate downstream consumer contract when present
- the relevant schema or artifact contract for any published outputs

Examples:

- Stage 3 work should be implemented with Stage 2, Stage 3, Stage 4, Stage 5A, and the orchestrator in view
- Stage 5A work should be implemented with Stage 3, Stage 4, Stage 5A, Stage 5B, and the orchestrator in view
- Stage 5B work should be implemented with Stage 5A, Stage 5B, `UIExecutionPlan.md`, and the orchestrator in view

This rule exists so no stage is implemented as if it were isolated or free to invent its own contract.

### 1.11 Synchronization rule

When code changes affect behavior that is described in the document system, Codex should keep the owning documents synchronized.

At minimum:

- stage-behavior changes should update the owning stage file
- cross-stage artifact changes should update the relevant schema contract and registry entries when needed
- UI/workspace behavior changes should keep `UIExecutionPlan.md` aligned
- execution-order or milestone-scope changes should update `ExecutionPlan.md`

The goal is to keep the repository's specification network authoritative as implementation advances.

---

## 2. Product Definition

The product is a local, browser-based, AI-assisted structural drawing interpretation system.

It should:

1. ingest a drawing pack
2. understand what the pack contains
3. decide how the pack should be read
4. gather evidence through coordinated AI reading and support extraction
5. organize that evidence into a coherent interpretation package
6. expose that interpretation for human review
7. later synthesize, verify, publish, and review a richer structural model

The product is not:

- a generic PDF chatbot
- a blind OCR dump viewer
- a direct PDF-to-Revit converter
- a first-build 3D modeling tool

The product should remain evidence-linked, artifact-backed, and explicit about uncertainty.

---

## 3. Core Operating Principles

The following rules are non-negotiable.

### 3.1 GPT-5.5 is the main orchestrated reasoning layer

The system is agent-orchestrated.

The orchestrator controls the flow from run start, not only later planning stages.

### 3.2 Vision is the primary reading tool

Vision should be the default reading mode for the pack.

PDF-native text, OCR, and vector support are auxiliary tools selected when useful.

### 3.3 Artifacts are the main system memory

Important state must live in the shared artifact space.

The system should not depend on hidden chat continuity for core workflow state.

### 3.4 Evidence and uncertainty must remain explicit

The product must not silently upgrade guesses into facts.

The product must preserve evidence links, conflict state, unresolved state, and inference status.

### 3.5 Early milestones stop before the later model pipeline

The first implementation milestone ends at Stage 5A and Stage 5B.

Do not pull Stage 6, Stage 7, Stage 8, Stage 8A, or Stage 10 into milestone 1 unless a small scaffold is needed for code organization only.

### 3.6 One product, two workspaces

The user-facing review surface and the developer debugging surface should be one application with shared backend APIs and shared run state.

Do not build two disconnected products.

---

## 4. Product Surfaces

The product should be built as one application with two main workspaces.

### 4.1 Review workspace

The review workspace is for judging AI interpretation quality.

Its first milestone job is to let the user:

- create or open a project
- upload a drawing pack
- run interpretation
- see broad pack understanding
- inspect page-level understanding
- inspect evidence-linked Stage 5A package outputs
- inspect the Stage 5B visual interpretation board
- approve the first milestone or request correction

### 4.2 Developer workspace

The developer workspace is for internal visibility and debugging.

Its first milestone job is to let the user:

- see current run state
- see current stage state
- inspect prompts, model calls, and tool choices
- inspect raw artifacts and manifests
- inspect logs and failures
- rerun narrow slices when needed

---

## 5. Project Model

For milestone 1, use a simple project model.

Recommended rule:

- one project represents one uploaded drawing pack
- one project may have multiple runs and reruns
- different file sets should normally be different projects

Do not build complex multi-pack merging in milestone 1.

The minimum project flow should be:

1. create project
2. upload PDFs
3. start interpretation run
4. watch progress in the review and developer workspaces
5. inspect Stage 5A and Stage 5B outputs
6. record approval or correction

---

## 6. Full Stage Map

The full product architecture remains the MainPlan3 stage flow.

### Stage 0

Ingestion and page preparation.

### Stage 1

Whole-pack reconnaissance.

### Stage 2

Orchestrator read-plan generation.

### Stage 3

Targeted AI reading.

### Stage 4

Optional support extraction.

### Stage 5A

Coherent observation packaging.

### Stage 5B

Low-resolution visual interpretation feedback board.

### Stage 6

Neutral-model synthesis.

### Stage 7

Verification.

### Stage 8

Scene graph generation.

### Stage 8A

Detailed Three.js review model.

### Stage 10

Structured human review of the browser model.

Milestone 1 stops after Stage 5B and the first human decision.

---

## 7. Milestone Plan

The product should be built in milestones.

### Milestone 1

Goal:

Build a usable application that accepts a drawing pack and, after a run, shows the AI's first coherent interpretation of the documents through Stage 5A and Stage 5B.

Milestone 1 includes:

- project creation
- PDF upload
- run creation
- Stage 0 through Stage 5B execution
- review workspace for interpretation review
- developer workspace for internal visibility
- first-milestone approval or correction capture

Milestone 1 does not include:

- neutral-model synthesis
- verification loop
- browser scene graph
- richer Three.js model
- final human review loop for model correction

### Milestone 2

Stage 6 and Stage 7.

### Milestone 3

Stage 8 and Stage 8A.

### Milestone 4

Stage 10 and later export-oriented preparation.

---

## 8. Milestone 1 Exact Outcome

At the end of milestone 1, the user should be able to:

1. open the application
2. create a project
3. upload a set of structural drawing PDFs
4. start an interpretation run
5. watch the run progress
6. open a review workspace that shows what the AI thinks the uploaded pack contains
7. inspect evidence-linked Stage 5A package outputs
8. inspect the Stage 5B interpretation board
9. approve the first milestone or request correction
10. open the developer workspace and inspect what happened internally

The user should not need to wait for Stage 6 or a 3D model to get value from milestone 1.

---

## 9. Milestone 1 Functional Requirements

### 9.1 Project creation

The application must support:

- create project
- list existing projects
- open project
- show project runs

### 9.2 Upload and ingestion

The application must support:

- upload one or more PDFs into the project
- create a run linked to that upload set
- store source files unchanged
- render page images for reading
- create base manifests and indexes

### 9.3 Pipeline execution

The backend must support:

- Stage 0
- Stage 1
- Stage 2
- Stage 3
- Stage 4 when useful
- Stage 5A
- Stage 5B

The orchestrator must control those steps and persist routing state in artifacts.

### 9.4 Review workspace outputs

The review workspace must show:

- project header
- run selector
- pack summary
- page gallery
- page detail view
- Stage 5A package summary
- Stage 5A candidate groups
- Stage 5A unresolved and conflict views
- Stage 5B interpretation board
- human decision panel

### 9.5 Developer workspace outputs

The developer workspace must show:

- run timeline
- stage status
- queue or worker state
- logs
- model call journal
- raw artifact browser
- prompt version references
- cost and latency summary when available

### 9.6 Human decision capture

The application must let the user record:

- approved
- needs correction
- rerun requested
- notes linked to the milestone decision

Those decisions must be written into artifacts that the orchestrator can read.

---

## 10. Milestone 1 UX Definition

Milestone 1 should keep the UX narrow and useful.

### 10.1 Review workspace screens

Recommended first screens:

- projects list
- project detail
- run detail
- page inspector
- Stage 5A interpretation summary view
- Stage 5B board view

### 10.2 Review workspace interaction rules

The user should be able to:

- click a page and inspect its role and main findings
- click a Stage 5A candidate group and inspect evidence
- click a Stage 5B card and jump to the related page or crop
- filter conflicts and unresolved items
- record first-milestone feedback

### 10.3 Developer workspace screens

Recommended first screens:

- runs dashboard
- run event timeline
- stage detail panel
- artifact inspector
- model call inspector
- logs and errors panel

### 10.4 UX design rule

Do not treat milestone 1 as a final design pass.

Build a clear, inspectable interface that can grow with later stages.

---

## 11. Milestone 1 Technical Direction

Use a simple, pragmatic stack for the first build.

### 11.1 Backend

Recommended backend stack:

- Python 3.11+
- FastAPI for the HTTP API
- Pydantic for typed contracts
- OpenAI Responses API client for model calls
- filesystem artifact store for run outputs
- SQLite for lightweight run and project indexing when useful
- server-sent events or WebSockets for live run status

### 11.2 Frontend

Recommended frontend stack:

- TypeScript
- React
- Vite
- a lightweight state and data-fetching layer appropriate for a local app

Milestone 1 does not need Three.js.

### 11.3 Document processing support

Recommended support tooling:

- PDF rendering library for page previews
- image crop generation support
- OCR or text-layer helpers only where needed
- optional vector extraction support where useful

### 11.4 Persistence model

The system should persist:

- project metadata
- run metadata
- stage status
- artifacts and manifests
- logs
- model call summaries
- milestone decisions

---

## 12. Shared Artifact Rules

The system must follow the existing artifact-first architecture.

Key rules:

- important stage state must be written to artifacts
- published cross-stage artifacts must include `schema_id` and `schema_version`
- stage-local scratch data may stay local until it becomes published shared state
- Stage 5B helper payloads may remain stage-local for now
- orchestrator state must remain inspectable

Codex should follow `Schemas/README.md` and `Schemas/registry.json` when writing published shared artifacts.

---

## 13. Model And API Plan

### 13.1 API key assumption

For milestone 1, assume one company OpenAI API key is enough.

Use environment configuration for secrets.

Do not store secrets in source code or markdown files.

### 13.2 Model usage strategy

Model choice should remain configurable by task.

At minimum, milestone 1 should support:

- one model for broad reconnaissance
- one model for targeted detailed reading
- one model for packaging or explanation tasks if needed

Even if the same model is used for all three at first, keep the configuration boundary explicit.

### 13.3 Prompt strategy

Do not start by writing one giant unstable prompt blob.

Milestone 1 should use smaller prompt modules tied to stages and tasks.

Examples:

- Stage 1 reconnaissance prompt template
- Stage 3 targeted reading prompt template
- Stage 5A packaging prompt template
- Stage 5B board-building prompt template

The larger master prompt can later be assembled from proven prompt modules, stage rules, and artifact contracts.

---

## 14. Milestone 1 Implementation Order

When implementing milestone 1, build in this order.

Before Phase 0, read the milestone 1 source bundle defined in Section 1.9.

### Phase 0

Foundation:

- repository structure
- configuration loading
- secrets loading
- artifact store
- run and project IDs
- basic schema validation helpers

### Phase 1

Application shell:

- backend API skeleton
- frontend shell
- review workspace route
- developer workspace route
- live run status channel

### Phase 2

Project and run management:

- create project
- upload PDFs
- create run
- persist metadata
- show project and run lists

### Phase 3

Stage 0 and Stage 1:

- page rendering
- manifests
- broad pack understanding
- review display of page and pack summary

### Phase 4

Stage 2 and Stage 3:

- read-plan generation
- targeted read execution
- evidence capture
- developer visibility into stage routing

### Phase 5

Stage 4 when useful:

- support extraction integration
- optional text or vector evidence support

### Phase 6

Stage 5A:

- coherent observation package
- package summary
- candidate groups
- unresolved and conflict registries

### Phase 7

Stage 5B:

- board slice selection
- cards and highlights
- reviewable visual interpretation board
- feedback artifact writing

### Phase 8

Milestone decision loop:

- approval and correction capture
- orchestrator recording
- rerun entry points

Do not move past Phase 8 until the first milestone is usable.

---

## 15. Acceptance Criteria For Milestone 1

Milestone 1 is complete only when all of the following are true.

### 15.1 Product behavior

- a project can be created
- PDFs can be uploaded
- a run can be started
- the run executes through Stage 5A and Stage 5B
- the review workspace shows the AI interpretation of the uploaded drawings
- the developer workspace shows internal execution state

### 15.2 Data behavior

- artifacts are persisted to disk
- stage outputs are inspectable
- published cross-stage artifacts follow the current schema rules
- important state is not hidden only in in-memory process state

### 15.3 Review behavior

- the user can inspect page-level understanding
- the user can inspect evidence-linked package outputs
- the user can inspect the visual interpretation board
- the user can record approval or correction

### 15.4 Debuggability

- failures are visible in the developer workspace
- model calls and stage progression are inspectable
- reruns can be initiated without deleting the project

---

## 16. Explicit Out-Of-Scope For Milestone 1

Do not treat these as milestone 1 requirements:

- Stage 6 neutral-model synthesis
- Stage 7 verification automation
- Stage 8 scene graph publication
- Stage 8A Three.js review model
- Stage 10 full browser correction loop
- BIM export
- Revit integration
- advanced production infrastructure
- multi-user collaboration
- cloud deployment hardening

Scaffolding for future growth is acceptable.

Implementing later-stage features now is not.

---

## 17. Missing Planning Items That Must Be Addressed During Build

The plan is solid enough to begin milestone 1, but these items must be made concrete during implementation rather than ignored.

- benchmark pack selection
- detailed scoring rubric for reading quality
- prompt version tracking
- model call logging structure
- artifact naming and retention policy
- rerun policy for narrow slices
- correction taxonomy for first-milestone feedback
- cost reporting in the developer workspace

These should be implemented as explicit structures, not left as informal ideas.

---

## 18. Codex Execution Rule

When a future coding conversation says:

`Implement milestone 1 of ExecutionPlan.md`

the coding agent should assume:

- the milestone scope is already approved
- the correct target is Stage 0 through Stage 5B plus the review and developer workspaces
- the implementation should begin directly without reopening major planning questions
- this file is an entry point into a deliberate document system rather than a self-contained replacement for that system
- the agent should read the milestone 1 source bundle defined in Section 1.9 before coding
- the agent should follow the stage ownership and adjacency rule defined in Section 1.10 while implementing each slice
- the agent should keep the specification network synchronized under the rule defined in Section 1.11 when implementation changes the documented behavior

The agent should still surface genuine blockers such as missing dependencies, broken environment assumptions, or contradictory repository state.

It should not reopen settled scope questions that this document already answers.

---

## 19. Relationship To UIExecutionPlan.md

`UIExecutionPlan.md` should be kept.

It is useful, but it is not the whole-product execution plan.

Its role is to define the UI and workspace growth path inside the broader execution plan defined here.

Use it as a supporting plan during UI work.

Use this file as the main Codex execution brief.