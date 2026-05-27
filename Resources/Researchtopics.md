# Gemini Research Prompts By Topic For HUGEPROMPT2 Preparation

This file is intentionally split into separate Gemini prompts.

Use one prompt per topic.

The point is to get one deep research document per hard architectural area, not one large mixed report.

## How To Use This File

1. Run one prompt at a time in Gemini.
2. Always attach these common context files:
	 - MainPlan2.md
	 - HUGEPROMPT.md
3. Also attach the topic-specific files listed under each prompt.
4. Ask Gemini to produce one standalone research document per prompt.
5. Keep the research implementation-grade, MVP-scoped, and focused on information flow and interface design.

## Global Bias For Every Prompt

Every prompt below assumes the same project context:

- We are rebuilding an AI-assisted structural drawing interpretation system for structural warehouse drawing packs.
- The old system will be archived.
- The new architecture is:
	1. PDF ingestion
	2. Lightweight sheet classification and labeling
	3. GPT-5.5 image-based pack interpretation producing an initial JSON
	4. Deterministic PDF evidence extraction producing organized JSON artifacts
	5. Agentic synthesis that reads stored JSON artifacts and constructs the neutral model from the ground up
	6. Scene graph output with named elements, dimensions where known, spatial placement, and connectivity
	7. Browser review in Three.js with evidence and uncertainty visible
	8. Human review, structured overrides, and targeted reruns
	9. Future export later, but not part of the current milestone

Every prompt should stay biased toward these rules:

- avoid generic summaries
- avoid generic AI optimism and product language
- avoid deep dives into unrelated future research unless directly useful to MVP
- focus on exact inputs, outputs, interfaces, schemas, IDs, evidence, uncertainty, and rerun behavior
- explain how one stage communicates with the next one
- separate recommendation from unresolved decision
- include tables, schema fragments, and pseudocode where useful

## Prompt 1 - Agent Orchestration And Artifact Graph Architecture

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/AI Structural Model Review Pipeline - Step 9.md
- Resources/PDF Vector and OCR Extraction Pipeline - Step 1.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Agent orchestration and artifact graph architecture for an AI-assisted structural drawing interpretation pipeline.

The system flow is:
1. PDF ingestion
2. Lightweight sheet classification and labeling
3. GPT-5.5 pack interpretation JSON
4. Deterministic evidence bundle JSON
5. Agentic synthesis into a neutral structural model
6. Scene graph output for browser review
7. Human review, overrides, and targeted reruns

Your job is to define exactly how the steps communicate and how the system is orchestrated.

Focus especially on:
- stage lifecycle and ownership
- artifact graph design
- what each stage reads
- what each stage writes
- artifact registration and lookup
- issue records and unresolved records
- rerun dependencies and invalidation rules
- event streaming and status transitions
- auditability and traceability
- agent-to-agent communication through typed artifacts rather than hidden chat memory
- how orchestration should work for MVP without overengineering

I want explicit recommendations for:
- orchestrator responsibilities
- stage state machine
- artifact registry schema
- dependency graph between stages
- invalidation and rerun DAG
- how a stage discovers prior artifacts
- how a failed stage should leave partial outputs
- how review actions should connect back into orchestration

Please structure the document with sections such as:
1. Why this topic is hard
2. Core architectural recommendation
3. Stage inventory and ownership model
4. Artifact families and graph relationships
5. Exact handoffs between stages
6. Storage and indexing model
7. Event and status model
8. Invalidation and rerun protocol
9. Failure modes and anti-patterns
10. MVP implementation recommendation

Include:
- at least one end-to-end sequence diagram in text form
- at least one proposed artifact registry schema
- at least one table mapping stage -> inputs -> outputs -> downstream consumers

Write for engineers defining an execution spec, not for a product audience.
```

## Prompt 2 - Pack Interpretation JSON Design

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/Sheet Classification and Extraction Pipeline - Step 2.md
- Resources/Structural Plan Interpretation Research - 5.md
- Resources/Structural Elevation Resolution Research - Step 6.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Pack interpretation JSON design for the first GPT-5.5 pass over structural drawing packs.

The first deep AI pass reads the pages as images and produces a pack-level interpretation.

This JSON is not the final truth.

It is the first structured hypothesis about:
- what kind of project this is
- what major spaces or functional zones exist
- what structural systems likely exist
- what major element families likely exist
- which pages matter most
- what questions remain unresolved

Your job is to define exactly what this first JSON should look like and what it is allowed or forbidden to claim.

Focus especially on:
- pack-level fields versus page-level fields
- confidence and evidence requirements
- allowable claims versus forbidden claims without deterministic support
- unresolved-question representation
- initial object skeletons and candidate element families
- links to source pages and crops
- how this JSON seeds later deterministic extraction and synthesis
- validation rules for this stage

I want explicit answers to:
- what should this stage claim confidently
- what should it explicitly mark as provisional
- what should it never claim yet
- what exact fields must exist for downstream stages to work
- how this JSON should reference pages, crops, and artifacts
- how a later deterministic stage can confirm or reject these claims

Please structure the document with sections such as:
1. Purpose of the pack interpretation stage
2. Allowed claims and forbidden claims
3. JSON schema proposal
4. Required versus optional fields
5. Evidence and confidence model
6. Unresolved question model
7. Handoff to deterministic evidence extraction
8. Handoff to synthesis
9. Failure modes
10. MVP recommendation

Include:
- a concrete example schema fragment
- one example of a good pack interpretation JSON
- one example of an overreaching or invalid JSON and why it is invalid

Write for engineers defining a stage contract.
```

