# Vision-First Structural Drawing Interpretation Pipeline

---

## 0. Purpose Of This Second Plan

This document is the second top-level plan for the project.

It replaces the previous extraction emphasis with a new primary thesis:

> Recent vision models and agent workflows are now the main experimental focus.

The project is still building the same product category:

```text
Structural drawing pack
    -> AI extraction
    -> evidence-backed neutral structural schema
    -> browser 3D review model
    -> human approval / correction
    -> downstream export later
```

But the core question has changed.

The main thing being tested is no longer:

> how far classic PDF parsing and hand-written heuristics can carry the pipeline

The main thing being tested is now:

> how well a modern multimodal model, orchestrated as an agent, can read technical drawing packs, decide what matters, navigate across sheets, extract structural intent, preserve evidence, and support a reviewable structural scene graph.

This plan keeps the review-first architecture, evidence model, and staged outputs, but now formalizes a hybrid process:

```text
lightweight labeling
  -> GPT-5.5 pack interpretation
  -> deterministic PDF evidence extraction
  -> agentic synthesis into neutral model
  -> scene graph and browser review
```

---

## 1. Mission

Build a local, browser-based, AI-assisted drawing extraction and review system focused on structural steel warehouse drawing packs.

The first critical milestone remains the same:

> read a structural drawing pack and build a browser-reviewable 3D portal-frame model with traceable evidence and explicit unresolved issues

If portal-frame understanding is not credible, the broader platform should not be expanded.

---

## 2. New Core Thesis

The system should be designed around the capabilities of recent vision models and agent workflows.

### 2.1 What is being tested

We are testing whether a strong multimodal model can:

- read technical drawing pages directly
- visually classify sheets and regions
- identify schedules, plans, elevations, sections, notes, and title blocks
- connect information across sheets
- extract structural facts with evidence
- preserve ambiguity instead of silently guessing
- revisit the right region when the first pass is insufficient
- work as an agent rather than a one-shot parser

### 2.2 What is not the main experiment

We are not primarily testing:

- old-school PDF parsing as the main extraction engine
- broad regex-first routing as the core intelligence
- vector-only interpretation as the main path
- hand-built heuristics as the defining system behavior

Those things may still exist, but they become supporting infrastructure, fallback logic, QA inputs, and evidence sources.

They are no longer the star of the system.

---

## 3. Core Philosophy

### 3.1 Vision-first, not image-only

Technical PDFs are hybrid documents.

They often contain a mix of:

- rendered page imagery
- vector linework
- embedded text layers
- tables and schedules
- repeated symbols and callouts
- title block metadata
- rotated or derotated page content

So the correct principle is not:

> treat everything as dumb pixels only

The correct principle is:

> let the vision model read the page first, while also giving the system access to text, vectors, and PDF structure as supporting evidence when available

That means:

1. GPT-5.5 should read the document pages before downstream specialist extraction.
2. Page images and cropped regions are first-class inputs.
3. Text layer, vector data, and table structure are supporting channels, not the primary intelligence.
4. If PDF-native text or vectors are helpful, they should be exposed to the model or to the resolver as additional evidence.
5. If PDF-native structure conflicts with what the model sees, the conflict should be explicit.

### 3.2 The AI should extract observations, not fabricate final geometry

The model should produce:

- observations
- transcriptions
- classifications
- associations
- candidate identities
- topological relationships
- alternatives
- confidence
- evidence
- unresolved findings

The system should then resolve those observations into a neutral model.

### 3.3 Determinism has a narrower meaning now

The extraction layer is not fully deterministic if it depends on a vision model.

The deterministic part does not begin the moment the first model call finishes.

It begins only after the system has captured and organized two artifact layers:

1. vision-led interpretation artifacts
2. deterministic PDF evidence artifacts

So the architecture becomes:

```text
Lightweight sheet labels
  -> GPT-5.5 pack interpretation JSON
  -> deterministic PDF evidence JSON
  -> agentic synthesis into neutral model observations
  -> deterministic topology and geometry resolution
  -> scene graph and browser review model
```

