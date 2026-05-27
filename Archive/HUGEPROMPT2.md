# Master Execution Prompt For The Vision-First Structural Review Pipeline

You are a very powerful llm programming model working inside this repository through github copilot.

This file is the new master execution brief for the product defined in [MainPlan2.md](MainPlan2.md).

Use this document before you change architecture, write code, create schemas, define prompts, or add pipeline stages.

Treat this file as a build brief, not as a brainstorming document.

If this file conflicts with [HUGEPROMPT.md](HUGEPROMPT.md), follow this file for architecture and stage behavior.

Use [MainPlan2.md](MainPlan2.md) as the product-truth companion.
Use [HUGEPROMPT.md](HUGEPROMPT.md) only as a structural example for how detailed a master prompt should be.
Use [copilot-instructions.md](copilot-instructions.md) as the repository routing guide for what to adapt, what to ignore, and what is already archived.
Do not use anything in [Resources/archive](Resources/archive) as part of the core source set unless a very specific blocker forces consultation later.

---

## 1. What The Product Is

The product is a local, browser-based, AI-assisted structural drawing interpretation and review system for structural steel warehouse drawing packs.

The product reads a folder of PDF drawings, organizes the pack, interprets the pack with GPT-5.5, extracts deterministic evidence from the PDF itself, synthesizes those artifacts into a neutral structural model, renders a browser-reviewable scene graph, and lets a human review or correct the result without destroying the original extraction history.

The product is not a generic document chatbot.
The product is not a direct PDF-to-Revit converter.
The product is not a fabrication-detail modeler.
The product is not a compliance-checking engine.
The product is not a CAD editor.

The product is a trustworthy structural interpretation pipeline whose main output is:

1. a traceable understanding of the drawing pack
2. a neutral structural model built from evidence
3. a browser scene graph for review
4. a review and override layer that preserves uncertainty and lineage

### 1.1 Product Inputs

The runtime product accepts these primary inputs:

- a folder of structural drawing PDFs
- project-level metadata if available
- an optional intake hint for the first GPT-5.5 vision pass
- reviewer actions and override feedback after the first run

The product may also use these supporting inputs when available:

- PDF text layer
- PDF vector objects
- rendered page previews
- rendered page crops
- title block hints
- low-authority user hints about expected scope, likely missing sheets, or immediate review priority
- stored artifacts from earlier runs

### 1.2 Product Outputs

The runtime product must produce these first-class outputs:

- project manifest
- document and page index
- lightweight page labels and routing hints
- pack interpretation JSON
- pack coverage assessment and proceed recommendation
- interpretation evidence and interpretation manifest artifacts
- deterministic evidence bundle JSON
- neutral model observations
- resolved structural model
- scene graph JSON for browser review
- issue register
- review actions and overrides
- run records and artifact lineage

### 1.3 Current Milestone

The first milestone is still the portal-frame proof of concept.

The system must be able to read a structural drawing pack and build a browser-reviewable portal-frame model with:

- named elements
- evidence links
- explicit unresolved items
- honest maturity labels such as semantic, topological, schematic, or metric

If the system cannot do that credibly for the primary structure, do not expand into wider scope.

### 1.4 What The Product Is Not Allowed To Pretend

The product must never pretend that:

- a vision guess is final truth
- a schematic placement is metric truth
- an extracted text string is a resolved model object by itself
- a reviewer override has replaced the raw evidence
- a missing coordinate is acceptable if a plausible coordinate can be guessed

---

## 2. How The Product Works Very Specifically

The runtime flow must follow this exact product-facing order:

```text
1. PDF ingestion
2. Lightweight sheet classification and labeling
3. GPT-5.5 image-based pack interpretation and initial JSON
4. Deterministic PDF evidence extraction and evidence JSON
5. Agentic synthesis into the neutral model from the ground up
6. Scene graph output for Three.js and browser review
7. Human review, structured overrides, and targeted reruns
8. Future export layer later, not now
```

The rest of this section explains exactly what each runtime stage does, what goes in, what comes out, and what the stage is not allowed to claim.

### 2.1 Stage 1 - PDF Ingestion

#### Goal

Create a managed project workspace, copy the original PDFs into storage unchanged, render the pages for AI reading, and produce the base document inventory for the rest of the pipeline.

#### Runtime Inputs

- uploaded folder of PDFs
- optional project name or project code

#### Runtime Processing

- create a stable project ID
- copy source PDFs into project storage without mutation
- register document IDs and page IDs
- render page previews
- record page size, page count, rotation, and document metadata
- extract text layer if present
- extract vector metadata if present
- support later crop rendering for page regions

#### Runtime Outputs

- `project.json`
- `documents/index.json`
- `documents/pages.json`
- rendered preview images
- crop rendering capability
- optional text and vector side artifacts

#### Example Output Shape

```json
{
  "project_id": "PROJ_B9BE6D2C",
  "documents": [
    {
      "document_id": "DOC_0001",
      "filename": "warehouse-pack.pdf",
      "pages": [
        {
          "page_id": "PAGE_0001",
          "page_number": 1,
          "rotation": 0,
          "width": 841,
          "height": 594,
          "preview_path": "documents/previews/PAGE_0001.png",
          "text_layer_available": true,
          "vector_layer_available": true
        }
      ]
    }
  ]
}
```

#### This Stage Is Allowed To Claim

- what files and pages exist
- how the pages were rendered
- what basic metadata exists
- whether text or vector support is available

#### This Stage Is Not Allowed To Claim

- what structural system exists
- what sheet type a page is
- what members or frames exist

#### Primary Research Links

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### 2.2 Stage 2 - Lightweight Sheet Classification And Labeling

#### Goal

Perform a cheap first-pass organization of the pack so later stages know which pages are likely schedules, plans, elevations, details, notes, or low-priority noise.

#### Runtime Inputs

- page previews
- filenames
- page metadata
- easy title block hints if available
- optional short text snippets

#### Runtime Processing

- assign coarse page labels
- group likely page families
- rank pages by likely value to later stages
- identify pages that may need special preprocessing
- leave uncertain pages as uncertain instead of forcing a label

#### Runtime Outputs

- `classification/page_labels.json`
- `classification/page_groups.json`
- `classification/routing_hints.json`
- unknown-page queue

#### Example Output Shape

```json
{
  "page_id": "PAGE_0012",
  "coarse_label": "roof_plan_candidate",
  "confidence": 0.78,
  "routing_hints": ["send_to_pack_interpretation", "look_for_pf_labels"],
  "status": "provisional"
}
```

#### This Stage Is Allowed To Claim

- likely page family
- likely routing priority
- need for follow-up

#### This Stage Is Not Allowed To Claim

- final page truth when evidence is weak
- final structural element identity
- schedule values or geometry

