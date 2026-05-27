# MainPlan3

## Agent-Orchestrated Structural Drawing Interpretation Workflow

---

## 0. Purpose Of This Plan

This document defines the high-level workflow for the project.

The project is framed as:

> an agent-orchestrated structural drawing interpretation system, with GPT-5.5 acting as the main reasoning and coordination layer, and vision acting as its primary reading tool

This is a general architecture for technical and structural drawing packs.

It is not limited to warehouses, even though portal-frame and warehouse-style projects may remain the first proof of concept.

The goal of this document is to define the end-to-end workflow of the product in clear general terms before implementation details are finalized.

---

## 1. Product Goal

Build a system that can:

1. ingest a drawing pack
2. understand what the pack contains
3. decide how the pack should be read
4. gather relevant information through coordinated agents
5. build a structured internal model of what exists in the project
6. generate a scene graph that shows what the AI believes is there
7. support human feedback at the first interpretation milestone and during later browser review
8. later use the reviewed model as the basis for BIM or Revit-oriented export

The product is not just a document reader.

The product is a reasoning system that interprets technical documents into a reviewable structural and geometric model.

---

## 2. Core Thesis

The main architectural idea is:

> GPT-5.5 is the orchestrator.

The orchestrator does not only read pages.

It:

- reasons over the whole pack
- decides what matters
- chooses which agents to call
- chooses whether vision alone is enough or whether support tools should be invoked
- organizes outputs into shared memory and artifacts
- drives synthesis into a neutral model
- requests verification
- routes human feedback back into the workflow

Vision is still central, but not as an ideology.

Vision is the orchestrator's primary sensing and interpretation tool.

---

## 3. Core Principles

### 3.1 General architecture, domain-specialized outputs

The architecture should work for structural and technical drawing packs broadly.

The first POC may focus on portal-frame steel projects, but the system should be able to reason about broader object families such as:

- walls
- columns
- beams
- roofs
- slabs
- openings
- frames
- supports
- grids
- levels
- schedules
- notes
- details
- zones or spaces

### 3.2 PDFs are multimodal sources

A PDF is not only an image and not only text.

A drawing pack may contain:

- rendered page imagery
- vector geometry
- embedded text layers
- tables and schedules
- title blocks
- callouts
- dimensions
- notes
- symbols
- details
- cross-sheet references

The orchestrator should decide which representation is most useful for each task.

### 3.3 Vision is the default first read

GPT-5.5 vision should usually be the first reading tool used by the orchestrator.

It should be allowed to inspect whole pages, crops, and follow-up regions iteratively.

Typical interaction pattern:

1. read the pack broadly
2. identify what the project appears to be
3. identify what information matters
4. request targeted follow-up reads
5. continue until enough understanding exists for structured synthesis

### 3.3A The current optimization target is effectiveness before efficiency

At this stage of the project, the system should optimize first for:

- correctness
- usefulness
- inspectability
- robustness of the workflow

It should not yet treat AI cost reduction as a hard architectural boundary.

The orchestrator should be allowed to:

- re-read pages
- request extra crops or tiles
- over-collect evidence when needed
- invoke more verification than may later be economical

Efficiency tuning should come later, once the workflow is proven to work reliably.

### 3.3B Spatial reasoning should be grounded from the plan upward

The system should prefer to think about the project the way architects and engineers usually do when first understanding a structure.

That means the model should be grounded first in the spatial manifestation of elements in the plan or ground-floor space, and then extended upward into columns, walls, roofs, upper levels, supports, and other vertical or elevated relationships.

This should influence both interpretation and modeling.

The workflow should prefer to establish:

- where elements sit in plan
- how they partition or define space
- what they connect to at the base spatial level
- how higher or dependent elements rise from that plan-level organization

### 3.4 Agents communicate through memory and artifacts, not one shared context window

The system should not rely on one giant shared prompt or a single long conversational context.

Instead, it should use:

- shared project memory
- shared artifact storage
- orchestrator-managed task briefs
- task-specific retrieved context
- typed outputs written back into the project state

This keeps the workflow:

- cheaper
- more auditable
- more focused
- easier to rerun
- easier to debug