The synthesis layer may still use model reasoning.

The deterministic geometry and topology layer begins only after the synthesis stage has committed a structured observation set.

This distinction must stay explicit in both code and UI.

### 3.4 Conflicts must come from evidence, not from artificial seeding

The system must not create fake conflict by mixing:

- mocked schedule rows
- heuristic defaults
- hand-seeded geometry
- model claims
- inferred facts that were never observed

If a fact is not observed or derived from a defined rule, it should be marked as assumed, seeded, schematic, or unresolved.

---

## 4. Product Goal Remains Review-First

The browser output is still the trust layer.

The user should be able to click any portal-frame object and understand:

- what it is
- which page(s) support it
- what the model actually saw
- what was transcribed from text or tables
- what was inferred across sheets
- what remains unresolved
- what is schematic rather than metric
- what the human overrode later

This remains a review system, not a CAD authoring tool.

---

## 5. Current Prototype Achievements To Preserve

The current codebase has already proven useful things and should not be discarded blindly.

### 5.1 What is already valuable

- local full-stack app structure
- project creation and PDF upload flow
- persisted project workspaces on disk
- PDF inspection with PyMuPDF
- page previews, title hints, and searchable page summaries
- a staged payload shape consumed by the frontend
- evidence objects, issue objects, and override storage
- 3D browser viewer for portal-frame review
- real portal-frame instance detection from repeated PF labels on S301
- real portal elevation slicing and support-column extraction from S401 vectors
- real support-mark assignment from elevation text near support columns

### 5.2 How to reinterpret those achievements

These should now be treated as:

- infrastructure for document access
- evidence channels
- fallback and QA helpers
- candidate generators
- viewer and review scaffolding

They should not define the future extraction architecture.

### 5.3 What should stop being the primary path

- heuristic-first sheet routing
- hardcoded schedule catalogue rows
- vector-only portal interpretation as the preferred intelligence path
- mixed seeded and observed facts presented as if equivalent

---

## 6. New Stack Direction

### 6.1 Backend

- Python
- FastAPI
- Pydantic
- local project workspace on disk
- SQLite or DuckDB for extraction records and observations
- background task runner for stage execution
- event streaming for stage progress
- PDF rendering service for page images and crops
- OpenAI API client targeting GPT-5.5

### 6.2 Frontend

- React
- TypeScript
- Vite
- Zustand or equivalent
- React Three Fiber / Three.js
- PDF page and crop viewer
- stage-by-stage extraction inspector
- evidence panel
- issues and overrides panel

### 6.3 AI integration

Use GPT-5.5 through the Responses API as the primary model for document reading, specialist extraction, and later synthesis support.

The system should:

- send page images and targeted crops
- include PDF text and metadata when helpful
- save response IDs and run metadata for every agent call
- save raw model responses
- save parsed JSON outputs
- save prompts used for each stage
- keep separate run histories for separate agents
- save which stored artifacts were retrieved and passed into each call
- save retry history and alternative outputs where relevant

---

## 7. New Source Priority Order

The previous plan leaned heavily toward vector-first extraction.

The new priority order should be:

1. GPT-5.5 reading the document page or crop directly
2. explicit drawing annotations, labels, schedules, callouts, dimensions, notes
3. cross-sheet consistency between the model's observations
4. PDF text layer and vector structure as supporting evidence
5. deterministic rule-based resolution from extracted facts
6. pixel or vector measurement only as low-confidence fallback

Important:

The model is allowed to use visible geometry cues, but it should not silently invent authoritative metric dimensions from appearance alone.

---

## 8. Main Process Overview

The project still benefits from staged outputs, but the high-level operating flow should now match the way the team wants to reason about the job.

```text
0. Project and document ingestion
1. Lightweight sheet classification and labeling
2. GPT-5.5 pack interpretation and initial structure JSON
3. Deterministic PDF evidence extraction and classification
4. Agentic synthesis into the neutral structural model
5. Scene graph and browser render model
6. Human review and iterative correction
7. Future export layer later
```