#### Primary Research Links

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/GPT-5.5 Structural Pack Interpretation JSON.md](Resources/HUGEPROMPT2/GPT-5.5%20Structural%20Pack%20Interpretation%20JSON.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### 2.3 Stage 3 - GPT-5.5 Pack Interpretation And Initial Structure JSON

#### Goal

Use GPT-5.5 to read the drawing pack as images and produce the first structured hypothesis about what the project is, which pages matter, what structural systems likely exist, what major object families exist, and what questions remain unresolved.

#### Runtime Inputs

- page images
- coarse labels and routing hints
- filenames and metadata
- optional text support
- optional title block evidence
- optional `intake_hint.json` carrying low-authority user hints

#### Runtime Processing

- read the pack visually
- create a page atlas with page roles and importance
- produce pack-level interpretation fields
- identify candidate structural systems and object families
- identify unresolved questions and conflict candidates
- perform a soft coverage check for likely missing or insufficient sheet families
- produce a structured proceed recommendation instead of a hidden internal judgment
- produce evidence anchors and a manifest that later agents can retrieve without guessing the output shape
- seed later deterministic extraction with targets and priorities

#### Runtime Outputs

- `pack_interpretation/pack_interpretation.json`
- `pack_interpretation/page_atlas.json`
- `pack_interpretation/coverage_assessment.json`
- `pack_interpretation/interpretation_evidence.json`
- `pack_interpretation/interpretation_manifest.json`
- `pack_interpretation/operator_update.json`
- `pack_interpretation/unresolved_questions.json`
- stored raw model response and parsed response

#### Example Output Shape

```json
{
  "project_id": "PROJ_B9BE6D2C",
  "primary_building_type": "steel warehouse",
  "candidate_structural_systems": [
    {
      "system_type": "portal_frame",
      "confidence": 0.91,
      "evidence_pages": ["PAGE_0012", "PAGE_0024"]
    }
  ],
  "major_element_families": ["frames", "columns", "rafters", "purlins"],
  "priority_pages": ["PAGE_0012", "PAGE_0019", "PAGE_0024"],
  "coverage_assessment": {
    "status": "proceed_with_partial_confidence",
    "suspected_missing_sheet_families": ["member_schedule"],
    "confidence": 0.61,
    "reason": "Plan and elevation evidence appear present, but a high-confidence primary member schedule is not yet confirmed.",
    "proceed_recommendation": "continue"
  },
  "operator_update": {
    "message": "This pack looks workable for an initial pass. Continuing with partial confidence.",
    "tone": "friendly_status"
  },
  "unresolved_questions": [
    {
      "issue_id": "ISSUE_0001",
      "kind": "missing_information",
      "question": "Are PF2 and PF3 distinct frame templates or revisions of the same template?"
    }
  ]
}
```

#### This Stage Is Allowed To Claim

- building type and broad building intent when evidence supports it
- candidate structural systems
- likely major element families
- page priority and page-role hypotheses
- a soft recommendation about whether the pack appears sufficient to continue
- suspected missing or weakly represented sheet families when evidence suggests that risk
- unresolved questions for later stages

#### This Stage Is Not Allowed To Claim

- final geometry
- exact section sizes without deterministic support
- exact quantities from visual appearance alone
- compliance or design adequacy conclusions
- a hard global judgment that the project is impossible to process based only on this first pass

#### Important Rule

The optional intake hint may help the model prioritize attention, but it is not evidence.

The operator-facing update may be friendly in tone, but the pipeline must rely on the structured `coverage_assessment` fields rather than free text.

#### Primary Research Links

- [Resources/HUGEPROMPT2/GPT-5.5 Structural Pack Interpretation JSON.md](Resources/HUGEPROMPT2/GPT-5.5%20Structural%20Pack%20Interpretation%20JSON.md)
- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)
- [Resources/Structural Plan Interpretation Research - 5.md](Resources/Structural%20Plan%20Interpretation%20Research%20-%205.md)
- [Resources/Structural Elevation Resolution Research - Step 6.md](Resources/Structural%20Elevation%20Resolution%20Research%20-%20Step%206.md)

### 2.4 Stage 4 - Deterministic PDF Evidence Extraction And Evidence JSON

#### Goal

Extract deterministic evidence from the PDFs after Stage 3 has already formed an initial interpretation.

This stage collects hard evidence into typed artifacts.
It does not decide the final model.

#### Runtime Inputs

- source PDFs
- page previews and crops
- pack interpretation JSON
- text layer if present
- vector data if present

#### Runtime Processing

- create a bundle manifest
- normalize text and units while preserving raw strings
- record page-level artifacts
- record region-level artifacts
- detect and store schedule candidates
- detect and store grid, level, RL, dimension, and note artifacts
- detect and store vector-layout artifacts
- preserve unresolved regions as first-class artifacts

#### Runtime Outputs

- `evidence_bundle/manifest.json`
- `evidence_bundle/retrieval_index.json`
- `evidence_bundle/pages/*.json`
- `evidence_bundle/crops/*.json`
- `evidence_bundle/schedules/*.json`
- `evidence_bundle/reference/*.json`
- `evidence_bundle/dimensions/*.json`
- `evidence_bundle/vectors/*.json`
- `evidence_bundle/unresolved_regions.json`

#### Example Output Shape

```json
{
  "artifact_id": "ART_EVIDENCE_BUNDLE_0001",
  "project_id": "PROJ_B9BE6D2C",
  "pages": ["PAGE_0012", "PAGE_0019", "PAGE_0024"],
  "artifact_families": [
    "page_artifacts",
    "crop_catalog",
    "schedule_artifacts",
    "dimension_artifacts",
    "vector_artifacts",
    "unresolved_region_artifacts"
  ],
  "status": "completed"
}
```

#### Internal Stage 4 Workers

The deterministic stage should internally split into specialist evidence workers such as:

- schedule and catalogue evidence extraction
- reference framework extraction for grids, levels, RLs, and dimensions
- roof plan evidence extraction
- portal frame elevation evidence extraction
- note and callout extraction
- unresolved region capture

#### This Stage Is Allowed To Claim

- what evidence was extracted
- how it was extracted
- how reliable the extraction appears
- what remains unresolved

#### This Stage Is Not Allowed To Claim

- the final resolved structural model
- the final meaning of every ambiguous crop
- exact 3D placement simply because a vector segment exists

#### Primary Research Links

- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/Structural Drawing Reference Framework Research - Step 3.md](Resources/Structural%20Drawing%20Reference%20Framework%20Research%20-%20Step%203.md)
- [Resources/AI for Australian Steel Schedule Extraction - Step 4.md](Resources/AI%20for%20Australian%20Steel%20Schedule%20Extraction%20-%20Step%204.md)
- [Resources/Structural Plan Interpretation Research - 5.md](Resources/Structural%20Plan%20Interpretation%20Research%20-%205.md)
- [Resources/Structural Elevation Resolution Research - Step 6.md](Resources/Structural%20Elevation%20Resolution%20Research%20-%20Step%206.md)

### 2.5 Stage 5 - Agentic Synthesis Into The Neutral Model

#### Goal

Read the stored Stage 3 and Stage 4 artifacts and construct the neutral structural model from the ground up.

This is the hardest stage.
It must act like a disciplined agent, not like a one-shot answer generator.

#### Runtime Inputs

- pack interpretation JSON
- deterministic evidence bundle JSON
- artifact registry lookup
- prior unresolved issue records
- targeted page or crop follow-up reads when needed

#### Runtime Processing

- plan the next synthesis question
- retrieve only the relevant artifacts
- establish the coordinate bootstrap from grids, levels, RLs, and dimensions
- map schedule marks to physical elements
- infer object identity and topology from evidence
- create neutral-model observations
- create resolved objects where evidence supports resolution
- create alternatives or unresolved records where evidence conflicts
- rerun targeted follow-up reads when a specific local question remains open

#### Runtime Outputs

- `neutral_model/observations.json`
- `neutral_model/resolved_model.json`
- `neutral_model/conflicts.json`
- `neutral_model/unresolved.json`
- `neutral_model/identity_lineage.json`

#### Example Output Shape

```json
{
  "object_id": "OBJ_FRAME_PF2_GRID_B_01",
  "object_type": "portal_frame_instance",
  "maturity": "schematic_3d",
  "evidence_ids": ["EV_0211", "EV_0319", "EV_0442"],
  "supporting_observations": ["OBS_0021", "OBS_0094"],
  "status": "resolved_with_open_questions",
  "open_questions": ["ISSUE_0007"]
}
```

#### This Stage Is Allowed To Claim

- resolved neutral objects when evidence supports them
- local topology and object relationships
- schematic or metric placement when supported
- explicit conflicts and alternative hypotheses

#### This Stage Is Not Allowed To Claim

- a resolved object with no evidence links
- a coordinate system that was never established
- silent conflict collapse
- direct final export semantics for downstream BIM tools

#### Primary Research Links