## Prompt 3 - Deterministic Evidence Bundle JSON Design

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/PDF Vector and OCR Extraction Pipeline - Step 1.md
- Resources/Sheet Classification and Extraction Pipeline - Step 2.md
- Resources/AI for Australian Steel Schedule Extraction - Step 4.md
- Resources/Structural Drawing Reference Framework Research - Step 3.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Deterministic evidence bundle JSON design for structural drawing interpretation.

After the GPT pack interpretation stage, the system runs deterministic PDF processing and must produce organized evidence artifacts.

This bundle should include things like:
- page metadata
- title block fields
- text spans
- OCR support where needed
- crop references
- schedule candidates
- dimension strings
- grids and levels
- vector-layout artifacts
- callouts and references
- unresolved extraction warnings

Your job is to define the evidence bundle as a formal contract that later agents can retrieve and trust.

Focus especially on:
- artifact families inside the evidence bundle
- normalization rules
- evidence provenance
- confidence representation
- page-level versus region-level artifacts
- how deterministic and OCR-derived evidence coexist
- how unresolved regions are preserved
- indexing and lookup for later retrieval

I want explicit recommendations for:
- exact artifact types that must exist
- required fields for each artifact family
- how artifacts link to source PDF, page, bbox, crop, and extraction run
- how bundle-level manifests should work
- how synthesis should query the bundle
- how review should reference individual evidence objects

Please structure the document with sections such as:
1. Why the evidence bundle is a separate layer
2. Artifact family inventory
3. Proposed JSON schemas by artifact type
4. Provenance and traceability rules
5. Confidence and ambiguity representation
6. Indexing and retrieval model
7. Handoff to synthesis and QA
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- a bundle manifest example
- example schemas for at least page, crop, schedule region, dimension artifact, and vector artifact
- a table showing which downstream stages consume which artifact families

Write for engineers defining a deterministic data contract.
```

## Prompt 4 - Neutral Model Construction And Agentic Synthesis Protocol

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/Structural Plan Interpretation Research - 5.md
- Resources/Structural Elevation Resolution Research - Step 6.md
- Resources/Structural Drawing Reference Framework Research - Step 3.md
- Resources/Geometry Solver Research for Structural Drawings - Step 8.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Neutral model construction and agentic synthesis protocol.

This is the hardest stage in the new architecture.

The system already has:
- a pack interpretation JSON from GPT-5.5
- a deterministic evidence bundle JSON

Now an agentic synthesis stage must read those stored artifacts and build the neutral structural model from the ground up.

This stage must:
- retrieve the right slices of context instead of loading everything at once
- establish the usable coordinate framework
- map marks to physical elements
- reconcile plans, elevations, schedules, dimensions, and notes
- build topology and connectivity
- place named objects in space where justified
- preserve unresolved and conflicting interpretations
- decide when it needs targeted follow-up reads

Your job is to define exactly how this synthesis stage should work.

Focus especially on:
- the step-by-step synthesis loop
- retrieval strategy during synthesis
- coordinate-system bootstrap
- plan/elevation/schedule reconciliation
- model maturity levels: semantic, topological, schematic, metric
- handoff from AI-assisted synthesis to deterministic resolution
- how alternatives and unresolved items are preserved
- how the stage commits a structured observation set

I want explicit recommendations for:
- the internal phases of synthesis
- the exact input artifacts consumed at each phase
- the exact outputs produced at each phase
- how the stage asks for more evidence
- how conflicts are represented
- when the stage is allowed to create a model object
- when the stage must stop and leave something unresolved

Please structure the document with sections such as:
1. Why synthesis is the hardest stage
2. Proposed synthesis lifecycle
3. Retrieval and context-selection strategy
4. Coordinate bootstrap protocol
5. Identity and topology construction
6. Conflict and alternative handling
7. Commit protocol for neutral-model observations
8. Handoff to deterministic geometry/QA
9. Failure modes
10. MVP recommendation

Include:
- text pseudocode for the synthesis loop
- one end-to-end worked example
- at least one table mapping synthesis phase -> consumed artifacts -> produced artifacts

Write for engineers defining the core model-building protocol.
```

## Prompt 5 - Stable IDs, Identity Resolution, And Naming Rules

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/AI Structural Model Review Pipeline - Step 9.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Stable IDs, identity resolution, and naming rules for structural elements across the whole pipeline.

The system will have many layers of objects:
- source documents
- pages
- crops
- evidence artifacts
- pack interpretation claims
- synthesized neutral-model objects
- scene graph objects
- review issues and overrides
- future export objects

If identity is not designed properly, the whole pipeline becomes unstable.

Your job is to define a stable ID and naming strategy that survives reruns, partial updates, human review, and future export.