This is the product-facing process.

The detailed sections below unpack Steps 3 and 4 into internal specialist agents for schedules, plans, elevations, reference framework extraction, synthesis, QA, and resolution.

---

## 9. Stage 0 - Project And Document Ingestion

### Goal

Create a local project workspace, accept a folder of PDFs, copy them into backend-managed storage, and prepare the pages for vision-first reading.

### Inputs

- folder upload from the browser
- PDF documents

### Outputs

- project manifest
- source document index
- rendered page previews
- page-level metadata
- optional text-layer extraction
- optional vector metadata extraction

### Hard requirements

- accept folder upload via browser-compatible flow
- store original PDFs unchanged
- render a preview image for every page
- support crop rendering for later agent calls
- extract page rotation, page size, and page count
- extract PDF text layer when available
- extract vector metadata when available
- mark whether each page is vector-heavy, raster-heavy, text-heavy, or mixed

### Important rule

This stage does not interpret structure yet.

It prepares the document so GPT-5.5 can read it reliably.

------------------------------------------------

## 10. Stage 1 - Lightweight Classification And Labeling

### Goal

Perform a cheap and conservative first pass over the uploaded drawing pack so the system can label pages before deeper AI interpretation begins.

This stage exists to organize the pack, not to deeply understand it.

### Why it exists

A real pack may contain structural plans, schedules, notes, elevations, details, legends, architectural sheets, and noise.

Before the expensive model pass, the system should attach simple labels and routing hints such as:

- probable sheet family
- likely schedule-bearing pages
- likely plan pages
- likely elevation or section pages
- likely general notes or detail pages
- obvious low-priority pages for the first POC

### Inputs

- filenames
- page metadata
- low-resolution previews
- optional title block hints
- optional easy text-layer snippets

### Outputs

- preliminary page labels
- coarse sheet groups
- simple routing hints
- pages to send for higher-value GPT reading first
- pages that remain unknown

### Key rule

This stage must stay lightweight and cheap.

It should not be treated as the authoritative interpretation layer.

### Example responsibilities

- classify by filename, title hints, and obvious page cues
- separate likely structure sheets from obvious noise
- detect mixed pages that deserve richer follow-up later
- mark pages whose text, rotation, or layout suggests extra preprocessing

---

## 11. Stage 2 - GPT-5.5 Document Read Pass And Pack Interpretation

### Goal

Run GPT-5.5 over the drawing pack as images and produce the first broad interpretation of what the project is, what it contains, and what initial object structure should exist.

This is the first deep interpretation stage.

### Inputs

- lightweight labels and routing hints
- page images
- optional text layer
- filenames and metadata
- title block evidence where present

### Outputs

- document reading summary
- per-page AI reading notes
- page priority ranking
- candidate sheet types
- pack interpretation JSON
- initial structure inventory
- initial building-program summary
- initial unresolved questions
- initial schema skeleton that later stages can fill

### What this stage should decide

- what kind of project this appears to be
- what major built spaces or zones exist if visible in the pack
- what primary structural system is present
- what main element families likely exist
- which pages matter most for the primary structure
- which questions remain unresolved and need later evidence

### Important rule

This stage may use PDF text and vector clues, but the output is still an evidence-backed hypothesis, not final truth.

It should create a structured initial interpretation such as:

- building type
- major spaces or functional zones
- likely structural system
- candidate support count or frame count when the evidence supports it
- initial object categories to be filled later

---

## 12. Stage 3 - Deterministic PDF Evidence Extraction

### Goal

After the pack interpretation is saved, run a deterministic PDF-processing stage that extracts and classifies as much hard evidence as possible into organized JSON artifacts.

This stage should gather evidence, not decide the final model.

### Main evidence targets

The deterministic extractor should organize artifacts such as:

- page titles and title block fields
- schedule regions and row candidates
- text-layer captures and OCR support where needed
- dimensions and dimension strings
- grids, levels, RL markers, and axis labels when detectable
- vector layouts and structural linework candidates
- crop catalogs for later AI follow-up
- per-page evidence summaries