- [Resources/HUGEPROMPT2/Agentic Synthesis Protocol Design.md](Resources/HUGEPROMPT2/Agentic%20Synthesis%20Protocol%20Design.md)
- [Resources/HUGEPROMPT2/Pipeline Object Identity and Naming.md](Resources/HUGEPROMPT2/Pipeline%20Object%20Identity%20and%20Naming.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)
- [Resources/Geometry Solver Research for Structural Drawings - Step 8.md](Resources/Geometry%20Solver%20Research%20for%20Structural%20Drawings%20-%20Step%208.md)

### 2.6 Stage 6 - Scene Graph Output For Browser Review

#### Goal

Transform the neutral model into a browser-ready scene graph that can be rendered in Three.js and inspected by a reviewer.

#### Runtime Inputs

- resolved model
- unresolved and conflict records
- evidence references
- geometry payloads or centerline proxies

#### Runtime Processing

- map resolved objects into scene nodes
- preserve evidence and issue links on scene nodes
- keep uncertainty visible
- separate structural graph data from heavier geometry payloads
- mark each object as semantic, topological, schematic, or metric

#### Runtime Outputs

- `scene_graph/scene_graph.json`
- `scene_graph/geometry_payloads/*.json`
- `scene_graph/viewpoints.json`
- `scene_graph/filter_indexes.json`

#### Example Output Shape

```json
{
  "scene_node_id": "SCN_0001",
  "object_id": "OBJ_FRAME_PF2_GRID_B_01",
  "node_type": "portal_frame_instance",
  "maturity": "schematic_3d",
  "geometry_kind": "centerline_proxy",
  "evidence_ids": ["EV_0211", "EV_0319"],
  "issue_ids": ["ISSUE_0007"]
}
```

#### This Stage Is Allowed To Claim

- how the resolved model should be visualized
- which nodes are reviewable
- which geometry is semantic, topological, schematic, or metric

#### This Stage Is Not Allowed To Claim

- certainty that does not exist upstream
- fabrication-ready detail that the neutral model never resolved
- removal of issues just because a node can be drawn

#### Primary Research Links

- [Resources/HUGEPROMPT2/Scene Graph Contract for Browser Review.md](Resources/HUGEPROMPT2/Scene%20Graph%20Contract%20for%20Browser%20Review.md)
- [Resources/AI Structural Model Review Pipeline - Step 9.md](Resources/AI%20Structural%20Model%20Review%20Pipeline%20-%20Step%209.md)
- [Resources/Geometry Solver Research for Structural Drawings - Step 8.md](Resources/Geometry%20Solver%20Research%20for%20Structural%20Drawings%20-%20Step%208.md)

### 2.7 Stage 7 - Human Review, Overrides, And Targeted Reruns

#### Goal

Let a human review the scene graph and underlying evidence, then approve, reject, clarify, or override the model without mutating the raw extraction history.

#### Runtime Inputs

- scene graph
- evidence links
- issue register
- natural-language reviewer feedback
- structured UI review actions

#### Runtime Processing

- attach review actions at evidence, neutral-model, or scene-graph level
- convert natural-language feedback into structured actions when possible
- create override records
- invalidate only the affected downstream artifacts
- rerun only the necessary stages by default

#### Runtime Outputs

- `review/review_actions.json`
- `review/overrides.json`
- `review/reviewed_model.json`
- `review/rerun_requests.json`
- updated issue statuses and audit trail

#### Example Output Shape

```json
{
  "review_action_id": "REV_0003",
  "target_object_id": "OBJ_FRAME_PF2_GRID_B_01",
  "action_type": "override_attribute",
  "field": "section",
  "new_value": "530UB92",
  "reason": "Confirmed against schedule crop and elevation callout",
  "source_issue_ids": ["ISSUE_0007"]
}
```

#### This Stage Is Allowed To Claim

- that the reviewer changed or approved something
- what rerun should happen because of that action
- what reviewed overlay should be applied

#### This Stage Is Not Allowed To Claim

- that raw evidence changed
- that unresolved upstream ambiguity disappeared unless explicitly resolved
- that the entire project must rerun when only one local decision changed

#### Primary Research Links

- [Resources/HUGEPROMPT2/Human Review Protocol for AI Extraction.md](Resources/HUGEPROMPT2/Human%20Review%20Protocol%20for%20AI%20Extraction.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)
- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)

### 2.8 Stage 8 - Future Export Layer Later

#### Goal

Export is deliberately deferred.

The current milestone is a trustworthy review model.
Only after the reviewed neutral model is stable should the project consider IFC, Revit, USD, fabrication exports, or deeper interoperability.

#### Runtime Inputs

- reviewed neutral model
- reviewed scene graph
- explicit export mapping rules

#### Runtime Outputs

- none for the current milestone

#### Important Rule

Do not let future export design distort current review-first architecture.

#### Primary Research Links

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/Pipeline Object Identity and Naming.md](Resources/HUGEPROMPT2/Pipeline%20Object%20Identity%20and%20Naming.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)

### 2.9 Runtime Handoff Table

| Stage | Main Inputs | Main Outputs | Main Consumer |
| --- | --- | --- | --- |
| 1. Ingestion | uploaded PDFs | project manifest, page index, previews, crops | Stage 2, Stage 3, Stage 4 |
| 2. Lightweight classification | previews, metadata, filenames | page labels, routing hints | Stage 3 |
| 3. Pack interpretation | page images, routing hints, metadata | pack interpretation JSON, page atlas, unresolved questions | Stage 4, Stage 5 |
| 4. Deterministic evidence | PDFs, pack interpretation, text, vectors, crops | evidence bundle artifacts | Stage 5, Stage 7 |
| 5. Agentic synthesis | pack interpretation, evidence bundle, registry lookup | observations, resolved model, conflicts, unresolved items | Stage 6, Stage 7 |
| 6. Scene graph | resolved model, evidence links, issues | scene graph, geometry payloads, viewpoints | Stage 7 |
| 7. Human review | scene graph, evidence, issues, reviewer input | review actions, overrides, reviewed model, reruns | Stage 5, Stage 6 |
| 8. Future export | reviewed model, mapping rules | deferred | later milestone |

---

## 3. Core Source Set For Building This Product

The source set is intentionally split into three categories.

### 3.1 Must-Use Core Files

These files define the new architecture and should drive HUGEPROMPT2 directly:

- [copilot-instructions.md](copilot-instructions.md)
- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/HUGEPROMPT2/GPT-5.5 Structural Pack Interpretation JSON.md](Resources/HUGEPROMPT2/GPT-5.5%20Structural%20Pack%20Interpretation%20JSON.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/HUGEPROMPT2/Agentic Synthesis Protocol Design.md](Resources/HUGEPROMPT2/Agentic%20Synthesis%20Protocol%20Design.md)
- [Resources/HUGEPROMPT2/Pipeline Object Identity and Naming.md](Resources/HUGEPROMPT2/Pipeline%20Object%20Identity%20and%20Naming.md)
- [Resources/HUGEPROMPT2/Human Review Protocol for AI Extraction.md](Resources/HUGEPROMPT2/Human%20Review%20Protocol%20for%20AI%20Extraction.md)
- [Resources/HUGEPROMPT2/Scene Graph Contract for Browser Review.md](Resources/HUGEPROMPT2/Scene%20Graph%20Contract%20for%20Browser%20Review.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)
- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)

### 3.2 Supporting Active Domain Files

These files remain important for domain logic, deterministic reasoning, and review behavior:

- [Resources/Structural Drawing Reference Framework Research - Step 3.md](Resources/Structural%20Drawing%20Reference%20Framework%20Research%20-%20Step%203.md)
- [Resources/AI for Australian Steel Schedule Extraction - Step 4.md](Resources/AI%20for%20Australian%20Steel%20Schedule%20Extraction%20-%20Step%204.md)
- [Resources/Structural Plan Interpretation Research - 5.md](Resources/Structural%20Plan%20Interpretation%20Research%20-%205.md)
- [Resources/Structural Elevation Resolution Research - Step 6.md](Resources/Structural%20Elevation%20Resolution%20Research%20-%20Step%206.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)
- [Resources/Geometry Solver Research for Structural Drawings - Step 8.md](Resources/Geometry%20Solver%20Research%20for%20Structural%20Drawings%20-%20Step%208.md)
- [Resources/AI Structural Model Review Pipeline - Step 9.md](Resources/AI%20Structural%20Model%20Review%20Pipeline%20-%20Step%209.md)