Focus especially on:
- ID namespaces
- deterministic versus generated IDs
- identity resolution across stages
- merge and split behavior
- stable naming for elements like frames, supports, members, bays, footings, braces, and zones
- distinction between display names and canonical IDs
- links between evidence IDs, neutral-model IDs, scene graph IDs, and future export IDs

I want explicit recommendations for:
- ID format by object family
- naming rules by structural object type
- when an object keeps the same ID across reruns
- when an object must get a new ID
- how to preserve traceability through human overrides
- how identity resolution should work when multiple evidence sources point to the same object

Please structure the document with sections such as:
1. Why identity is a system-wide problem
2. Object families and namespaces
3. Stable ID strategy
4. Canonical naming strategy
5. Identity resolution rules
6. Merge/split and rerun behavior
7. Scene graph and export mapping implications
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- concrete ID examples
- a table of object family -> canonical ID pattern -> display-name pattern
- examples of good and bad identity behavior across reruns

Write for engineers defining system-wide object identity.
```

## Prompt 6 - Scene Graph Schema For Three.js Review

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/AI Structural Model Review Pipeline - Step 9.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/Geometry Solver Research for Structural Drawings - Step 8.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Scene graph schema for browser review in Three.js.

The current milestone's main output is a scene graph that can be rendered in the browser and inspected by a human reviewer.

This scene graph must represent:
- named elements
- element type and role
- spatial placement
- connectivity
- evidence references
- uncertainty
- distinction between semantic, topological, schematic, and metric states

Your job is to define the exact scene graph contract that the frontend should consume.

Focus especially on:
- scene node types
- transforms and coordinate conventions
- connectivity representation
- geometry modes
- evidence references on renderable objects
- unresolved and low-confidence state representation
- groupings for frames, bays, supports, surfaces, zones, and issues
- interaction model support: selection, inspection, filtering, issue highlighting

I want explicit recommendations for:
- top-level scene graph shape
- node schemas
- geometry payload formats suitable for browser rendering
- how uncertainty should appear in the scene graph data
- how review actions should reference scene graph objects
- what should be included for MVP and what can wait

Please structure the document with sections such as:
1. Role of the scene graph in the new pipeline
2. Scene graph design principles
3. Proposed schema
4. Geometry modes and object maturity levels
5. Evidence and issue linkage
6. Interaction and selection requirements
7. Performance and payload-size considerations
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- a concrete JSON schema fragment
- one minimal scene graph example
- one richer example with uncertainty and issue references

Write for engineers defining a browser-facing data contract.
```

## Prompt 7 - Human Review, Override Interpretation, And Targeted Rerun Protocol

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/AI Structural Model Review Pipeline - Step 9.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/Geometry Solver Research for Structural Drawings - Step 8.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Human review, override interpretation, and targeted rerun protocol.

The pipeline must support iterative review.

A human reviewer may:
- approve or reject an interpretation
- correct names, placements, or associations
- provide prompt-like natural language feedback
- ask for clarification

The system must translate that review into structured actions and rerun only the necessary stages.

Your job is to define exactly how this review loop should work.

Focus especially on:
- review action schemas
- issue schemas
- override schemas
- natural-language review comment interpretation
- invalidation and targeted reruns
- preserving raw history
- reviewed model versus raw extraction
- how review actions attach to evidence, neutral model objects, and scene graph objects

I want explicit recommendations for:
- what kinds of review actions should exist
- how a free-text review prompt becomes structured data
- what gets invalidated by different kinds of overrides
- how reruns should be targeted
- how accepted overrides should appear in the reviewed model
- what should remain immutable for auditability

Please structure the document with sections such as:
1. Why review is a first-class pipeline layer
2. Review object model
3. Override taxonomy
4. Natural-language to structured-action interpretation
5. Invalidation and targeted rerun rules
6. Reviewed model composition
7. Auditability and history preservation
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- example review action schemas
- example override schemas
- a table showing review action type -> invalidated stages -> rerun policy

Write for engineers defining the human-in-the-loop control layer.
```

## Prompt 8 - Confidence Propagation, Conflict Tracking, And Unresolved-State Handling

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/Geometry Solver Research for Structural Drawings - Step 8.md
- Resources/Structural Elevation Resolution Research - Step 6.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Confidence propagation, conflict tracking, and unresolved-state handling across the pipeline.

The system must not collapse ambiguity or pretend uncertain objects are resolved.

It must preserve:
- confidence per claim or artifact
- conflicts between sources
- alternative hypotheses
- unresolved objects
- reviewed versus unreviewed status

Your job is to define a rigorous model for how uncertainty and conflict should move through the pipeline.

Focus especially on:
- confidence at evidence level
- confidence at synthesized-object level
- conflict objects and alternative sets
- unresolved-state taxonomy
- how confidence should be shown in the scene graph and review UI
- how review affects confidence and conflict records

I want explicit recommendations for:
- confidence fields and scoring model
- whether confidence should be numeric, categorical, or hybrid
- how conflicts should be represented structurally
- how unresolved objects should be stored and surfaced
- how alternative hypotheses should be preserved without exploding complexity
- which validation checks should guard against false certainty

Please structure the document with sections such as:
1. Why uncertainty must be first-class
2. Confidence model
3. Conflict model
4. Alternative hypothesis model
5. Unresolved-state taxonomy
6. Propagation rules across stages
7. Review implications
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- concrete schema fragments
- a table showing how confidence/conflict data changes from evidence -> synthesis -> scene graph -> review
- one example of conflicting evidence handled correctly

Write for engineers defining uncertainty and conflict semantics.
```