### Inputs

- pack interpretation JSON
- source PDFs
- page previews and crop rendering
- PDF text layer when available
- PDF vector data when available

### Outputs

- deterministic evidence bundle JSON
- per-page evidence manifests
- crop catalog
- schedule artifacts
- title and note artifacts
- dimension artifacts
- vector-layout artifacts
- unresolved extraction warnings

### Important rule

This stage is allowed to be incomplete.

If something cannot be parsed cleanly, the system should save the evidence region and mark it unresolved rather than inventing structure.

The next sections describe the most important internal evidence extractors for the POC.

---

## 13. Stage 3A - Schedule And Catalogue Evidence Extraction

### Goal

Extract schedule evidence and map marks to sections, roles, product codes, and notes wherever the PDF gives deterministic support.

### Deterministic evidence role

Schedules are not always clean machine-readable tables.

So this stage should do the deterministic work it can, including:

- region detection
- line and cell grouping where possible
- text extraction and normalization
- row candidate construction
- crop generation for ambiguous regions

### Supporting inputs

- schedule candidate regions
- page crop images
- optional PDF text layer
- optional table-line detection
- title block context

### Key rule

This step should produce organized schedule evidence JSON, not a forced final schedule truth.

If the schedule is visually readable but structurally messy, preserve the crop and the partial parse for later synthesis instead of emitting brittle fake precision.

---

## 14. Stage 3B - Portal Frame Elevation Evidence Extraction

### Goal

Extract portal-frame elevation evidence from the sheets into reusable artifacts that later stages can interpret.

### Evidence targets

For each frame type such as PF1, PF2, PF3, or PF4, this stage should capture whatever evidence can be extracted deterministically, including:

- frame identity labels
- local support positions
- vector-derived member geometry candidates
- rafter or beam callouts
- member marks and nearby section strings
- roof profile cues
- dimension strings and note strings
- unresolved geometry regions for targeted AI follow-up

### How this differs from the current implementation

The current prototype already extracts useful support geometry from S401 using vectors.

That logic should remain available and expand where possible, but it should now be framed as deterministic evidence production rather than the final interpretation itself.

### Supporting inputs

- page images and crop images
- vector layouts
- text near detected structural candidates
- title and viewport labels

### Key rule

The preferred path in this stage is:

> extract the elevation evidence deterministically, then let later synthesis and targeted AI follow-up interpret it

Vector support extraction remains valuable, but it is now a structured evidence source, a QA source, and a fallback source.

---

## 15. Stage 3C - Roof Framing Plan Evidence Extraction

### Goal

Extract deterministic roof-framing-plan evidence and candidate portal-frame occurrences in plan.

### POC focus

For now, this stage should focus on artifacts such as:

- PF labels in plan
- grid labels and axes
- candidate frame occurrence sequence
- dimension strings and spacing annotations
- vector bands and alignment cues
- nearby structural confirmation cues

### Existing achievement to reuse

The current code already finds repeated PF label occurrences on S301 and derives ordered frame instances.

That should remain as:

- candidate generation
- deterministic evidence for later synthesis
- visual QA
- fallback if the model misses a clear label

### New preferred behavior

This stage should not claim final placement truth by itself.

It should produce candidate instance artifacts, spacing cues, and alignment evidence that the synthesis stage can merge with the pack interpretation and schedule evidence.

---

## 16. Stage 4 - Agentic Synthesis And Neutral Model Construction

### Goal

Consume the organized JSON artifacts from Stages 2 and 3 and build the neutral structural model from the ground up.

This stage is agentic because it must retrieve the right stored evidence, reason iteratively, and construct the model the way a human would.

### Ground-up behavior

The synthesis agent should:

- retrieve only the relevant JSON artifacts and crops for the current question
- establish the usable coordinate system from plans, grids, levels, and dimensions
- decide whether the model is metric, partial, or topological at each area
- identify primary structural families and their naming scheme
- map schedule marks to physical elements
- place supports, members, bays, and repeated frames into space
- assign topology and connectivity
- retain alternatives and unresolved findings where evidence conflicts
- request targeted follow-up reads when the current evidence bundle is insufficient