### 3.3 Structural Template Reference Only

Use [HUGEPROMPT.md](HUGEPROMPT.md) only as a structural template for level of detail, section naming discipline, and stage-by-stage specification style.

Do not copy its old parser-first assumptions into the new architecture.

### 3.4 Explicitly Out Of Scope As Core Design Sources

Do not use the archive set as core planning input:

- [Resources/archive](Resources/archive)
- [backend/app/legacy](backend/app/legacy)

Do not treat [masterprompt2.txt](masterprompt2.txt) as the source of truth for this document.

Treat these root files as legacy reference only, not active planning input:

- [HUGEPROMPT.md](HUGEPROMPT.md)
- [MainPlan.md](MainPlan.md)
- [MainPlan.txt](MainPlan.txt)
- [masterprompt2.txt](masterprompt2.txt)

### 3.5 Current Repo Assets To Adapt, Not Recreate

The current repository already contains useful implementation shells.

Do not rebuild these from zero unless a hard technical blocker forces replacement.

Adapt these files first:

- [backend/app/ingestion.py](backend/app/ingestion.py) for PDF inspection, page metadata, text extraction, vector extraction, and future crop support
- [backend/app/config.py](backend/app/config.py) for backend-only environment loading, GPT defaults, and non-secret readiness reporting
- [backend/app/storage.py](backend/app/storage.py) for project storage, document upload, and separate override persistence
- [backend/app/main.py](backend/app/main.py) for the FastAPI shell and route layout
- [backend/.env.example](backend/.env.example) as the backend-only environment template for GPT-5.5 settings
- [frontend/src/App.tsx](frontend/src/App.tsx) for the browser review shell and inspection layout
- [frontend/src/api.ts](frontend/src/api.ts) and [frontend/src/store.ts](frontend/src/store.ts) for frontend data flow
- [frontend/src/components/StructureViewer.tsx](frontend/src/components/StructureViewer.tsx) for Three.js rendering, selection, labels, and grid overlays
- [frontend/src/styles.css](frontend/src/styles.css) for the existing review UI visual shell
- [backend/app/models.py](backend/app/models.py) and [frontend/src/types.ts](frontend/src/types.ts) as transitional contracts that should be evolved carefully until the new artifact-first schemas fully replace them

If a future implementation needs logic from the retired portal-frame POC pipeline, consult [backend/app/legacy/portal_poc_pipeline_legacy.py](backend/app/legacy/portal_poc_pipeline_legacy.py) only as a rescue source for isolated routines.
Do not extend its orchestration model.

### 3.6 Verified Bootstrap State For The Next Coding Chat

The repository already has a verified backend configuration bootstrap.

Treat these statements as current fact unless a later validation disproves them:

- the real API key belongs only in `backend/.env`, never in frontend `VITE_` config
- `backend/app/config.py` already loads `backend/.env` and exposes non-secret GPT readiness settings
- `backend/.env.example` is the editable template for local setup and onboarding
- `GET /api/health` is the quick non-secret readiness check and should stay available while the AI client is being integrated
- the current default first-pass model policy is `gpt-5.5`, `reasoning_effort=high`, `reasoning_summary=auto`, `detail=original`, `vision_input_mode=rendered_images`, and `max_output_tokens=25000`
- next-chat implementation should extend this bootstrap rather than creating a second config path or moving secrets into the frontend

---

## 4. Non-Negotiable Architectural Laws

These rules are mandatory.

### 4.1 Do Not Skip Stages

Bad:

```text
PDF -> GPT guess -> final 3D model
```

Good:

```text
PDF -> ingestion -> lightweight labeling -> pack interpretation -> deterministic evidence -> synthesis -> scene graph -> review overlay
```

### 4.2 Pack Interpretation Is A Structured Hypothesis, Not Final Truth

The first GPT pass may propose project type, candidate systems, priority pages, and unresolved questions.

It must not pretend that it has produced a fully resolved model.

### 4.3 Deterministic Evidence Must Stay Separate From Synthesis

Evidence extraction stores what the PDF says.
Synthesis decides how that evidence becomes neutral-model objects.

Do not collapse these into one mixed stage.

### 4.4 Use Retrieval Over Hidden Chat Memory

Agents must read and write typed artifacts.
They must not rely on long hidden conversational state as the main memory of the project.

### 4.5 Stable IDs Are Not Optional

All important artifacts, evidence objects, observations, resolved objects, issues, overrides, scene nodes, runs, and rerun replacements need stable IDs and lineage.

### 4.6 Uncertainty, Conflict, And Unresolved States Are First-Class

Low confidence is not enough.
The system must explicitly represent:

- ambiguity
- conflict
- missing evidence
- unresolved geometry
- unresolved identity
- needs-human-decision state

### 4.7 Human Review Is An Overlay Layer

The reviewed model is:

```text
raw artifacts + synthesis outputs + review actions + overrides = reviewed model
```

Review never mutates raw evidence history.

### 4.8 The Browser Model Must Expose Why Objects Exist

The reviewer must be able to click an object and inspect:

- source evidence
- upstream observations
- conflicts
- unresolved items
- review decisions

### 4.9 Targeted Reruns Beat Whole-Pipeline Reruns

If a reviewer resolves one schedule ambiguity, the system should rerun only the impacted downstream stages unless a broader invalidation is required.

### 4.10 No Mock-First Core Pipeline

Tiny UI scaffolding and isolated front-end placeholders are acceptable.

But the main build path must use real PDFs and real artifacts early.
The goal is not a fake demo.
The goal is a real artifact-backed pipeline.

### 4.11 No Archive-Driven Architecture Regression

Do not let older vector-first or parser-first instincts reshape the new architecture back into the old one simply because text or vectors happen to be available.

### 4.12 No Export-Driven Distortion

Current architecture is review-first.
Do not redesign the system around IFC, Revit, USD, or fabrication export before the reviewable neutral model is stable.

### 4.13 Adapt Useful Assets Before Replacing Them

If the current repository already has working upload, storage, override, UI, or viewer behavior, adapt that asset first.

Do not recreate a working shell from zero merely because the internal data contracts need to change.

Replacement is allowed only when:

- the current file blocks the new architecture materially
- the replacement path is clearer and lower risk than adaptation
- the migration preserves the currently useful behavior instead of discarding it casually

---

## 5. Mandatory Artifact Families, IDs, And Contracts

The whole system should communicate through typed, versioned artifacts.

### 5.1 Mandatory Artifact Families

| Artifact Family | Produced By | Must Contain | Consumed By |
| --- | --- | --- | --- |
| intake hint | UI or operator input | optional user hints, likely missing sheets, current priority goal, low-authority notes | pack interpretation |
| project manifest | ingestion | project ID, source docs, storage paths | all stages |
| document index | ingestion | document IDs, page IDs, page metadata | stages 2, 3, 4 |
| page atlas | pack interpretation | page roles, priorities, confidence | stages 4, 5 |
| pack interpretation | pack interpretation | broad project hypothesis, major systems, unresolved questions, evidence anchors | stages 4, 5 |
| coverage assessment | pack interpretation | proceed recommendation, suspected missing sheet families, confidence, operator status | UI, stages 4, 5 |
| interpretation manifest | pack interpretation | schema version, output sections present, retrieval hints, counts, linked evidence files | stages 4, 5 |
| evidence bundle | deterministic evidence | page, region, crop, text, vector, schedule, dimension, unresolved artifacts | stage 5, stage 7 |
| neutral observations | synthesis | observation records, evidence links, local decisions | synthesis, review |
| resolved model | synthesis | resolved objects, maturity level, identity links | scene graph, review |
| issue register | synthesis and review | unresolved items, conflicts, escalation state | scene graph, review |
| scene graph | scene graph stage | reviewable scene nodes, geometry references, evidence links | browser review |
| review actions | review stage | structured user actions and targets | rerun logic |
| overrides | review stage | immutable overlay modifications | reviewed model, reruns |
| run records | every agent stage | prompt version, parser version, response ID, status, cost, lineage | debugging, audit |