## Prompt 9 - Retrieval Over JSON Artifacts And Project-Level RAG Strategy

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/PDF Vector and OCR Extraction Pipeline - Step 1.md
- Resources/Structural Graph Builder Research - Step 7.md
- Resources/Structural Plan Interpretation Research - 5.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Retrieval over JSON artifacts and project-level RAG strategy for the new pipeline.

The system should not send the entire project state into the model every time.

Instead, stages like synthesis and review interpretation should retrieve only the relevant JSON artifacts, evidence objects, issues, and crops needed for the current task.

Your job is to define a practical retrieval strategy for this project.

Focus especially on:
- artifact indexing strategy
- chunking boundaries for JSON artifacts
- metadata-first versus embedding-first retrieval
- page-level, crop-level, object-level, and issue-level retrieval
- context packing into model calls
- retrieval for synthesis versus retrieval for review
- caching and repeat-query behavior
- MVP-suitable storage choices

I want explicit recommendations for:
- what should be indexed
- what should be retrievable as one unit
- how retrieval queries should be composed
- how the system should find the minimum useful context
- how evidence references and object IDs should drive retrieval
- how retrieval quality should be evaluated

Please structure the document with sections such as:
1. Why retrieval is necessary in this pipeline
2. Retrieval object model
3. Indexing strategy
4. Query-planning strategy
5. Context assembly for model calls
6. Retrieval for synthesis
7. Retrieval for review and reruns
8. Failure modes and anti-patterns
9. MVP recommendation

Include:
- one proposed indexing schema
- one example retrieval workflow for synthesis
- one example retrieval workflow for human review feedback

Write for engineers designing project-level retrieval over structured artifacts.
```

## Prompt 10 - Responses API Run Management, Prompt Versioning, Retries, And Auditability

### Recommended Context Files

- MainPlan2.md
- HUGEPROMPT.md
- Resources/AI Structural Model Review Pipeline - Step 9.md
- Resources/Structural Graph Builder Research - Step 7.md

### Copy-Paste Prompt

```text
You are writing one implementation-grade research document for HUGEPROMPT2 preparation.

Topic:
Responses API run management, prompt versioning, retries, and auditability for a multi-stage agentic pipeline.

This system will make many GPT-5.5 calls across many stages.

We need a rigorous operational model for:
- run IDs
- response IDs
- prompt versions
- artifact inputs and outputs
- retries
- caching
- partial failures
- resumability
- cost tracking
- auditability

Your job is to define exactly how model runs should be managed as first-class records.

Focus especially on:
- run-record schema
- relationship between stage runs and model responses
- prompt versioning strategy
- retry policy and retry classification
- idempotency and deduplication
- partial output handling
- traceability between a model response and the artifacts it created
- how reruns should coexist with prior history instead of overwriting it

I want explicit recommendations for:
- database-level object model for runs
- required fields for run records
- versioning rules for prompts and parsers
- retry and backoff policy
- resumability rules
- audit log requirements
- what needs to be visible in the UI for debugging and review

Please structure the document with sections such as:
1. Why run management is critical
2. Proposed run object model
3. Prompt/version model
4. Response tracking model
5. Retry and failure classification
6. Artifact lineage and auditability
7. Caching and idempotency
8. UI/debug implications
9. MVP recommendation

Include:
- one proposed run-record schema
- one example lifecycle of a successful run
- one example lifecycle of a failed and retried run