### 3.4A Prompt families should be stable even if task briefs are dynamic

The orchestrator should not invent the entire prompting strategy from scratch on every run.

Instead, the system should maintain stable prompt families or templates for recurring jobs such as:

- reconnaissance
- targeted plan reading
- targeted elevation reading
- schedule reading
- detail reading
- synthesis
- verification

The orchestrator should decide:

- which prompt family to use
- which artifacts to include
- what the immediate task is
- what the requested output should contain
- whether a follow-up read is needed

This keeps the workflow adaptable without making prompting chaotic.

### 3.4B The orchestrator may infer, but inferred data must remain explicitly flagged

The orchestrator should be allowed to infer approximate or schematic values when direct information is missing and the inferred value is useful for scene understanding.

However, inferred data must:

- be explicitly marked as inferred
- remain reviewable by a human
- remain distinguishable from directly read values
- never be silently upgraded into authoritative metric truth

The workflow should preserve distinctions such as:

- directly read
- derived from explicit evidence
- inferred schematic
- unknown

### 3.5 PDF-native extraction is optional support, not the backbone

PDF-native extraction remains useful, but it should not define the main process.

It should be treated as:

- an optional support path
- an orchestrator-invoked helper
- a source of structured supporting evidence
- something that can be disabled, down-weighted, or emphasized depending on test results

This support path can be totally disabled for a run, for a project type, or for a testing configuration without breaking the core architecture.

If needed, the orchestrator should ask the deterministic extractor for help and manage the relationship.

This support path may be useful for:

- schedules and tables
- text-layer recovery
- title block extraction
- vector-heavy dimension or linework recovery
- repeated marks and labels
- page metadata

When vision and PDF-native extraction disagree, the system should generally trust the vision-led interpretation more for semantic meaning, while still keeping the conflicting support artifact visible for verification or review.

---

## 4. Major System Parts

The project should be thought of as five cooperating layers.

### 4.1 Orchestration layer

The GPT-5.5 master orchestrator:

- manages the workflow
- issues reading instructions
- decides follow-up actions
- manages artifacts and project memory
- decides when to ask support tools for more evidence
- routes outputs toward synthesis, verification, and review

### 4.2 Reading layer

A set of specialized readers that may include:

- whole-pack reconnaissance readers
- targeted sheet readers
- crop readers
- schedule readers
- detail readers
- verification readers

These are orchestrated, not autonomous in isolation.

### 4.3 Support extraction layer

Optional PDF-native tools for:

- text
- vectors
- schedules
- dimensions
- title blocks
- structural regions

This layer supports the orchestrator when useful.

### 4.4 Synthesis layer

A layer that converts the gathered findings into a neutral internal model describing:

- what objects exist
- what type they are
- how they connect
- what geometry is known
- what geometry is still approximate
- what evidence supports each claim

### 4.5 Review and output layer

A browser-based scene graph and review environment that allows:

- object inspection
- evidence inspection
- uncertainty display
- issue tracking
- override capture
- later export preparation

The output side of the system should evolve through three distinct stages:

1. an interpretive scene graph for low-resolution structural intent
2. a richer Three.js review model with more complete geometry
3. a much later BIM or Revit-oriented export workflow

---

## 5. Shared Memory And Artifact Space

This is a core architectural requirement.

Agents should not pass knowledge mainly through hidden chat state.

They should read from and write to a shared project memory and artifact space.

Typical artifacts may include:

- project manifest
- run manifest
- source document manifest
- page manifest
- image asset manifest
- page atlas
- first-pass pack understanding
- per-sheet reading instructions
- page findings
- region findings
- support extraction artifacts
- unresolved findings log
- conflict register
- interpretation package
- neutral model drafts
- verification reports
- scene graph data
- human review actions
- reviewed model state

The orchestrator should assemble a narrow context package for each task by retrieving the relevant artifacts rather than exposing the entire project state every time.

---

## 6. High-Level Workflow

## Stage 0 - Ingestion And Preparation

### Goal

Accept the drawing pack and prepare the base working materials.

### Inputs

- source files, usually one or more PDFs
- project or run configuration
- source metadata when available