### 5.2 Stable ID Prefixes

Use predictable IDs.

- `PROJ_` for projects
- `DOC_` for documents
- `PAGE_` for pages
- `CROP_` for crop artifacts
- `RUN_` for stage runs
- `ART_` for artifact records
- `EV_` for evidence items
- `OBS_` for synthesis observations
- `OBJ_` for resolved neutral-model objects
- `SCN_` for scene graph nodes
- `ISSUE_` for issues and conflicts
- `OVR_` for overrides
- `REV_` for review actions

### 5.3 Canonical Artifact Registry Record

```json
{
  "artifact_id": "ART_PACK_INTERPRETATION_0001",
  "project_id": "PROJ_B9BE6D2C",
  "stage": "pack_interpretation",
  "artifact_kind": "pack_interpretation_json",
  "version": 1,
  "status": "completed",
  "path": "artifacts/pack_interpretation/v1/pack_interpretation.json",
  "input_artifact_ids": ["ART_INGESTION_0001", "ART_CLASSIFICATION_0001"],
  "run_id": "RUN_0007"
}
```

### 5.4 Canonical Evidence Object

```json
{
  "evidence_id": "EV_0211",
  "project_id": "PROJ_B9BE6D2C",
  "page_id": "PAGE_0019",
  "crop_id": "CROP_0042",
  "artifact_family": "schedule_artifact",
  "raw_text": "PF2 530UB92",
  "normalized_text": "PF2 530UB92",
  "bbox_norm": [0.143, 0.221, 0.318, 0.257],
  "method": "pdf_text_plus_table_grouping",
  "confidence": 0.94
}
```

### 5.5 Canonical Observation Object

```json
{
  "observation_id": "OBS_0094",
  "object_family": "portal_frame_instance",
  "proposed_identity": "OBJ_FRAME_PF2_GRID_B_01",
  "claim": {
    "frame_type": "PF2",
    "grid_location": "B"
  },
  "evidence_ids": ["EV_0211", "EV_0319"],
  "confidence": 0.88,
  "status": "proposed"
}
```

### 5.6 Canonical Issue Object

```json
{
  "issue_id": "ISSUE_0007",
  "scope": "object_local",
  "issue_kind": "conflicting_schedule_assignment",
  "target_object_id": "OBJ_FRAME_PF2_GRID_B_01",
  "evidence_ids": ["EV_0211", "EV_0442"],
  "alternatives": [
    {"value": "530UB82", "confidence": 0.38},
    {"value": "530UB92", "confidence": 0.56}
  ],
  "status": "needs_review"
}
```

### 5.7 Canonical Override Object

```json
{
  "override_id": "OVR_0002",
  "review_action_id": "REV_0003",
  "target_object_id": "OBJ_FRAME_PF2_GRID_B_01",
  "field": "section",
  "old_value": "530UB82",
  "new_value": "530UB92",
  "reason": "Confirmed against schedule crop and elevation callout"
}
```

### 5.8 Mandatory Unresolved Taxonomy

At minimum, support these unresolved categories:

- `missing_information`
- `ambiguous_read`
- `conflicting_evidence`
- `broken_reference_chain`
- `identity_unstable`
- `geometry_unsolved`
- `needs_human_decision`

### 5.9 Mandatory Run Record Fields

Every AI or agent stage run must store:

- run ID
- stage name
- project ID
- prompt version
- parser version
- model name
- response ID
- input artifact IDs
- output artifact IDs
- start and finish time
- status
- retry count
- token and cost summary if available
- failure reason if failed

### 5.10 Prompt Asset Rules

Prompt management is part of the architecture, not an afterthought.

At minimum:

- every AI stage must use editable prompt files stored in the repository rather than hidden inline strings
- prompts must be versioned and tied to run records
- parser versions must be versioned separately from prompt versions
- model settings must be stored per stage run
- API keys must come from environment or config, never from hardcoded source
- the Stage 3 prompt set must support an optional intake hint without treating that hint as evidence
- the pipeline should preserve both raw model output and parsed structured output for debugging and replay

Recommended minimum prompt assets:

- stage system prompt
- stage extraction contract or schema prompt
- stage parser definition or parser version record
- prompt assembly logic that injects project artifacts, page/crop references, and optional intake hints

---

## 6. Documentation And Delivery Discipline

Every stage implementation is incomplete until it ships with all of the following:

1. a written stage contract
2. explicit input artifact list
3. explicit output artifact list
4. one example artifact payload
5. one validator or schema check
6. one failure-mode list
7. one debug surface in the API or UI

For this product, good engineering means good runtime behavior plus good inspectability.

---

## 7. Very Detailed Step-By-Step Guide To Create The Product

This is the implementation order.

Do not build this out of order unless a concrete blocker forces a local reorder.

Global implementation rule for every step below:

- inspect the existing file or module that already serves that concern
- decide whether it should be kept and adapted, wrapped and replaced gradually, or left in legacy
- prefer adapting the kept shells over recreating them from zero

### Step 0 - Triage Existing Repo Assets Before New Architecture Work

#### Purpose

Separate reusable implementation shells from retired architecture before new development starts, so the new build does not accidentally recreate working behavior or extend the wrong code path.

#### Build Inputs

- [copilot-instructions.md](copilot-instructions.md)
- [backend/app/ingestion.py](backend/app/ingestion.py)
- [backend/app/storage.py](backend/app/storage.py)
- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/api.ts](frontend/src/api.ts)
- [frontend/src/store.ts](frontend/src/store.ts)
- [frontend/src/components/StructureViewer.tsx](frontend/src/components/StructureViewer.tsx)
- [backend/app/legacy/portal_poc_pipeline_legacy.py](backend/app/legacy/portal_poc_pipeline_legacy.py)

#### Build Outputs

- keep-and-adapt list
- legacy-reference list
- migration notes for transitional contracts
- explicit statement of which existing user-visible behaviors must survive the migration

#### Concrete Work

- confirm that upload, project storage, override persistence, review layout, and Three.js selection behavior are being preserved and adapted
- confirm that the old monolithic portal-only pipeline remains legacy reference only
- record which existing modules will be evolved in place versus replaced gradually behind stable APIs
- make sure the new architecture grows out of the current useful shell instead of restarting it from zero

#### Validation

- a new chat should be able to identify active versus legacy files immediately without repo archaeology
- the implementation plan should preserve currently useful upload, review, and viewer behavior deliberately rather than accidentally deleting it

#### Use These Resources

- [copilot-instructions.md](copilot-instructions.md)
- [HUGEPROMPT2.md](HUGEPROMPT2.md)
- [MainPlan2.md](MainPlan2.md)

### Step 1 - Freeze Scope, Gold Packs, And Acceptance Questions

#### Purpose

Lock the first milestone so the pipeline is built against a real target instead of a vague ambition.

#### Build Inputs

- [MainPlan2.md](MainPlan2.md)
- sample packs in `example pdfs/`
- current project data under `backend/data/projects/`
- the existing review shell files kept from Step 0

#### Build Outputs

- chosen gold sample pack set
- portal-frame POC acceptance checklist
- written list of required visible outputs in UI and API
- list of out-of-scope items for the first milestone

#### Concrete Work

- choose one or two representative warehouse packs
- list the exact pages that should matter most
- define the minimum portal-frame objects the system must surface
- define what counts as acceptable schematic placement versus metric placement
- define which unresolved items are acceptable and which are blockers
- define the review interactions that must exist in the UI
- define which current UI and viewer behaviors are mandatory to preserve during the migration