### Important principle

This stage should use retrieval over stored JSON artifacts rather than one giant prompt containing the whole project state.

The neutral model should be built incrementally and explicitly.

After the synthesis stage commits a structured observation set, deterministic checks should:

- merge duplicates
- normalize IDs and names
- preserve evidence links
- apply consistency checks
- keep alternatives where needed
- separate unresolved items from resolved items

### Resolution levels

Use the same maturity ladder, but keep it explicit in data and UI:

1. semantic only
2. topological
3. schematic 3D
4. metric 3D
5. export-ready

The first milestone only needs Level 3 reliably, and Level 4 only where the evidence truly supports it.

---

## 17. Stage 5 - Scene Graph And Browser Render Model

### Goal

Produce the scene graph that will be read by Three.js and displayed in the browser with linked evidence.

This scene graph is the primary product output for the current milestone.

### Required contents

- named elements
- element type and role
- dimensions when resolved
- spatial placement
- connectivity and parent-child relationships where relevant
- evidence references
- confidence and unresolved markers
- distinction between schematic and metric geometry

### Required behavior

- render primary structural members as simple lines, proxies, or lightweight solids
- let the reviewer select members, supports, frames, and other structural objects
- display the reason each object exists
- expose source pages, crops, schedules, and notes
- make low-confidence and unresolved items obvious

### Important rule

The viewer must not collapse uncertainty.

If the system only knows an element topologically, the scene graph and the viewer should show that honestly.

---

## 18. Stage 6 - Human Review And Iterative Correction

### Goal

Keep human review separate from extraction while allowing iterative correction until the scene graph is trusted.

Overrides must not mutate raw observations.

The reviewed model should be:

```text
raw observations
  + resolution rules
  + human overrides
  = reviewed model
```

### Required actions

- approve
- reject
- needs clarification
- override section
- override frame type
- override placement
- override naming
- accept schematic geometry
- add note

### Review-loop rule

The reviewer may provide prompt-like feedback in natural language, but the system should translate that feedback into structured review actions, issue references, and override records.

The loop should then rerun only the necessary agent stages rather than the whole project by default.

---

## 19. Agent Architecture

The project should now be organized around explicit agent modules.

Minimum agents:

1. Ingestion Agent
2. Lightweight Classification Agent
3. GPT-5.5 Pack Interpretation Agent
4. Deterministic Evidence Builder
5. Schedule Evidence Extractor
6. Portal Frame Elevation Evidence Extractor
7. Roof Framing Plan Evidence Extractor
8. Synthesis Agent
9. Deterministic Resolver / QA Agent
10. Scene Graph Builder
11. Review Interpreter

Each agent must:

- accept typed inputs
- return typed outputs
- read and write stored artifacts rather than rely on hidden chat state
- save raw model response
- save parsed structured JSON
- save evidence references
- save unresolved findings
- save separate run history
- be rerunnable independently
- communicate with other agents through typed artifacts and issue references
- expose status in the UI

---

## 20. Canonical Data Principle

The project still needs a neutral evidence-backed schema.

The same separation remains mandatory:

### 20.1 Observation layer

What the model saw or transcribed.

Examples:

- page classification observation
- schedule row observation
- PF1 elevation template observation
- plan PF instance observation
- level marker observation

### 20.2 Resolved model layer

What the system believes after merging and resolving observations.

### 20.3 Review layer

What the human accepted, corrected, or rejected.

---

## 21. Evidence Requirements

Every important object should preserve:

- source file
- source page
- source crop or bbox
- source text if transcribed
- prompt / agent stage
- model output reference
- confidence
- alternatives if applicable

The model should never silently guess.

If something is ambiguous, it must remain ambiguous in the data.

---

## 22. Role Of PDF Structure In The New Plan

PDF-native structure is still useful.

But its role changes.

### 22.1 PDF structure should be used for

- preview rendering
- crop generation
- rotation correction
- searchable metadata
- optional text support
- optional vector support
- QA and alignment
- evidence enrichment