### Outputs

- original source files
- run and project manifests
- source document manifest
- page manifest
- image asset manifest
- rendered page images
- low-resolution page previews for Stage 1
- high-resolution master renders for later crops and targeted reads
- page metadata
- optional title or sheet-number hints when deterministically available
- optional text-layer access
- optional vector availability summary

### Rule

This stage prepares the pack but does not interpret it yet.

### Important notes

Stage 0 should usually be mostly local processing rather than a model-driven reasoning stage.

Its role is to register files, split pages, render imagery, and write manifests and asset references that later stages can consume.

The stage should not collapse the pack into only raster images.

It should preserve multiple useful representations when available, including:

- preview renders
- high-resolution renders
- text-layer availability
- vector availability

These outputs should be written into the shared artifact space for orchestrator use.

They do not all need to be placed into the next model call at once.

In normal operation, Stage 1 should mainly consume the preview set plus page metadata and hints, while the high-resolution render set remains available for later targeted reading.

---

## Stage 1 - Whole-Pack Reconnaissance

### Goal

Use GPT-5.5 vision to perform a first broad understanding pass over the pack.

### Purpose

This stage is for orientation, not deep extraction.

The system should identify:

- what kind of project this appears to be
- what kinds of sheets are present
- which sheets seem important
- which object families seem likely
- where schedules, plans, elevations, sections, notes, and details probably exist
- where uncertainty is already visible

### Inputs

- Stage 0 preparation artifacts
- low-resolution page images or page previews
- high-resolution master renders when needed for the current reconnaissance mode
- page manifest and page metadata
- filenames
- page metadata
- title hints if available

### Outputs

- pack reconnaissance summary
- page atlas
- initial page roles
- initial importance ranking
- early unresolved questions

### Important notes

The long-term architecture should allow the orchestrator to pass only a narrow Stage 0 slice into Stage 1 when that is sufficient.

However, in the current testing mode, Stage 1 may ingest the full Stage 0 preparation set so the workflow can be tested for effectiveness before narrowing is introduced.

That means Stage 1 may currently have access to:

- all page previews
- all high-resolution master renders
- page manifests
- image asset manifests
- page metadata
- title or sheet-number hints
- text-layer and vector-availability summaries

This broader Stage 1 ingestion should be treated as a temporary or configurable operating mode, not a permanent architectural requirement.

---

## Stage 2 - Orchestrator Read-Plan Generation

### Goal

Turn the reconnaissance results into a concrete reading strategy.

### Purpose

The orchestrator should decide:

- what the project probably is
- what information must be collected
- which plan or ground-level sheets should anchor the first spatial understanding pass
- what object families matter most
- which sheets deserve high-resolution follow-up
- whether PDF-native support tools should be invoked
- what each reader should try to return

The orchestrator should also decide:

- which prompt family or template should be used for each task
- what may be inferred versus what must remain unresolved
- what should be surfaced early to human review if ambiguity is already critical

The default reading strategy should usually establish the lowest reliable plan-level spatial organization first, then expand into elevations, sections, details, schedules, and higher-level geometric relationships.

### Outputs

- reading plan
- per-sheet instructions
- crop priorities
- support-tool requests where needed
- initial schema intent and collection goals

---

## Stage 3 - Iterative Targeted Reading

### Goal

Read the relevant pages and regions in detail through orchestrated GPT-5.5 vision loops.

### Purpose

The orchestrator should be able to run iterative reads such as:

- read this plan for major object families
- read this elevation for vertical logic and support relationships
- read this schedule for marks and member descriptions
- read this detail for connectivity and assembly logic
- revisit this region because the first read was incomplete

### Important rule

This stage is iterative by design.

The orchestrator should be able to learn from one read and request another more focused read.

This stage should also:

- refine the orchestrator's understanding of the pack
- establish the base plan-space organization before over-committing to upper or derived geometry
- separate directly read findings from inferred findings
- produce evidence-linked object observations rather than only freeform notes
- request optional support extraction when the vision loop alone is insufficient

### Outputs

- per-sheet findings
- region findings
- object candidates
- relationship candidates
- direct-read observations
- inferred observations
- unresolved notes
- follow-up requests when needed