Write for engineers defining the operational backbone of model execution.
```

## Final Reminder For Every Gemini Run

If Gemini starts drifting into broad summaries, generic AI claims, or unrelated research directions, steer it back to these questions:

1. What exact data object is produced here?
2. What exact next stage consumes it?
3. What fields must be present for that next stage to work?
4. What evidence reference must survive the handoff?
5. What happens if the data is partial, ambiguous, or contradictory?
6. How does a human correction feed back into the pipeline without mutating raw history?
7. What should be rerun, and what should stay cached?

---

## HUGEPROMPT2 Research Guide

This section is a working external guide to the research files currently stored in Resources/HUGEPROMPT2.

The point of this guide is not to repeat each document.

The point is to identify what is actually useful for HUGEPROMPT2, what should be treated as a direct candidate for the new execution prompt, and what should be adapted carefully instead of copied blindly.

### Overall verdict

The research is useful.

It is strongest where it defines contracts, boundaries, object models, stage handoffs, rerun rules, and auditability.

It is weaker where it becomes overly theoretical, too enterprise-specific, or too tied to generic AI architecture language instead of the exact structural drawing workflow we want.

So the right move is not to start over.

The right move is to mine these files selectively and turn the best parts into concrete HUGEPROMPT2 sections.

### File-by-file guide

#### 1. AI Drawing Interpretation Pipeline Architecture.md

Useful material:

- The artifact-centric architecture is one of the best parts of the whole research set.
- The stage ownership model is useful because it makes clear that each stage owns a family of artifacts instead of letting everything write everywhere.
- The artifact registry schema is directly useful for HUGEPROMPT2 because it gives a concrete shape for storing intermediate outputs.
- The exact handoff table between stages is useful because it forces the pipeline to be described as contracts rather than as vague reasoning.
- The stage state machine is useful because it introduces explicit states like queued, processing, validating, awaiting review, completed, and failed.
- The partial output handling and rerun DAG logic are very useful for making the pipeline resumable and auditable.
- The invalidation logic and delta-driven synthesis notes are highly valuable because they explain how we avoid rerunning the whole project when only one part changes.
- The anti-patterns are useful, especially the warning against hidden chat memory and the warning against a god orchestrator.

Use this file for:

- HUGEPROMPT2 pipeline architecture section
- artifact graph and stage contracts
- orchestration rules
- rerun and invalidation logic

Adapt carefully:

- Do not blindly lock into specific infrastructure like Neo4j, Kafka, Temporal, or a Git-native implementation just because the file mentions them.
- Keep the architecture principles, not necessarily all the exact tooling suggestions.

#### 2. GPT-5.5 Structural Pack Interpretation JSON.md

Useful material:

- The allowed claims versus forbidden claims boundary is extremely useful and should become a hard rule in HUGEPROMPT2.
- The idea that the first GPT pass creates a structural hypothesis rather than final truth is exactly right.
- The page atlas concept is one of the most useful outputs described in the file.
- The distinction between required and optional fields is useful because it helps define the minimum viable interpretation JSON.
- The evidence anchor requirement with normalized coordinates is useful and should be kept.
- The confidence tiers are useful as a stage-specific contract.
- The unresolved question model is very useful, especially the categories: missing information, coordination conflict, load path discontinuity, and ambiguity.
- The seed mechanism into deterministic extraction is useful because it explains how the interpretation stage narrows the work for the next stage.
- The staged MVP rollout inside the document is useful because it breaks the first AI pass into atlas, systemic hypothesis, and conflict discovery.

Use this file for:

- the Stage 2 contract in HUGEPROMPT2
- pack interpretation JSON schema
- allowed and forbidden claims rules
- unresolved question output design

Adapt carefully:

- Do not let this stage overreach into exact quantities, exact section sizes, or compliance conclusions.
- The IFC and UniFormat references are useful as future mapping hints, but they are not the core of the current milestone.

#### 3. Deterministic Evidence Bundle for Drawings.md

Useful material:

- This is one of the strongest files in the set.
- The evidence bundle being a separate layer between extraction and synthesis is exactly the right architectural move.
- The artifact family inventory is highly useful because it tells us what the deterministic layer should actually output.
- The page-level versus region-level distinction is important and should be preserved.
- The schema shapes for manifest, page artifacts, crop references, schedule artifacts, dimension artifacts, and vector artifacts are directly useful.
- The normalization rules are very useful, especially coordinate normalization, text normalization, and unit normalization while still preserving the raw string.
- The provenance and traceability rules are strong and should absolutely be reused.
- The unresolved region artifact is a very good concept for handling extraction failures honestly.
- The confidence tiers inside the deterministic layer are useful because they keep extraction quality visible.
- The indexing and retrieval notes are useful, especially spatial indexing plus semantic indexing plus retrieval APIs.
- The deterministic versus OCR coexistence matrix is useful because it explains how to keep both sources without forcing one to dominate.
- The anchor, attribute, and validation query patterns are useful because they suggest how synthesis agents should interact with the bundle.

Use this file for:

- deterministic evidence bundle schema design
- evidence provenance rules
- retrieval contract for downstream agents
- extraction output contracts

Adapt carefully:

- The ISO 19650 and CDE framing is useful for discipline and auditability, but HUGEPROMPT2 should focus on practical contracts rather than enterprise BIM terminology unless it adds real implementation value.

#### 4. Agentic Synthesis Protocol Design.md

Useful material:

- This is probably the most important file in the folder because synthesis is the hardest stage.
- The four-phase synthesis lifecycle is useful: strategic planning, contextual retrieval, structural assembly, and conflict reconciliation.
- The planner-executor plus replanning loop is useful because it avoids pretending synthesis is one single prompt.
- The retrieve-verify-synthesize cycle is useful and should be kept.
- The hierarchical context slicing approach is useful because it reinforces the need to retrieve only the relevant artifacts.
- The coordinate bootstrap protocol is useful because it makes the coordinate system an explicit early task instead of a hidden assumption.
- The notes on identity, topology, and mark-to-schedule mapping are highly relevant.
- The conflict handling section is useful because it clearly states when the system should stop and leave something unresolved.
- The observation schema is valuable because it suggests what the synthesis stage should commit to the neutral model.
- The synthesis loop pseudocode is useful because it gives a good shape for HUGEPROMPT2 execution logic.
- The maturity ladder from semantic to metric is useful and aligns well with the rest of the plan.
- The worked column example is useful because it grounds the abstract protocol in a concrete case.

Use this file for:

- the main synthesis stage specification
- retrieval behavior during synthesis
- neutral model observation schema
- conflict handling rules
- the pseudocode backbone of HUGEPROMPT2

Adapt carefully:

- Some examples are too generic to architecture or too tied to non-structural cases.
- The AutoScale notes about toilets, sinks, and generic floorplan anchors are not central to the warehouse structural problem.
- The references to RL-based conflict resolution and some broad neural architecture claims are not needed for MVP.

#### 5. Pipeline Object Identity and Naming.md

Useful material:

- This file is very useful because stable identity will decide whether the whole pipeline remains coherent after reruns and human review.
- The separation of object families into namespaces is excellent and should be preserved.
- The distinction between evidence-layer IDs, interpretation-layer IDs, neutral-model IDs, and review/export IDs is useful.
- The recommendation to use deterministic IDs for evidence-derived objects is useful.
- The distinction between deterministic IDs and time-ordered generated IDs is useful.
- The insistence on separating canonical IDs from display names is important and should become a hard rule.
- The naming patterns for frames, members, bays, supports, and zones are useful as a structural naming foundation.
- The identity resolution logic based on geometry and evidence fusion is useful.
- The merge, split, and rerun behavior patterns are some of the best parts of the file.
- The survivor, tombstone, parentage, and three-state match patterns are especially useful.

Use this file for:

- HUGEPROMPT2 identity strategy
- naming rules
- rerun-stability rules
- merge and split behavior

Adapt carefully:

- The U.S. National CAD Standard examples are useful structurally, but we should not blindly adopt their naming vocabulary if it clashes with Australian practice or our own internal naming logic.
- Keep the layered naming strategy and the ID philosophy, not necessarily every literal example.

#### 6. Human Review Protocol for AI Extraction.md

Useful material:

- This file is very useful and lines up well with what the product needs.
- The idea that review is a first-class pipeline layer, not just a UI afterthought, is exactly right.
- The review object model is useful because it formalizes the data structures around review.
- The distinction between evidence-level, neutral-model-level, and scene-graph-level review attachment is very good.
- The override taxonomy is useful because it distinguishes attribute, association, and schema-level changes.
- The issue schema is useful and should likely be adapted into the project.
- The natural-language to structured-action flow is useful because it matches the desired prompt-like reviewer feedback.
- The invalidation and targeted rerun rules are highly valuable and should be preserved.
- The review-action-to-rerun table is especially useful.
- The overlay pattern for reviewed model composition is very strong and should definitely be kept.
- The rescued-data idea is useful for preserving reviewer input that does not fit the current schema cleanly.
- The immutable audit trail requirements are good and should be reused.
- The failure modes around cognitive load, limbo states, and brittle overrides are useful design warnings.

Use this file for:

- the human review and overrides section of HUGEPROMPT2
- structured review action schema
- review-to-rerun invalidation rules
- reviewed model composition rules

Adapt carefully:

- The generic HITL references are fine, but the important part is the override object model and rerun protocol, not the framework-specific examples.
- Do not let the review layer become too heavy for MVP.

#### 7. Scene Graph Contract for Browser Review.md

Useful material:

- This file is useful because it treats the scene graph as a real contract rather than a rendering afterthought.
- The top-level scene graph shape is useful and should be adapted.
- The node schema is useful, especially the separation between transform, states, uncertainty, geometry, and evidence.
- The decision to represent connectivity as first-class edges rather than only parent-child hierarchy is very useful.
- The object maturity levels are useful because they map well to semantic, topological, schematic, and metric states.
- The geometry payload strategy is useful, especially the distinction between lightweight browser payloads and heavier geometry blobs.
- The explicit separation between metric, semantic, topological, and schematic state layers is very valuable.
- The evidence and issue linkage section is useful, especially the idea that a scene object should point back to evidence and issues.
- The BCF-compatible issue pinning and stored viewpoints are useful.
- The filtering rules by maturity, uncertainty, group, and issue status are directly helpful for the review UI.
- The performance advice is useful, especially splitting graph structure from geometry blobs, using instancing, and disposing Three.js resources correctly.

Use this file for:

- the browser scene graph contract
- review viewer behavior
- issue linkage in 3D
- frontend performance rules

Adapt carefully:

- The digital twin framing is conceptually useful, but HUGEPROMPT2 should stay grounded in the actual review product we are building now.
- Some of the industrial sensor and semantic twin language is broader than the current milestone.

#### 8. Uncertainty and Conflict Pipeline Model.md

Useful material:

- This file is conceptually strong and should influence HUGEPROMPT2, even if the final implementation is simpler than the full theory described here.
- The central principle that uncertainty, conflict, and unresolved states must be first-class is exactly right.
- The distinction between evidence-level and synthesized-object-level confidence is useful.
- The conflict object model is very useful and should likely be adapted almost directly.
- The idea of keeping archived claims instead of deleting losing interpretations is very good.
- The alternative hypothesis model is useful, especially the recommendation to use local scoping instead of global branching.
- The taxonomy of unresolved states is very useful because it gives a better language than simply saying low confidence.
- The propagation table across pipeline stages is useful and should influence data design.
- The collapse mechanism notes are important because they explicitly warn against throwing away upstream uncertainty when mapping into discrete objects.
- The human review effect on the epistemic model is useful and fits well with the review protocol document.
- The validation checks such as tension gates and vacuity alarms are useful.

Use this file for:

- the uncertainty and conflict semantics section of HUGEPROMPT2
- unresolved-state taxonomy
- conflict object design
- review escalation rules

Adapt carefully:

- The full Subjective Logic math may be too heavy for MVP implementation.
- The best use is to take the conceptual structure and simplify it into a practical schema if needed.
- JSON-LD is optional; the important part is the semantics, not the specific serialization choice.

#### 9. LLM Pipeline Run Management Design.md

Useful material:

- This file is operationally very useful and gives the missing execution backbone for a multi-stage pipeline.
- The run versus span hierarchy is useful and should be kept.
- The run record field list is highly useful and concrete.
- The prompt and parser versioning rules are very useful and should become part of HUGEPROMPT2.
- The requirement to bind prompts and parsers together is especially important.
- The response tracking model is useful because it captures token usage, finish reasons, reasoning tokens, and partial outputs.
- The cost tracking logic is useful because this pipeline could become expensive quickly.
- The error classification and retry policy are useful and should be adapted.
- The reflexive retry pattern is useful for schema or validation failures.
- The idempotency and deduplication notes for tool calls are important.
- The artifact lineage rules are very useful and fit well with the artifact graph architecture.
- The caching and resumability sections are useful.
- The UI and debugging requirements are useful because they define what operators need to see when the system misbehaves.
- The successful and failed run examples are useful because they make the operational model concrete.

Use this file for:

- run management and observability sections in HUGEPROMPT2
- prompt versioning rules
- retry policies
- resumability and traceability design

Adapt carefully:

- The specific stack suggestions like PostgreSQL plus ClickHouse plus OpenTelemetry are good references, but HUGEPROMPT2 should describe the required operational capabilities first and only then choose tools.

### Cross-file notes

### Previous Resources Guide

This subsection covers the research files that already existed in Resources before the new HUGEPROMPT2 batch.

Only the files still active in Resources should be treated as part of the core source set for HUGEPROMPT2.

These older files are not the best source for the new orchestration and artifact-driven architecture, but they are still very useful for domain logic, structural conventions, deterministic reasoning, and browser review behavior.

The practical rule is:

- use the HUGEPROMPT2 files for the new architecture, contracts, reruns, identity, uncertainty, and scene graph semantics
- use the older Resources files for structural-domain logic, coordinate reasoning, schedule logic, topology interpretation, geometry generation, and review behavior

Explicit scope rule:

- anything in Resources/archive is out of scope for the solid HUGEPROMPT2 source set unless a very specific blocker forces us to consult it later

#### Older Resources still active in Resources

##### Structural Drawing Reference Framework Research - Step 3.md

Useful material:

- This file is still very useful for the coordinate and reference side of the project.
- The grid marking, level, RL, pitch, and slope conventions are directly relevant to the new synthesis stage.
- The dimension graph discussion is useful because we still need deterministic coordinate reasoning after AI interpretation.
- The fragmented dimension chain and cycle-detection ideas are useful for real drawing packs.
- The dependency-aware coordinate architecture and multi-sheet alignment ideas are highly relevant.
- The evidence traceability perspective in this file still matches the new architecture well.

Use this file for:

- coordinate bootstrap logic
- reference framework extraction rules
- dimension-chain reconciliation
- multi-sheet spatial alignment

Adapt carefully:

- Some advanced AI sections in the file, like GNN and diffusion references, are future research and not core to MVP.

##### AI for Australian Steel Schedule Extraction - Step 4.md

Useful material:

- This file is still useful because schedules remain one of the main deterministic evidence sources in the new pipeline.
- The schedule region detection logic is useful.
- The parsing of steel notation, hot-rolled sections, welded sections, purlins, and girts is directly useful.
- The distinction between project marks and catalog sections is very important.
- The validation rules for schedule data are still highly relevant.
- The confidence and revision reconciliation parts are useful for the new deterministic evidence layer.

Use this file for:

- schedule evidence extraction
- mark-to-section mapping
- schedule validation rules
- steel notation normalization

Adapt carefully:

- The file is written with more emphasis on direct extraction than on the newer artifact bundle contract, so use the domain logic while shaping the outputs according to the new evidence-bundle design.

##### Structural Plan Interpretation Research - 5.md

Useful material:

- This file remains useful for understanding how structural plans communicate topology.
- Portal frame and bay detection logic is still directly relevant.
- The purlin, girt, and bracing logic remains useful for later synthesis and geometry stages.
- Footing plan and foundation topology notes are useful for expanding beyond the first portal-frame-only focus.
- Symbolic zone detection, openings, and office-area notes are useful because the new pack interpretation stage explicitly wants general building understanding.
- The plan-to-elevation interface material is still very useful.
- The data serialization and evidence traceability sections are still relevant.

Use this file for:

- plan topology interpretation
- bay logic and frame placement reasoning
- secondary structural system rules
- plan-to-elevation correlation
- structural zones and openings

Adapt carefully:

- The file leans more toward the older deterministic extraction framing, so use it mainly for structural interpretation logic rather than for new pipeline contracts.

##### Structural Elevation Resolution Research - Step 6.md

Useful material:

- This file is still strongly relevant because elevations remain one of the core evidence sources for frame templates and vertical constraints.
- Portal frame type detection remains useful.
- Grid mapping between plan and elevation is directly useful.
- Level, RL, datum, pitch, and slope extraction remain important.
- Column, rafter, haunch, ridge, canopy, and secondary roof notes are still useful.
- Member label association in elevations is still highly relevant.
- The data models, JSON schemas, and downstream handoff notes remain useful.
- The handling of missing or conflicting vertical data is still important.

Use this file for:

- elevation evidence extraction
- plan-to-elevation linking
- vertical constraint logic
- portal frame template definition
- conflict handling around heights and roof form

Adapt carefully:

- Keep the engineering logic, but express the outputs using the newer artifact, synthesis, and uncertainty models.

##### Structural Graph Builder Research - Step 7.md

Useful material:

- This file is still one of the most valuable from the older set.
- It remains highly useful for structural object taxonomy, symbolic graph structure, connection semantics, template instantiation, schedule-to-member resolution, identity resolution, repeated-system rules, and evidence propagation.
- The connection between symbolic nodes, reference framework, and later geometry is still directly relevant.
- The confidence, provenance, alternatives, and unresolved-object sections still map well to the new architecture.
- The handoff notes to geometry and browser review are still useful.

Use this file for:

- neutral model object taxonomy
- connection and topology semantics
- repeated-system logic
- schedule-to-member linking
- graph-to-geometry handoff

Adapt carefully:

- Some of its architecture language overlaps with the new HUGEPROMPT2 graph and synthesis research; in those cases, prefer the newer HUGEPROMPT2 contracts for orchestration and use this older file for domain graph logic.

##### Geometry Solver Research for Structural Drawings - Step 8.md

Useful material:

- This file is still very useful for the deterministic post-synthesis layer.
- Coordinate synthesis, grid-to-world mapping, level solving, datum reconciliation, and portal frame instantiation are all relevant.
- Member centerline generation logic is still useful.
- Roof and wall plane construction, purlin and girt generation, bracing geometry, footing logic, canopy logic, and partial geometry handling all remain useful.
- The constraint graph, propagation, tolerance, and conflict visualization ideas remain helpful.
- The browser-ready geometry format notes are still useful.

Use this file for:

- deterministic geometry resolution
- schematic and metric geometry generation
- procedural secondary system generation
- tolerance rules and conflict visualization
- browser-ready geometry payload design

Adapt carefully:

- Keep the deterministic geometry and constraint-solving content.
- Deprioritize any future export or advanced enhancement sections that are not needed for the current milestone.

##### AI Structural Model Review Pipeline - Step 9.md

Useful material:

- This file is still very useful for the review-side product behavior.
- The frontend architecture notes are still useful.
- The browser-ready geometry data model and structural visualization strategies remain relevant.
- Grid, level, label, surface, zone, and footing visualization are all still useful.
- It helps define what the reviewer should be able to see and inspect.

Use this file for:

- browser review UI behavior
- structural visualization patterns
- evidence-centered inspection behavior
- rendering considerations for different structural families

Adapt carefully:

- Prefer the newer scene graph contract file for the formal backend-to-frontend data contract.
- Use this older file more for viewer behavior, inspection behavior, and UX expectations.

The strongest reusable themes across the whole HUGEPROMPT2 research folder are:

- everything important should move through typed, versioned artifacts
- every stage should have a strict contract with exact inputs and outputs
- GPT interpretation should remain hypothesis-driven, not truth-claiming
- deterministic evidence should stay separate from synthesis
- synthesis should retrieve scoped context, not the whole project state
- stable IDs and naming are system-critical, not a later cleanup task
- uncertainty, conflicts, and unresolved states should remain visible in the data model
- human review should be an overlay layer with targeted reruns, not destructive mutation
- the browser scene graph must expose evidence, uncertainty, and issues directly
- run management, prompt versioning, and auditability are necessary from the start

### What to be careful not to copy blindly into HUGEPROMPT2

- overly academic framing where a simpler engineering rule would do
- references to tools or infrastructure that may be unnecessary for MVP
- mathematically elegant confidence systems that add too much implementation burden early
- generic AI-agent language that does not improve the actual structural drawing workflow
- broad digital twin language that goes beyond the current review-model milestone

### Practical recommendation for the next phase

When drafting HUGEPROMPT2, these nine files should not be merged blindly.

They should be mined into a smaller number of execution sections:

1. Core architecture and orchestration
2. Pack interpretation contract
3. Deterministic evidence contract
4. Synthesis protocol
5. Identity and naming rules
6. Uncertainty and conflict semantics
7. Scene graph contract
8. Review and rerun control layer
9. Run management and observability

That restructuring will preserve the best content while removing repetition and theoretical drift.