#### Validation

- a human should be able to answer, before coding, whether the POC succeeded or failed on a pack
- the team should be able to name the exact outputs expected after one complete pipeline run

#### Use These Resources

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/AI Structural Model Review Pipeline - Step 9.md](Resources/AI%20Structural%20Model%20Review%20Pipeline%20-%20Step%209.md)

### Step 2 - Define Project Storage, Artifact Registry, And Run Lineage First

#### Purpose

Create the storage and lineage backbone before deeper extraction logic starts writing ad hoc files.

#### Build Inputs

- current backend storage flow
- existing project folder conventions under `backend/data/projects/`
- current backend modules such as `backend/app/storage.py`, `backend/app/models.py`, and `backend/app/main.py`
- legacy orchestration reference in `backend/app/legacy/portal_poc_pipeline_legacy.py`

#### Build Outputs

- artifact registry schema
- run record schema
- project storage layout
- stage state machine definition
- invalidation and rerun rules for downstream artifacts

#### Concrete Work

- adapt the current storage and API shell rather than replacing it wholesale
- define a stable folder layout per project for source docs, artifacts, review state, and runs
- create one artifact registry file or table that can locate every artifact by project, stage, version, and type
- create the run record format before the first GPT call is integrated
- define artifact status values such as queued, running, validating, completed, failed, superseded, and archived
- define how a rerun supersedes earlier artifacts without deleting history

#### Suggested Project Artifact Layout

```text
backend/data/projects/{project_id}/
  project.json
  documents/
  artifacts/
    ingestion/
    classification/
    pack_interpretation/
    evidence_bundle/
    neutral_model/
    scene_graph/
    review/
    runs/
```

#### Validation

- any artifact should be discoverable from the registry without searching the whole project folder
- any run should be able to list its input artifacts and output artifacts
- a failed run should still leave a readable partial record

#### Use These Resources

- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)
- [Resources/HUGEPROMPT2/Pipeline Object Identity and Naming.md](Resources/HUGEPROMPT2/Pipeline%20Object%20Identity%20and%20Naming.md)

### Step 3 - Build Ingestion, Preview, Metadata, And Crop Services

#### Purpose

Make the PDFs operational for every later stage.

#### Build Inputs

- uploaded PDF folder
- storage conventions from Step 2

#### Build Outputs

- persisted original PDFs
- page preview images
- page metadata
- crop rendering service
- optional text and vector side artifacts

#### Concrete Work

- adapt the current ingestion flow in `backend/app/ingestion.py` instead of rebuilding ingestion from zero
- ensure `backend/app/storage.py` preserves original files unchanged
- expose preview and crop retrieval through the backend API
- store page width, height, and rotation in a normalized page index
- store whether text and vector channels are available per page

#### Validation

- every page can be previewed in the frontend
- any normalized bbox can be turned into a crop image
- the system can distinguish raster-heavy from vector-heavy pages

#### Use These Resources

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### Step 4 - Implement Lightweight Classification And Routing

#### Purpose

Create a fast organizational pass that makes the pack readable to downstream stages without pretending to solve the job.

#### Build Inputs

- page previews
- filenames
- page metadata
- optional title block hints

#### Build Outputs

- provisional page labels
- page-group assignments
- routing priorities
- unknown-page queue

#### Concrete Work

- add a lightweight classification step as a new artifact-producing path instead of restoring the retired monolithic pipeline
- define a minimal page-label enum such as schedule, plan, elevation, detail, notes, unknown, and low-priority
- keep classification conservative and cheap
- expose page labels and routing hints in API responses and UI state
- allow uncertain pages to remain uncertain

#### Validation

- schedule-heavy pages should usually rise above general-note pages in priority
- obvious plan and elevation pages should be separated often enough to improve Stage 3 cost and focus
- unknown pages must remain visible instead of disappearing from the pipeline

#### Use These Resources

- [MainPlan2.md](MainPlan2.md)
- [Resources/HUGEPROMPT2/GPT-5.5 Structural Pack Interpretation JSON.md](Resources/HUGEPROMPT2/GPT-5.5%20Structural%20Pack%20Interpretation%20JSON.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### Step 5 - Integrate GPT-5.5 Responses API And Run Management

#### Purpose

Make model calls first-class, replayable, and debuggable before higher-level interpretation logic depends on them.

#### Build Inputs

- page previews and crops
- routing hints
- artifact registry and run record design
- existing backend env/config access to the GPT-5.5 API key through `backend/app/config.py`
- editable stage prompt files

#### Build Outputs

- Responses API client integration
- prompt registry or prompt file layout
- editable system prompts and stage prompt assets
- stage model configuration
- documented backend-only environment contract
- non-secret config readiness reporting
- stored raw model outputs
- stored parsed outputs
- retry policy
- prompt and parser version tracking

#### Concrete Work

- add a dedicated AI client layer in the backend
- keep system prompts as editable repository assets instead of burying them inside Python strings
- extend `backend/app/config.py` instead of creating a parallel config system
- keep the real API key in `backend/.env` only and never expose it through frontend `VITE_` variables
- keep the initial Stage 3 model defaults aligned with the current bootstrap: `gpt-5.5`, `reasoning_effort=high`, `reasoning_summary=auto`, `detail=original`, `vision_input_mode=rendered_images`, `max_output_tokens=25000`
- treat high-resolution rendered page images and crops as the primary Stage 3 vision inputs, with PDF `input_file` support as a secondary or fallback path rather than the only path
- define a prompt registry or prompt-folder convention for each AI stage
- integrate it into the existing FastAPI and storage shell rather than creating a separate parallel app
- store response ID, model name, prompt version, parser version, and raw output for every run
- distinguish transport failure, schema failure, parse failure, and logic failure
- implement idempotent retries for safe cases
- make prompt and parser versions explicit in run records
- preserve `GET /api/health` as a non-secret readiness surface while the AI client is being introduced

#### Validation

- one failed parse should not hide the raw model output
- repeated identical requests should be detectable in run history
- operators should be able to inspect the exact prompt and parser used for a run
- `GET /api/health` should confirm model configuration readiness without exposing the API key

#### Use These Resources

- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### Step 6 - Implement The Pack Interpretation JSON Contract

#### Purpose

Create the first deep AI stage as a disciplined contract instead of a loose summary.

#### Build Inputs

- page images
- routing hints
- page metadata
- Responses API client

#### Build Outputs

- pack interpretation schema
- page atlas schema
- coverage assessment schema
- interpretation evidence schema
- interpretation manifest schema
- operator update schema
- unresolved question schema
- stored pack interpretation artifacts

#### Concrete Work

- define required versus optional fields
- define the optional `intake_hint.json` contract as a low-authority input to this stage
- explicitly mark allowed claims versus forbidden claims
- create page atlas output with page roles, confidence, and priority
- create a structured coverage assessment with suspected missing sheet families and a soft proceed recommendation
- create an operator-facing status artifact derived from structured fields rather than ad hoc free text
- create interpretation evidence and interpretation manifest artifacts so later stages know what exists and where to look
- create unresolved-question records with category and evidence anchors
- create parser validation so the stage cannot silently overreach
- plug the outputs into the existing project storage and review shell instead of inventing a disconnected temporary UI path

#### Validation

- the output should be useful enough to guide deterministic extraction even when some pages remain ambiguous
- exact quantities, exact sizes, and final geometry should fail validation if they are unsupported
- every important pack-level claim should reference source pages or crops
- the stage should be able to continue with partial confidence instead of forcing a false yes or no on pack sufficiency
- downstream stages should be able to locate Stage 3 outputs from the interpretation manifest without guessing output structure

#### Use These Resources

- [Resources/HUGEPROMPT2/GPT-5.5 Structural Pack Interpretation JSON.md](Resources/HUGEPROMPT2/GPT-5.5%20Structural%20Pack%20Interpretation%20JSON.md)
- [Resources/Structural Plan Interpretation Research - 5.md](Resources/Structural%20Plan%20Interpretation%20Research%20-%205.md)
- [Resources/Structural Elevation Resolution Research - Step 6.md](Resources/Structural%20Elevation%20Resolution%20Research%20-%20Step%206.md)

### Step 7 - Build The Deterministic Evidence Bundle Core

#### Purpose

Create the evidence layer that later stages can trust and retrieve.

#### Build Inputs

- source PDFs
- page previews and crops
- pack interpretation JSON
- text and vector channels when present

#### Build Outputs

- evidence bundle manifest
- page artifact schema
- crop artifact schema
- unresolved region schema
- retrieval indexes

#### Concrete Work

- create a bundle manifest that lists all artifact families produced for a run
- create retrieval indexes so later agents know which evidence families exist and how to query them
- normalize coordinates into page-relative values while preserving raw source values
- preserve raw text plus normalized text
- record method and confidence for each artifact
- store unresolved regions as explicit artifacts instead of dropping failures
- make evidence lookup possible by page, bbox, artifact family, and linked object ID later
- replace old seeded evidence outputs gradually behind stable API contracts rather than deleting the current shell first

#### Validation

- synthesis should be able to retrieve artifacts by page, by region, and by artifact family without reading the whole project
- unresolved extractions must be visible and queryable
- OCR-derived artifacts must remain distinguishable from deterministic PDF-native artifacts

#### Use These Resources

- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)