### 22.2 PDF structure should not be treated as

- the main intelligence layer
- the authoritative interpretation layer by default
- the only route to schedules or geometry

### 22.3 Hybrid technical-drawing rule

When a sheet clearly contains useful native text or vectors, use them.

But do not let the existence of those channels push the architecture back into an old parser-first system.

---

## 23. Recommended Near-Term Backend Shape

```text
/backend
  /app
    main.py
    config.py
    /api
      projects.py
      documents.py
      pipeline.py
      review.py
    /agents
      base.py
      document_read.py
      sheet_classifier.py
      reference_framework.py
      schedule_extractor.py
      portal_frame_elevation.py
      roof_framing_plan.py
      resolver.py
      qa.py
    /schemas
      documents.py
      evidence.py
      reference_framework.py
      catalogue.py
      portal_frames.py
      neutral_model.py
      review.py
    /services
      ai_client.py
      pdf_service.py
      preview_service.py
      crop_service.py
      storage_service.py
      pipeline_runner.py
```

---

## 24. Recommended Near-Term Frontend Shape

```text
/frontend
  /src
    App.tsx
    /components
      ProjectPicker.tsx
      DrawingIndex.tsx
      PipelineStepper.tsx
      PdfPageViewer.tsx
      EvidencePanel.tsx
      IssuesPanel.tsx
      JsonInspector.tsx
      ReviewControls.tsx
      ThreeModelViewer.tsx
    /stores
      projectStore.ts
      modelStore.ts
      reviewStore.ts
```

---

## 25. API Direction

Important new requirement:

The backend must connect to GPT-5.5 through the Responses API, support page-image and crop-based document reading as first-class pipeline actions, and preserve the artifact graph that lets agents retrieve each other's outputs.

Suggested endpoints:

```text
POST /api/projects
POST /api/projects/{project_id}/documents/upload-folder
GET  /api/projects/{project_id}/documents
GET  /api/projects/{project_id}/documents/{doc_id}/preview/{page}
GET  /api/projects/{project_id}/documents/{doc_id}/crop/{page}

POST /api/projects/{project_id}/pipeline/run
POST /api/projects/{project_id}/pipeline/run-step/{step_name}
GET  /api/projects/{project_id}/pipeline/status
GET  /api/projects/{project_id}/pipeline/events

GET  /api/projects/{project_id}/classifications/light
GET  /api/projects/{project_id}/interpretations/pack
GET  /api/projects/{project_id}/evidence/bundle
GET  /api/projects/{project_id}/evidence/reference-framework
GET  /api/projects/{project_id}/evidence/catalogue
GET  /api/projects/{project_id}/evidence/portal-frame-templates
GET  /api/projects/{project_id}/evidence/portal-frame-instances
GET  /api/projects/{project_id}/agents/runs

GET  /api/projects/{project_id}/models/resolved
GET  /api/projects/{project_id}/models/scene-graph
GET  /api/projects/{project_id}/models/browser-render

POST /api/projects/{project_id}/review/actions
GET  /api/projects/{project_id}/review/issues
GET  /api/projects/{project_id}/review/overrides
```

---

## 26. QA And Consistency Checks

The QA layer should verify:

- every portal frame instance references a known template
- every schedule-backed mark resolves cleanly or remains unresolved explicitly
- every model object has evidence
- every schematic coordinate is marked as schematic
- every low-confidence object appears in the issues panel
- every cross-sheet conflict is visible to the reviewer
- every unresolved page classification is listed

New QA principle:

conflicts must be evidence-derived, not introduced by inconsistent mocked assumptions.

---

## 27. Immediate Build Order Under The New Plan

Build in this order:

1. Preserve the existing local app, viewer, and evidence/override scaffolding.
2. Add robust page preview and crop services if not already sufficient.
3. Add lightweight sheet labeling and initial routing.
4. Implement a GPT-5.5 Responses API client and raw-response storage.
5. Add the pack-interpretation JSON stage as a real pipeline step.
6. Build the deterministic evidence bundle stage over titles, schedules, dimensions, vectors, and crops.
7. Keep the current specialized extractors, but reframe them as evidence producers and QA helpers.
8. Add the synthesis agent that retrieves stored JSON artifacts and builds the neutral model incrementally.
9. Refactor the resolver to consume artifact-backed observation records rather than mixed seeded facts.
10. Build the scene graph output and apply overrides back into the reviewed model rather than storing them only as side metadata.

---

## 28. Proof Of Concept Acceptance Criteria Under The New Plan

The first successful vision-first POC must:

1. let the user upload a folder of drawing PDFs
2. render and preview every page
3. attach lightweight labels to the pages before deep interpretation
4. run a GPT-5.5 pack-interpretation pass that produces a structured initial JSON
5. build a deterministic evidence bundle covering titles, schedules, dimensions, vector layouts, and crop references
6. synthesize a neutral structural model with named elements, dimensions where known, spatial placement, and connectivity
7. build a browser scene graph at least at schematic Level 3 for the primary structure
8. clearly label objects as schematic, partial, or metric
9. let the reviewer click any object and inspect its evidence
10. surface unresolved issues instead of hiding them
11. support iterative review feedback without mutating raw extraction history
12. store review actions and overrides separately from raw extraction

---

## 29. What To Avoid

Avoid these failure modes:

- calling the whole pipeline deterministic when the extraction step is model-driven
- drifting back into parser-first architecture because PDF text happens to exist
- mixing mocked and observed data in ways that create fake conflicts
- hiding ambiguity behind default geometry
- asking the model to emit final 3D geometry directly
- treating schematic coordinates as metric truth
- using vector extraction success on one sheet as proof that vision is unnecessary

---

## 30. Final Product Principle

The browser model is not the product by itself.

The product is:

> a trustworthy structural drawing interpretation system that combines vision-led understanding, deterministic evidence extraction, and agentic synthesis so a human can see what the model read, what it inferred, what it could not resolve, and why the 3D scene graph exists.

The most important design rule remains:

> the user should be able to click any 3D object and understand exactly why it exists

In this second plan, that explanation starts with GPT-5.5 reading the drawing pack, continues through deterministic evidence extraction, and ends in a reviewable scene graph.

---

## 31. Responses API, Artifact Retrieval, And Agent Communication

The project should explicitly standardize how agent runs are managed.

### 31.1 Responses API focus

- use the GPT-5.5 Responses API rather than ad hoc chat flows
- store each response ID, prompt, model settings, and parsed outputs
- treat each agent run as a first-class record tied to a project and stage

### 31.2 Artifact-first memory

Agents should not depend on long hidden chat histories as their main memory.

Instead, they should read and write:

- pack interpretation JSON
- deterministic evidence JSON
- crop references
- issue records
- resolved-model drafts
- review actions and overrides

### 31.3 Retrieval over JSON artifacts

When an agent needs context, it should retrieve the relevant stored JSON slices and evidence references rather than load the whole project into one prompt.

This is the correct place for project-level RAG behavior.

### 31.4 Inter-agent communication

Agents should communicate through typed artifacts, issue references, and rerunnable stage outputs.

They should not communicate by passing around informal free-text summaries as the source of truth.

---

## 32. Small Summary Of The Steps

1. Ingest the PDFs and prepare previews, crops, metadata, and storage.
2. Apply lightweight labels so the pack is roughly organized before deep interpretation.
3. Let GPT-5.5 read the pages as images and produce a pack-level interpretation JSON.
4. Run deterministic PDF extraction to build structured evidence JSON for schedules, titles, dimensions, vectors, and other artifacts.
5. Use an agentic synthesis stage to read those JSON artifacts, establish the coordinate framework, and build the neutral model from the ground up.
6. Output a scene graph with named elements, dimensions where known, placement in space, and connectivity.
7. Render that scene graph in Three.js with full evidence, uncertainty, and issue visibility.
8. Let a human review, correct, and iteratively rerun the necessary stages until the model is trusted.