---

## Stage 4 - Optional PDF-Native Support Extraction

### Goal

Provide structured supporting evidence when the orchestrator decides it will help.

### Purpose

This stage is optional and subordinate to the orchestrator.

It should be callable when useful for:

- schedules
- title blocks
- text layers
- vector geometry
- dimensions
- repeated marks
- clean region parsing

### Important rule

This is not a mandatory backbone stage.

It is a selective support path that can be:

- totally disabled
- disabled
- emphasized
- tuned between tests
- used only for certain sheet types

### Outputs

- support artifacts
- extracted schedule candidates
- text-layer snippets
- vector hints
- dimension candidates
- metadata enrichments

---

## Stage 5A - Coherent Observation Packaging

### Goal

Transform fragmented findings into a coherent, indexed, evidence-linked observation package that is stable enough for synthesis and deterministic enough for software to consume.

### Purpose

This package should be generated by the orchestrator or by a dedicated observation-packaging agent operating under the orchestrator.

This stage is where the system stops holding only scattered findings and starts organizing them into a coherent observation layer.

This is the text-and-package half of the first milestone.

It is not yet the final model-building stage.

Its role is to:

- collect the outputs of prior reading and support stages
- normalize them into a stable observation language
- group related findings without over-resolving them too early
- preserve provenance, confidence, conflict, and unresolved states
- emit a packaging result that Stage 6 can use without having to clean up raw reading noise first

This stage should include agentic behaviour, but not in the form of dumping a giant JSON blob into a single prompt.

Instead, the packaging agent should work through manifests, indexes, and targeted retrieval of relevant observation slices, more like a tool-using inspector than a passive summarizer.

It should be able to:

- inspect the run manifest
- inspect observation indexes
- query only relevant object families, sheet groups, marks, or conflict sets
- follow evidence links
- assemble candidate groups incrementally
- write back a coherent package

It should include:

- pack understanding
- page roles
- relevant object families
- key findings by sheet
- unresolved questions
- evidence references
- structured observations
- freeform findings that do not fit rigid fields yet

It should also include:

- grouped candidate objects
- grouped candidate relationships
- direct-read observations
- derived observations
- inferred observations
- unknown or unresolved observations
- conflict records
- indexes and manifests that let later stages navigate the package deterministically

### Internal subflow

This stage should be understood as a controlled packaging workflow:

1. ingest findings from Stage 3 and Stage 4
2. validate that incoming artifacts match expected structures
3. normalize findings into stable observation templates
4. deduplicate near-identical or overlapping findings
5. cluster related observations into candidate object groups and candidate relationship groups
6. attach evidence references and provenance
7. mark what is direct, derived, inferred, unknown, or blocked by conflict
8. emit a coherent observation package and package manifest

### Important rule

This layer may be flexible and adaptive, but it must remain navigable and deterministic for software.

It is the AI's coherent observation package, not yet the final canonical model.

It should not invent the full downstream contract from scratch.

It should populate versioned output templates and manifests that remain compatible with the downstream scene graph and render layers.

It must not:

- silently discard contradictory findings
- silently upgrade inferred observations into direct facts
- require later stages to parse one giant unstructured JSON blob just to understand what was found

---

## Stage 5B - Visual Interpretation Feedback Board

### Goal

Expose the machine's early interpretation visually so the human is not blind during the first milestone.

### Purpose

This stage should consume the structured understanding produced by Stage 5A and turn it into a low-resolution interpretation board for human steering.

It is not a 3D scene graph.

It is not the neutral model.

It is not the later browser review model.

It exists so the human can see what the system currently believes about the pack before synthesis hardens that understanding into Stage 6.

The board may include artifacts such as:

- key page thumbnails
- highlighted regions
- grouped sheet clusters
- detected object-family hints
- attention maps for unresolved or conflict-heavy areas
- evidence panels tied to the text interpretation

### Important rule

This stage must remain interpretive and low-resolution.

It should help the human steer understanding.

It should not become a premature 3D scene graph.

### Feedback role

Together, Stage 5A and Stage 5B form the first milestone checkpoint.