### Step 8 - Add Schedule And Catalogue Evidence Extraction

#### Purpose

Turn schedule regions into structured evidence that can support later mark-to-section resolution.

#### Build Inputs

- evidence bundle manifest
- schedule candidate regions
- text extraction or OCR outputs
- page crops

#### Build Outputs

- schedule region artifacts
- row candidate artifacts
- normalized section strings
- mark-to-section evidence links
- unresolved schedule crops

#### Concrete Work

- detect schedule regions and their titles
- group lines and cells where possible
- extract text and preserve row-level raw strings
- normalize Australian steel notation while retaining raw source text
- distinguish project marks from catalogue sections and notes
- create unresolved artifacts for visually readable but structurally messy schedules

#### Validation

- the same mark should not silently normalize into multiple sections without producing a conflict or issue
- schedule evidence should remain inspectable at region and row level
- the system should prefer honest partial parse plus crop evidence over brittle fake precision

#### Use These Resources

- [Resources/AI for Australian Steel Schedule Extraction - Step 4.md](Resources/AI%20for%20Australian%20Steel%20Schedule%20Extraction%20-%20Step%204.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)

### Step 9 - Add Reference Framework And Spatial Anchor Extraction

#### Purpose

Create the coordinate bootstrap layer that synthesis will rely on.

#### Build Inputs

- page artifacts
- dimension strings
- level markers
- RL markers
- grid labels
- plan and elevation evidence pages

#### Build Outputs

- grid artifacts
- level artifacts
- RL artifacts
- dimension-chain artifacts
- reference framework summary

#### Concrete Work

- extract grids, levels, datums, RLs, and dimension chains as explicit artifacts
- reconcile fragmented dimension chains where possible
- record conflicting coordinate evidence rather than forcing a single answer
- connect plan anchors to elevation anchors when identifiable
- preserve the evidence graph needed for later coordinate solving

#### Validation

- synthesis should be able to ask, for any object placement, which grid and level evidence supported it
- broken dimension chains must raise unresolved issues rather than disappearing
- plan and elevation anchors should be linkable when the evidence supports the connection

#### Use These Resources

- [Resources/Structural Drawing Reference Framework Research - Step 3.md](Resources/Structural%20Drawing%20Reference%20Framework%20Research%20-%20Step%203.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)

### Step 10 - Add Plan And Elevation Evidence Extractors

#### Purpose

Extract the reusable frame-template and frame-instance evidence needed for the portal-frame POC.

#### Build Inputs

- pack interpretation priorities
- reference framework artifacts
- page crops and vector artifacts
- plan pages and elevation pages

#### Build Outputs

- portal frame template artifacts
- portal frame instance candidate artifacts
- plan-to-elevation linkage records
- vertical constraint artifacts

#### Concrete Work

- capture elevation frame labels and member callouts
- capture support locations, roof profile cues, and dimension strings from elevations
- capture PF labels, ordered occurrences, spacing cues, and grid associations from plans
- connect template candidates from elevations to instance candidates from plans
- save ambiguous regions for targeted follow-up reads instead of collapsing them prematurely

#### Validation

- plan-derived frame occurrences should be inspectable independently from elevation-derived template definitions
- missing plan-to-elevation links must stay unresolved, not assumed
- vertical constraints must remain traceable to explicit evidence objects

#### Use These Resources

- [Resources/Structural Plan Interpretation Research - 5.md](Resources/Structural%20Plan%20Interpretation%20Research%20-%205.md)
- [Resources/Structural Elevation Resolution Research - Step 6.md](Resources/Structural%20Elevation%20Resolution%20Research%20-%20Step%206.md)
- [Resources/HUGEPROMPT2/Deterministic Evidence Bundle for Drawings.md](Resources/HUGEPROMPT2/Deterministic%20Evidence%20Bundle%20for%20Drawings.md)

### Step 11 - Build The Synthesis Orchestrator And Neutral-Model Assembly Loop

#### Purpose

Build the agentic stage that turns stored artifacts into a coherent neutral model.

#### Build Inputs

- pack interpretation JSON
- evidence bundle artifacts
- schedule, reference, plan, and elevation evidence
- artifact registry lookup

#### Build Outputs

- synthesis planning loop
- neutral-model observation schema
- resolved-object schema
- conflict and unresolved schema
- committed neutral-model artifacts

#### Concrete Work

- implement a plan-retrieve-verify-synthesize loop
- break synthesis into local questions rather than one giant prompt
- bootstrap coordinates before broader placement decisions
- map schedule marks to physical candidates
- create observations first, then resolved objects second
- stop and emit unresolved or conflicting records when evidence is insufficient

#### Validation

- no resolved object should exist without evidence links
- no final placement should exist if the coordinate bootstrap never happened
- conflicting schedule or template evidence must stay visible in issue records

#### Use These Resources

- [Resources/HUGEPROMPT2/Agentic Synthesis Protocol Design.md](Resources/HUGEPROMPT2/Agentic%20Synthesis%20Protocol%20Design.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)

### Step 12 - Implement Identity, Naming, Merge, Split, And Rerun Stability

#### Purpose

Keep object identity coherent across synthesis passes, reruns, and reviewer corrections.

#### Build Inputs

- synthesis observations
- resolved objects
- prior versions of resolved objects
- rerun requests and override records

#### Build Outputs

- canonical object naming rules
- merge records
- split records
- tombstones or superseded-object lineage records
- stable display naming rules separate from canonical IDs

#### Concrete Work

- separate canonical IDs from user-facing display names
- create deterministic identity rules for evidence-derived objects when possible
- track when one object becomes two objects or two objects become one
- preserve lineage when reruns change identity assumptions
- keep object-family namespaces explicit for frames, members, supports, bays, zones, surfaces, and connections

#### Validation

- the same frame should keep a stable identity when a rerun only adds stronger evidence
- merge or split events should be explicit in lineage, not hidden in silent replacement
- user-facing labels should remain readable without becoming the canonical identity source

#### Use These Resources

- [Resources/HUGEPROMPT2/Pipeline Object Identity and Naming.md](Resources/HUGEPROMPT2/Pipeline%20Object%20Identity%20and%20Naming.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)

### Step 13 - Add Deterministic Geometry Enrichment For Schematic And Metric States

#### Purpose

Convert the neutral model into browser-ready geometric representations without pretending that every object is fully resolved.

#### Build Inputs

- resolved neutral model
- reference framework artifacts
- schedule and template evidence
- identity and naming rules

#### Build Outputs