The human should be able to respond to either or both:

- the structured text-and-package understanding
- the low-resolution visual interpretation board

That feedback should route back into the first loop through the orchestrator.

The first milestone loop should exit only when the human explicitly approves that checkpoint.

The orchestrator should record that human decision and route the next action.

---

## Stage 6 - Neutral Model Synthesis

### Goal

Consume the coherent observation package and build the stable internal model of the project.

### Purpose

This stage is where the system turns coherent observations into the actual neutral model.

Stage 5A makes the evidence coherent.

Stage 5B helps the human see what the machine thinks before synthesis begins.

Stage 6 makes the model.

The neutral model should describe:

- what objects exist
- what each object is
- what connects to what
- what dimensions are known
- what geometry is exact, approximate, or unresolved
- what evidence supports each claim
- what conflicts or ambiguities remain
- what values are direct, derived, inferred, or still unknown

The synthesis stage should consume the coherent observation package from Stage 5A rather than relying on raw page findings as its primary working input.

It should be able to:

- resolve candidate object groups into internal object identities
- resolve candidate relationship groups into internal topology
- assign geometry maturity levels
- keep schematic objects usable even when exact metric values are missing
- preserve unresolved, inferred, and conflicting states explicitly

### Important rule

This is the core internal model of the product.

It should not be tied directly to Revit, Three.js, or a specific export target.

It should be general enough to serve as the bridge between interpretation and downstream outputs.

The neutral model should also preserve a ground-up spatial logic.

Where possible, it should anchor objects first in the lowest reliable plan-level spatial layout and then represent how higher, dependent, or enclosing elements rise from that layout.

The synthesis layer should be able to represent objects that are important semantically even when they are not yet fully geometrically modeled.

For example, the system may know that a toilet, a door, or another placed element exists and where it belongs without yet knowing its final detailed geometry.

This means the neutral model should support semantic placement before full geometric completeness.

---

## Stage 7 - Verification

### Goal

Challenge the synthesized model before presenting it as trustworthy.

### Purpose

Verification agents may inspect:

- whether the evidence actually supports the object
- whether cross-sheet consistency holds
- whether geometry is plausible
- whether schedule-backed facts match model claims
- whether topology is coherent

### Important rule

Verification is a separate stage, not an afterthought.

The system should not rely only on the same agent that built the model to decide that it is correct.

### Outputs

- verification findings
- confidence adjustments
- issue flags
- conflicts requiring review
- review queue items for human or orchestrator follow-up

---

## Stage 8 - Scene Graph Generation

### Goal

Generate a browser-facing scene graph that displays what the AI believes exists in the project.

### Purpose

This stage should consume the Stage 6 neutral model as its structural source and the Stage 7 verification outputs as its trust and issue source.

It should not reinterpret raw reading artifacts as its primary truth.

The scene graph should be able to show:

- objects
- object classes
- approximate or exact geometry
- connectivity
- uncertainty
- evidence links
- issue markers

This first scene graph is primarily interpretive.

It should manifest the model from the ground up.

It should publish verified and, when orchestrator policy allows, provisional model state into a browser-facing graph without hiding unresolved or issue-heavy areas.

In practice, the browser scene should prefer to show the plan-level spatial organization first, then layer upward into vertical structure, enclosure, roof logic, upper levels, and other elevated relationships.

It may use low-resolution geometry such as:

- structural wireframes
- simple member lines
- planar walls
- planar roofs or ceilings
- lightweight placeholders for recognized placed elements

### Important rule

The scene graph should be able to represent partial truth.

If the system only knows something schematically, it should still be displayable as schematic rather than hidden until perfection exists.

Even when geometry is incomplete, the scene graph should still try to preserve the correct spatial logic of what is placed in the ground or floor plan and what rises or depends on it.

If a Stage 6 item is blocked or invalidated by Stage 7, the scene graph should not silently present it as a normal object.

When useful, it may instead publish issue-oriented or missing-coverage markers under orchestrator control.

If a useful pre-modeled lightweight asset exists, such as a simple GLB placeholder for a recognizable object family, the scene graph may reference it as long as the system still preserves what is direct, inferred, and unresolved.