- centerline geometry
- proxy geometry payloads
- maturity labels per object
- geometry confidence and conflict annotations

#### Concrete Work

- generate portal frame centerlines and simple member proxies first
- attach schematic versus metric labels explicitly
- use deterministic coordinate solving when the evidence supports it
- preserve unresolved or approximate geometry as such
- record which geometry was derived from explicit dimensions versus inferred topology
- preserve the existing viewer-friendly geometry shell while swapping its backing contracts to the new scene-graph path

#### Validation

- a schematic object should never be exposed as metric by default
- the browser payload should be lightweight enough for review while still traceable to upstream objects
- unresolved geometry should stay selectable and explainable in the viewer

#### Use These Resources

- [Resources/Geometry Solver Research for Structural Drawings - Step 8.md](Resources/Geometry%20Solver%20Research%20for%20Structural%20Drawings%20-%20Step%208.md)
- [Resources/Structural Graph Builder Research - Step 7.md](Resources/Structural%20Graph%20Builder%20Research%20-%20Step%207.md)
- [Resources/Structural Drawing Reference Framework Research - Step 3.md](Resources/Structural%20Drawing%20Reference%20Framework%20Research%20-%20Step%203.md)

### Step 14 - Build The Scene Graph Contract And Browser Review UI

#### Purpose

Turn resolved objects and geometry payloads into the actual review product.

#### Build Inputs

- resolved model
- geometry payloads
- issue register
- evidence links
- existing frontend surfaces such as `frontend/src/api.ts`, `frontend/src/types.ts`, `frontend/src/store.ts`, and `frontend/src/components/StructureViewer.tsx`

#### Build Outputs

- scene graph schema
- browser scene graph endpoint
- evidence panel behavior
- issue panel behavior
- maturity and uncertainty filters

#### Concrete Work

- define scene nodes separately from heavy geometry blobs
- attach evidence IDs and issue IDs to every reviewable node
- allow the user to select objects and inspect why they exist
- show uncertainty and unresolved state visually
- keep viewer behavior honest about semantic, topological, schematic, and metric maturity

#### Validation

- the reviewer should be able to click a frame or member and inspect its source evidence
- low-confidence or unresolved nodes should be visibly distinct
- the scene graph should be usable even before every object reaches metric maturity

#### Use These Resources

- [Resources/HUGEPROMPT2/Scene Graph Contract for Browser Review.md](Resources/HUGEPROMPT2/Scene%20Graph%20Contract%20for%20Browser%20Review.md)
- [Resources/AI Structural Model Review Pipeline - Step 9.md](Resources/AI%20Structural%20Model%20Review%20Pipeline%20-%20Step%209.md)
- [Resources/Geometry Solver Research for Structural Drawings - Step 8.md](Resources/Geometry%20Solver%20Research%20for%20Structural%20Drawings%20-%20Step%208.md)

### Step 15 - Implement Human Review, Structured Overrides, And Targeted Reruns

#### Purpose

Create the review loop that turns a raw pipeline into a trustworthy product.

#### Build Inputs

- scene graph
- issue register
- evidence links
- reviewer selections and comments
- run lineage and artifact registry

#### Build Outputs

- structured review actions
- override records
- reviewed-model overlay
- rerun dependency logic
- review audit trail

#### Concrete Work

- define review action types such as approve, reject, override attribute, override association, request clarification, accept schematic, and add note
- translate natural-language feedback into structured records when possible
- connect review actions to invalidation and rerun rules
- compose a reviewed model from raw outputs plus overlay records
- keep the audit trail immutable

#### Validation

- one override should update the reviewed model without deleting the raw model history
- local review actions should request local reruns by default
- unresolved items should only disappear when the system or reviewer explicitly resolves them

#### Use These Resources

- [Resources/HUGEPROMPT2/Human Review Protocol for AI Extraction.md](Resources/HUGEPROMPT2/Human%20Review%20Protocol%20for%20AI%20Extraction.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)

### Step 16 - Add QA, Acceptance Testing, And Operator Debug Surfaces

#### Purpose

Make the pipeline falsifiable, inspectable, and supportable.

#### Build Inputs

- gold packs from Step 1
- all runtime artifacts from earlier steps
- run records and issue records

#### Build Outputs

- acceptance checks
- stage validators
- operator debug views
- golden artifact snapshots
- failure classification dashboard or logs

#### Concrete Work

- create schema validation for every major artifact family
- create pack-level acceptance checks for portal frame objects, evidence linkage, and unresolved visibility
- expose run history, prompt version, parser version, and failure reason in an operator-facing debug surface
- record golden artifacts for known sample packs
- add consistency checks such as every scene node links to an object, every object links to evidence, and every unresolved issue is still accessible in the UI

#### Validation

- a broken parser should fail loudly and traceably
- a scene node with no evidence link should fail QA
- a rerun should preserve prior lineage and make supersession visible

#### Use These Resources

- [Resources/HUGEPROMPT2/LLM Pipeline Run Management Design.md](Resources/HUGEPROMPT2/LLM%20Pipeline%20Run%20Management%20Design.md)
- [Resources/HUGEPROMPT2/AI Drawing Interpretation Pipeline Architecture.md](Resources/HUGEPROMPT2/AI%20Drawing%20Interpretation%20Pipeline%20Architecture.md)
- [Resources/HUGEPROMPT2/Uncertainty and Conflict Pipeline Model.md](Resources/HUGEPROMPT2/Uncertainty%20and%20Conflict%20Pipeline%20Model.md)

---

## 8. Product Acceptance Criteria

The first successful version of this product must:

1. accept a folder of PDF drawings into a managed local project
2. render and index every page
3. attach lightweight provisional labels before deep interpretation
4. run GPT-5.5 pack interpretation and save a structured interpretation JSON
5. build a deterministic evidence bundle with page, crop, schedule, dimension, and reference artifacts
6. synthesize a neutral structural model with named elements and explicit maturity states
7. generate a browser scene graph for the primary structure
8. let the reviewer click objects and inspect evidence, issues, and upstream reasoning
9. preserve uncertainty, conflict, and unresolved states visibly
10. support structured overrides and targeted reruns without mutating raw history

---

## 9. What To Avoid

Avoid these failure modes:

- drifting back into parser-first architecture because text and vectors exist
- asking GPT-5.5 to emit final 3D geometry directly
- mixing evidence extraction and synthesis into one opaque stage
- creating objects with no evidence IDs
- silently collapsing ambiguity into a single answer
- storing reviewer decisions by overwriting raw artifacts
- forcing full reruns when only local invalidation is needed
- designing around future export before the review product works
- using archive files as the architectural baseline

---

## 10. Immediate Execution Order For Future Self

When work starts again, follow this exact order:

1. confirm the gold pack and acceptance checklist
2. formalize artifact registry and run record schemas
3. finish ingestion, preview, and high-resolution crop capability
4. add lightweight classification
5. extend the existing backend env/config bootstrap into GPT-5.5 Responses API integration with stored raw outputs
6. ship the pack interpretation JSON contract
7. ship the evidence bundle manifest and page artifact family
8. add schedule, reference, plan, and elevation evidence workers
9. build synthesis observations and resolved objects
10. add identity, uncertainty, scene graph, and review overlay in that order

Current verified start state before the next coding chat:

- `backend/.env` is the local backend-only secret location
- `backend/.env.example` is the safe template for expected settings
- `backend/app/config.py` already loads the backend env and exposes non-secret GPT readiness defaults
- `GET /api/health` already reports whether GPT configuration is wired without revealing the key
- the next coding chat should begin from this shell and move into Step 5, not redesign the repo bootstrap from zero

---

## 11. Final Operating Instruction

Build the product so that a reviewer can click any scene object and answer four questions immediately:

1. what does the system think this object is
2. why does the system think it exists
3. how certain is the system about it
4. what can the reviewer do if it is wrong

If a proposed implementation makes those four questions harder to answer, it is probably the wrong implementation for this milestone.