---

## Stage 8A - Detailed Three.js Review Model

### Goal

Build a richer browser model once object identity and core geometry are understood well enough.

### Purpose

This stage deepens the interpretive scene graph into a more complete review model where:

- lines become beams and columns
- walls gain thickness
- surfaces gain more realistic dimensions
- lightweight placeholders may be replaced with richer low-cost geometry
- inferred geometry remains visibly flagged
- missing recognition remains visible to the user

### Important rule

This is still a review model, not yet a BIM authoring model.

It exists to let the user inspect intent, geometry maturity, and unresolved issues more clearly before any export-oriented workflow is attempted.

---

## Stage 9 - Reserved For Future Review-Loop Refinement

### Note

The interpretation-steering role that older versions placed here has been moved upstream into the Stage 5A and Stage 5B milestone loop.

The later human-visible review loop is currently centered on:

- Stage 8 scene graph generation
- Stage 8A richer browser review model
- Stage 10 structured human review actions

This Stage 9 slot is intentionally left open for future refinement once the browser review loop hardens further.

### Rule

Do not use this stage to duplicate Stage 6 synthesis or Stage 10 human review.

---

## Stage 10 - Human Review Of The Scene Graph

### Goal

Allow final inspection and correction of the interpreted model inside the browser review environment.

### Use cases

- inspect objects in 3D
- inspect supporting evidence
- approve or reject AI interpretations
- correct object types
- correct geometry or topology
- record issues and overrides
- approve readiness for downstream use

### Interaction principle

Human communication should not rely only on free chat.

The main review mechanism should be structured actions such as:

- approve
- reject
- mark uncertain
- request reread
- change type
- correct relation
- correct geometry
- confirm inferred value

Natural-language comments may still be allowed, but they should be translated into structured review actions where possible.

### Rule

This is the final trust boundary before later export-oriented workflows.

Verification findings from Stage 7 should feed into this stage as structured review targets rather than as loose commentary.

---

## Stage 11 - Downstream Export Later

### Goal

Use the reviewed neutral model as the basis for export-oriented workflows such as BIM or Revit family placement.

### Important rule

Revit or BIM generation should not be the first internal model.

It should come later, once the system already knows:

- what the objects are
- where they are
- what connects to what
- what dimensions are known
- what family or class they likely correspond to

---

## 7. How The Agents Communicate

The communication model should be:

1. orchestrator decides the task
2. orchestrator retrieves relevant artifacts
3. orchestrator assembles a narrow task context
4. target agent performs the task
5. target agent writes structured outputs and notes back to the project artifact space
6. orchestrator reasons over the results and decides the next action

This means agents communicate primarily through:

- shared artifacts
- retrieved project memory
- structured outputs
- orchestrator routing

They do not depend on a single giant context window as their shared mind.

---

## 8. Schema Strategy

The workflow should distinguish between two output layers.

### 8.1 Flexible interpretation package

This is generated during the orchestrated reading process.

It should be treated as the orchestrator's evolving interpretation workspace rather than as the final model.

It should be semi-structured:

- stable enough for software and agents to navigate deterministically
- flexible enough to hold unusual or pack-specific findings

The package should follow a stable global structure while allowing domain-oriented template modules to activate depending on what type of project the orchestrator believes the document set represents.

This means the package may adapt to project profiles such as:

- warehouse or portal-frame projects
- houses or residential projects
- multi-floor buildings
- broader general structural packs

That adaptation should influence which object families, relations, and follow-up priorities are emphasized, but it should not cause the orchestrator to invent a completely new schema from scratch on every run.

It may include:

- adaptive findings
- pack-specific observations
- freeform insights
- provisional object categories
- collection manifests and read instructions

### 8.2 Stable neutral model contract

This is the core internal output that the product depends on.

It should keep a stable shape around concepts such as:

- object identity
- object type
- spatial anchor in plan
- level or elevation reference when known
- geometry description
- geometry maturity
- topology
- dimensions
- evidence
- uncertainty
- review status

At minimum, the neutral model contract should make it possible to answer:

- what this object is
- where it sits in the project spatially
- what it connects to or depends on
- how complete its geometry currently is
- what evidence supports it
- whether it is direct, derived, inferred, unresolved, or human-corrected

This avoids making the entire product dependent on a fully fluid schema.

### 8.3 Output stages should use stable templates

The downstream output flow should use stable versioned templates rather than unconstrained schema invention.

The main output templates should be:

- interpretation package template
- interpretive scene graph template
- detailed Three.js review model template
- later export template

### 8.4 Canonical schema registry

The project should maintain a top-level canonical schema registry under `Schemas/`.

This registry should define the shared artifact contracts used in the shared artifact space.

It should not try to freeze every temporary internal data structure used inside a stage worker.

Instead:

- every published cross-stage artifact should declare a canonical `schema_id` and `schema_version`
- flexible interpretation artifacts may keep an extension surface for unusual or project-specific findings
- stable downstream artifacts should validate more strictly before publication or state transitions

The first registry wave should cover:

- Stage 0 run and page manifests
- Stage 2 read plans
- common evidence references
- core observations, candidate objects, candidate relationships, conflict records, and unresolved records
- human review actions that affect workflow state
- Stage 6 neutral model manifests, slice results, backbone registries, and core entities
- Stage 7 verification manifests, slice results, issues, findings, confidence adjustments, invalidation recommendations, rerun recommendations, and review-queue items
- Stage 8 scene graph manifests and core publication artifacts

Stage files may still show local examples and build notes, but the registry should be the canonical contract layer for published shared artifacts.

This keeps continuity stable without overspecifying stage-local scratch reasoning too early.

The orchestrator may choose which templates to populate and which optional modules are present, but it should not invent the entire downstream shape from scratch on each run.

---

## 9. Human Review Philosophy

Human feedback should exist in two main places:

1. at the first interpretation milestone, while the system is still organizing understanding
2. after the scene graph and review model have been generated and can be inspected visually

This creates:

- a first milestone interpretation loop around Stage 5A and Stage 5B
- a later browser review and correction loop around Stage 8, Stage 8A, and Stage 10

The first milestone loop should not exit merely because the orchestrator thinks the package is sufficient.

It should exit when the human explicitly approves the Stage 5A and Stage 5B checkpoint.

Inside those human-facing loops, the system may also run the machine-side synthesis and verification loop between Stage 6 and Stage 7.

The project should treat both as first-class parts of the workflow.

The human-facing flow should aim to be structured, organized, and reviewable rather than chat-heavy and chaotic.

---

## 10. First Milestone

The architecture should remain general.

However, the first milestone can still focus on a narrower proof of concept such as:

- structural drawing packs
- primary structural object interpretation
- Stage 5A text-and-package understanding
- Stage 5B low-resolution visual interpretation feedback
- portal-frame or warehouse-style projects as the first test domain
- evidence-linked scene graph generation
- human review in the browser

The POC should prove the workflow, not limit the platform.

---

## 11. Final Workflow Summary

The intended workflow is:

1. ingest the pack
2. prepare the pages and metadata
3. run a whole-pack reconnaissance pass with GPT-5.5 vision
4. let the orchestrator decide how the pack should be read
5. run iterative targeted reads on the important sheets and regions
6. optionally invoke PDF-native support extraction when useful
7. organize findings into a coherent observation package through Stage 5A
8. generate a low-resolution visual interpretation board through Stage 5B
9. record explicit first-milestone human approval or requested corrections and route them back through the interpretation loop when needed
10. synthesize a ground-up neutral model of objects, relationships, spatial anchors, and geometry
11. verify the result through dedicated challenge passes
12. generate a scene graph for browser review
13. deepen that scene graph into a richer browser review model when appropriate
14. accept structured human review actions in the browser loop
15. later use the reviewed neutral model for BIM or Revit-oriented export

This is the core workflow that MainPlan3 establishes.

The guiding idea is simple:

> GPT-5.5 orchestrates the interpretation of the drawing pack, uses vision as its main reading tool, consults PDF-native extraction only when useful, builds a shared artifact-backed understanding of the project, and turns that understanding into a reviewable structural model.
