# Research Notes For MainPlan3 And Future HugePrompt3

## 0. Purpose

This document maps the current research corpus to the stage structure in MainPlan3.

Its job is not to restate MainPlan3.

Its job is to show which source documents are most useful for each stage, what they contribute, which ones should be treated as core versus optional support, and where MainPlan3 intentionally reframed older assumptions.

This should be the working bridge between:

- MainPlan3 as the workflow contract
- the research corpus in Resources
- the methodology baseline in openai_vision_skills
- the later authoring of HugePrompt3

## 1. Reading Key

- Core: directly shapes the stage contract and should materially influence HugePrompt3.
- Support: useful implementation help, but not the primary logic of the stage.
- Guardrail: mostly useful for constraints, validation, or failure handling.
- Reframed by MainPlan3: useful, but MainPlan3 changes its architectural weight or placement.

## 2. Source Index

| Source | Primary stage alignment | Main contribution | Status in MainPlan3 |
| --- | --- | --- | --- |
| openai_vision_skills/README.md | 1, 2, 3, 4 | Establishes that engineering drawings need a different treatment from ordinary documents | Core baseline |
| openai_vision_skills/skills/engineering-drawing-vision.md | 1, 2, 3, 7, 10 | Full-sheet plus crop reading, evidence discipline, visible vs inferred separation | Core baseline |
| openai_vision_skills/skills/openai-model-calls.md | 0, 2, 3, 5, 7 | Responses API discipline, model presets, structured outputs, versioned prompts, run traceability | Core baseline |
| openai_vision_skills/skills/vision-document-pipeline.md | 1, 4 | Useful mainly as contrast with ordinary document pipelines | Guardrail |
| Resources/AI Drawing Interpretation Pipeline Architecture.md | 0, 2, 4, 5, 7, 9 | Artifact graph, stage ownership, DAG invalidation, partial outputs, auditability | Core |
| Resources/Agentic Synthesis Protocol Design.md | 2, 3, 5, 6, 7 | Plan-and-execute synthesis, observation commits, conflict registry, targeted follow-up reads | Core |
| Resources/GPT-5.5 Structural Pack Interpretation JSON.md | 1, 2, 3, 5 | Defines what the first pack-level interpretation is allowed to claim | Core |
| Resources/LLM Pipeline Run Management Design.md | 0, 2, 3, 4, 5, 7, 9, 10 | Run IDs, spans, artifact lineage, retries, caching, observability, rerun control | Core |
| Resources/Sheet Classification and Extraction Pipeline.md | 0, 1, 2, 4 | Sheet role hints, title block handling, candidate region discovery | Core support |
| Resources/PDF Vector and OCR Extraction Pipeline.md | 0, 4, 5 | Deterministic PDF parsing, OCR layering, vector-first extraction, region artifacts | Core support |
| Resources/AI for Australian Steel Schedule Extraction.md | 3, 4, 5, 6, 7 | Schedule extraction discipline, row-cell evidence, mark capture, validation patterns | Core support |
| Resources/Structural Drawing Reference Framework Research.md | 3, 4, 5, 6, 7, 8 | Grids, levels, dimensions, viewport reference system, geometric anchors | Core |
| Resources/Structural Plan Interpretation Research.md | 3, 5, 6, 7, 8 | Plan-grounded topology, object families, bay logic, openings, footings | Core |
| Resources/Structural Elevation Resolution Research.md | 3, 5, 6, 7, 8 | Vertical resolution, frame templates, levels, roof pitch, plan-to-elevation linking | Core |
| Resources/Structural Graph Builder Research.md | 5, 6, 7, 8, 10, 11 | Symbolic graph, identity, topology, evidence propagation, merge logic | Core |
| Resources/Geometry Solver Research for Structural Drawings.md | 6, 7, 8A, 11 | Deterministic geometry solving once enough structural facts exist | Support |
| Resources/Deterministic Evidence Bundle for Drawings.md | 4, 5, 7, 10 | Immutable evidence contract, artifact families, provenance, unresolved-region handling | Core |
| Resources/Pipeline Object Identity and Naming.md | 5, 6, 8, 8A, 10, 11 | Stable IDs, canonical names, merge/split behavior, rerun stability | Core |
| Resources/Uncertainty and Conflict Pipeline Model.md | 5, 6, 7, 8, 10 | First-class conflict objects, unresolved states, confidence propagation | Core |
| Resources/Scene Graph Contract for Browser Review.md | 8, 8A, 10, 11 | Browser-facing semantic scene graph, evidence links, review states, issue markers | Core |
| Resources/AI Structural Model Review Pipeline.md | 8A, 10, 11 | Three.js review model requirements, rendering strategy, staged browser review workflow | Core support |
| Resources/Human Review Protocol for AI Extraction.md | 7, 9, 10 | Structured overrides, targeted invalidation, review state machine, audit trail | Core |
| Resources/Researchtopics.md | all | Topic inventory and research partitioning, useful as planning metadata only | Meta only |

## 3. Stage-By-Stage Mapping

### Stage 0 - Ingestion And Preparation

#### Core references

- LLM Pipeline Run Management Design.md
- Sheet Classification and Extraction Pipeline.md
- PDF Vector and OCR Extraction Pipeline.md
- openai-model-calls.md

#### What these sources contribute

- Stage 0 needs a run container, artifact lineage, and repeatable capture of source-file metadata before any interpretation starts.
- Sheet classification research gives the most useful early preparation targets: title blocks, page labels, candidate sheet roles, and region seeds.
- PDF vector/OCR research supplies the preparation-side decision that page imagery, text layers, and vector availability should all be recorded separately instead of collapsed.
- openai-model-calls.md matters here because later prompt/version traceability must begin at ingestion, not halfway through the run.

#### What HugePrompt3 should carry forward

- Require a project manifest and run manifest before any agentic reading begins.
- Record which page representations are available: raster preview, high-resolution render, embedded text, vector traces.
- Treat sheet-role hints as preparation metadata, not as final truth.

#### Reframing notes

- MainPlan3 keeps this stage non-interpretive. Classification hints are useful, but they should not hard-lock page meaning before Stage 1 and Stage 2.

### Stage 1 - Whole-Pack Reconnaissance

#### Core references

- engineering-drawing-vision.md
- openai_vision_skills/README.md
- GPT-5.5 Structural Pack Interpretation JSON.md
- Sheet Classification and Extraction Pipeline.md

#### Support and guardrail references

- vision-document-pipeline.md

#### What these sources contribute

- engineering-drawing-vision.md gives the right reconnaissance behavior: broad whole-sheet reading first, then progressive narrowing, while keeping coordinate traceability.
- The skills README reinforces that engineering packs are not ordinary business documents and should not be summarized as if they were.
- GPT-5.5 Structural Pack Interpretation JSON.md is the clearest source for what Stage 1 should emit: page atlas, page roles, candidate object families, major unknowns, and early pack hypotheses.
- Sheet classification research helps bootstrap likely plan, elevation, schedule, and detail pages.

#### What HugePrompt3 should carry forward

- Stage 1 is for orientation and hypothesis seeding, not final extraction.
- The first structured output should explicitly include unresolved questions and page-priority ranking.
- Pack-level claims should stay broad: project type, sheet families, likely structural systems, high-value pages.

#### Reframing notes

- MainPlan3 rejects a pure vision-first ideology. Vision is still the main sensing tool here, but the stage exists inside an orchestrated workflow, not as the whole architecture.
- vision-document-pipeline.md is mainly useful as a reminder of what not to do: do not flatten engineering drawings into ordinary OCR-first document summaries.

### Stage 2 - Orchestrator Read-Plan Generation

#### Core references

- AI Drawing Interpretation Pipeline Architecture.md
- Agentic Synthesis Protocol Design.md
- GPT-5.5 Structural Pack Interpretation JSON.md
- LLM Pipeline Run Management Design.md
- openai-model-calls.md

#### What these sources contribute

- AI Drawing Interpretation Pipeline Architecture.md gives the best stage-ownership and artifact-routing model for turning reconnaissance into an execution plan.
- Agentic Synthesis Protocol Design.md provides the most useful pattern for converting questions into targeted reading tasks and observation-commit loops.
- GPT-5.5 Structural Pack Interpretation JSON.md defines the minimum fields the read-plan should consume from Stage 1.
- Run management and model-call guidance ensure the read-plan is traceable, versioned, and reproducible.

#### What HugePrompt3 should carry forward

- The orchestrator should generate a typed read plan, not a loose narrative.
- The read plan should choose plan-anchor sheets first, then elevation/section/schedule/detail follow-up.
- Each task should specify prompt family, target sheets or crops, expected output shape, and escalation rule.

#### Reframing notes

- Older material sometimes blurs planning and synthesis. MainPlan3 keeps Stage 2 strictly as planning and routing, not object creation.

### Stage 3 - Iterative Targeted Reading

#### Core references

- engineering-drawing-vision.md
- Structural Plan Interpretation Research.md
- Structural Elevation Resolution Research.md
- Structural Drawing Reference Framework Research.md
- AI for Australian Steel Schedule Extraction.md
- Agentic Synthesis Protocol Design.md

#### Support references

- GPT-5.5 Structural Pack Interpretation JSON.md
- openai-model-calls.md

#### What these sources contribute

- engineering-drawing-vision.md defines the core read loop: whole context, targeted crops, evidence-linked claims, and separation of seen versus inferred.
- Plan interpretation research is the main source for ground-up spatial reading: bays, frames, openings, secondary members, and footing logic.
- Elevation resolution research adds the vertical complement: column heights, roof pitch, ridge/eaves logic, and frame templates.
- Reference framework research supplies the spatial scaffolding that lets plans, elevations, sections, and details be reconciled rather than read as isolated fragments.
- Schedule extraction research covers how marks, sizes, schedules, and labels can be read without losing evidence pointers.
- Agentic Synthesis Protocol Design.md is important here because Stage 3 is iterative by design; the orchestrator should be allowed to ask more focused questions after each read.

#### What HugePrompt3 should carry forward

- The default ordering should remain plan-space first, then vertical and relational follow-up.
- Targeted readers should emit observation objects, not just prose summaries.
- Every observation should distinguish direct-read, derived-from-explicit-evidence, inferred, or unresolved.

#### Reframing notes

- MainPlan3 elevates ground-up plan reasoning more strongly than the older docs did. That bias should remain explicit in HugePrompt3.

### Stage 4 - Optional PDF-Native Support Extraction

#### Core references

- Deterministic Evidence Bundle for Drawings.md
- PDF Vector and OCR Extraction Pipeline.md
- Sheet Classification and Extraction Pipeline.md
- AI for Australian Steel Schedule Extraction.md
- Structural Drawing Reference Framework Research.md

#### What these sources contribute

- Deterministic Evidence Bundle for Drawings.md is the cleanest statement of what the support layer should emit when invoked: page artifacts, crop refs, schedule artifacts, dimension artifacts, vector artifacts, unresolved regions, provenance.
- PDF Vector and OCR Extraction Pipeline.md gives the operational detail for vector-first parsing plus OCR fallback.
- Sheet classification research helps support-tool routing by identifying where schedule regions, title blocks, and candidate detail zones exist.
- The schedule extraction and reference framework research show where deterministic support is strongest: grids, levels, dimensions, labels, tables, repetitive marks.

#### What HugePrompt3 should carry forward

- Support extraction should be callable selectively by sheet type or question type.
- It should emit evidence artifacts that later stages can query directly.
- Unresolved regions must remain explicit artifacts rather than silent failure.

#### Reframing notes

- This is the clearest place where MainPlan3 changes the older architecture. Deterministic extraction is still valuable, but it is not the backbone. It is an optional support path under orchestrator control.

### Stage 5A - Coherent Observation Packaging

#### Core references

- AI Drawing Interpretation Pipeline Architecture.md
- Agentic Synthesis Protocol Design.md
- Deterministic Evidence Bundle for Drawings.md
- Uncertainty and Conflict Pipeline Model.md
- Pipeline Object Identity and Naming.md
- Structural Graph Builder Research.md

#### Support references

- GPT-5.5 Structural Pack Interpretation JSON.md
- LLM Pipeline Run Management Design.md

#### What these sources contribute

- AI Drawing Interpretation Pipeline Architecture.md gives the artifact-graph and validation mindset needed to turn scattered findings into a stable package.
- Agentic Synthesis Protocol Design.md adds the concept of observation commits, conflict registry, and targeted retrieval instead of one giant synthesis prompt.
- Deterministic Evidence Bundle for Drawings.md contributes the artifact families and provenance rules that make the package inspectable.
- Uncertainty and Conflict Pipeline Model.md is essential because Stage 5 should preserve conflict and unresolved state rather than prematurely forcing resolution.
- Pipeline Object Identity and Naming.md matters here because candidate objects and relationships need stable intermediate identities before final neutral-model resolution.
- Structural Graph Builder Research.md contributes grouping logic for candidate entities, relations, and evidence propagation.

#### What HugePrompt3 should carry forward

- Stage 5A should be an explicit package-building stage, not a side effect of Stage 6.
- The output should include manifests, indexes, grouped candidate objects, grouped candidate relationships, evidence links, and conflict records.
- This stage should normalize and cluster, but should not over-resolve.

#### Reframing notes

- MainPlan3 keeps observation packaging separate from neutral-model synthesis, and now treats that package as the first half of a combined Stage 5A and Stage 5B milestone.

### Stage 5B - Visual Interpretation Feedback Board

#### Core references

- Human Review Protocol for AI Extraction.md
- AI Drawing Interpretation Pipeline Architecture.md
- Deterministic Evidence Bundle for Drawings.md
- Uncertainty and Conflict Pipeline Model.md
- Scene Graph Contract for Browser Review.md

#### Support references

- AI Structural Model Review Pipeline.md
- LLM Pipeline Run Management Design.md

#### What these sources contribute

- Human Review Protocol for AI Extraction.md contributes the structured review-action model needed so early human steering writes back into artifacts rather than dissolving into chat.
- AI Drawing Interpretation Pipeline Architecture.md contributes the invalidation and rerun framing needed to route Stage 5B feedback back into Stage 2, Stage 3, Stage 4, or Stage 5A.
- Deterministic Evidence Bundle for Drawings.md provides the evidence-linking rules needed for thumbnails, overlays, and review panels to stay traceable.
- Uncertainty and Conflict Pipeline Model.md matters because the board should highlight unresolved and conflict-heavy regions instead of hiding them.
- Scene Graph Contract for Browser Review.md is relevant as a contrast boundary: Stage 5B should borrow reviewability ideas without becoming the later browser scene graph.

#### What HugePrompt3 should carry forward

- Stage 5B should make the first milestone visually legible before synthesis begins.
- It should stay low-resolution and evidence-linked.
- It should publish structured feedback targets that route back into the interpretation loop.

#### Reframing notes

- MainPlan3 now treats the first human loop as a combined Stage 5A and Stage 5B milestone rather than a late interpretation-feedback stage.

### Stage 6 - Neutral Model Synthesis

#### Core references

- Structural Graph Builder Research.md
- Structural Plan Interpretation Research.md
- Structural Elevation Resolution Research.md
- Structural Drawing Reference Framework Research.md
- Agentic Synthesis Protocol Design.md
- Pipeline Object Identity and Naming.md
- Uncertainty and Conflict Pipeline Model.md

#### Support references

- Geometry Solver Research for Structural Drawings.md
- AI for Australian Steel Schedule Extraction.md

#### What these sources contribute

- Structural Graph Builder Research.md is the central model-building source: symbolic graph construction, hybrid component-plus-relationship modeling, evidence propagation, merge logic.
- Plan interpretation and elevation resolution research provide the concrete semantics needed to instantiate spatial topology and vertical structure.
- Reference framework research supplies the coordinate and datum system that makes the model spatially coherent.
- Agentic Synthesis Protocol Design.md provides the stepwise retrieval-and-commit loop for synthesis rather than a monolithic pass.
- Identity and uncertainty research ensure that object creation, conflict handling, and reruns stay stable.
- Geometry solver research becomes relevant once enough facts exist to upgrade from semantic placement into more deterministic geometry.

#### What HugePrompt3 should carry forward

- Neutral-model creation should begin from plan-grounded spatial anchors and then extend upward.
- The model must support semantic placement before full metric completeness.
- Geometry maturity should stay explicit: schematic, approximate, metric, unresolved.
- Conflicts and alternatives should stay represented as first-class model state.

#### Reframing notes

- MainPlan3 keeps the neutral model independent from Three.js and Revit. Geometry solver work should therefore be attached to neutral-model enrichment, not treated as the model itself.

### Stage 7 - Verification

#### Core references

- Uncertainty and Conflict Pipeline Model.md
- Deterministic Evidence Bundle for Drawings.md
- Human Review Protocol for AI Extraction.md
- Structural Graph Builder Research.md
- LLM Pipeline Run Management Design.md

#### Support references

- Geometry Solver Research for Structural Drawings.md
- engineering-drawing-vision.md

#### What these sources contribute

- Uncertainty and conflict research gives the strongest framework for challenge passes, unresolved-state taxonomy, tension scoring, and conflict objects.
- Deterministic evidence bundle design ensures verification can trace every claim back to source evidence instead of merely rephrasing model outputs.
- Human Review Protocol for AI Extraction.md matters even before human review because it defines issue objects, invalidation rules, and rerun boundaries.
- Structural Graph Builder Research.md helps verify topological coherence and evidence propagation.
- Run management research is required so verification findings can feed structured rerun queues.

#### What HugePrompt3 should carry forward

- Verification must be a separate challenge stage with its own outputs.
- Verification outputs should include issue flags, confidence adjustments, contradiction records, and rerun recommendations.
- A failing verification should invalidate only the dependent slice when possible.

#### Reframing notes

- MainPlan3 strengthens verification as its own stage rather than burying it inside review or model synthesis.

### Stage 8 - Scene Graph Generation

#### Core references

- Scene Graph Contract for Browser Review.md
- Structural Graph Builder Research.md
- Structural Plan Interpretation Research.md
- Structural Elevation Resolution Research.md
- Structural Drawing Reference Framework Research.md
- Uncertainty and Conflict Pipeline Model.md

#### What these sources contribute

- Scene Graph Contract for Browser Review.md is the primary source here: semantic scene graph structure, evidence references, review states, issue links, and browser-facing representations.
- Structural graph builder research defines how neutral-model objects and relationships can become graph nodes and edges without losing evidence lineage.
- Plan, elevation, and reference framework research matter because Stage 8 should manifest spatial organization from the ground up rather than dropping abstract nodes into space arbitrarily.
- Uncertainty research matters because the scene graph needs to show partial truth, alternative hypotheses, and low-confidence areas.

#### What HugePrompt3 should carry forward

- The first scene graph is interpretive, not final-detail geometry.
- It must show what exists, where it sits spatially, what connects to what, and how certain the system is.
- It should preserve schematic visibility even when precise geometry is missing.

#### Reframing notes

- MainPlan3 deliberately separates Stage 8 from Stage 8A. Scene-graph generation is not the same thing as building the richer browser review model.

### Stage 8A - Detailed Three.js Review Model

#### Core references

- AI Structural Model Review Pipeline.md
- Scene Graph Contract for Browser Review.md
- Pipeline Object Identity and Naming.md
- Uncertainty and Conflict Pipeline Model.md

#### Support references

- Geometry Solver Research for Structural Drawings.md
- Structural Graph Builder Research.md

#### What these sources contribute

- AI Structural Model Review Pipeline.md is the main implementation source for the richer browser layer: R3F/Zustand direction, instancing, staged review sequence, evidence sync to PDF, performance guidance.
- Scene graph contract research provides the semantic data shape the richer browser model should deepen, not replace.
- Identity research matters because selections, overrides, and review history need stable object references.
- Uncertainty research supplies the UI rationale for heatmaps, ghosted geometry, and unresolved-state display.
- Geometry solver research becomes more useful here because it can improve the review model once enough object identity and topology are stable.

#### What HugePrompt3 should carry forward

- This stage is still a review model, not BIM authoring.
- The browser should prioritize evidence linkage, reviewability, and performance over photorealism.
- Detailed geometry should deepen confirmed understanding, not hide uncertainty.

### Stage 9 - Reserved For Future Review-Loop Refinement

#### Current note

- The interpretation-steering semantics previously placed at Stage 9 have been moved upstream into the Stage 5A and Stage 5B first milestone.
- The later human-visible review loop is now centered on Stage 8, Stage 8A, and Stage 10.

#### Reframing notes

- Leave Stage 9 open until the later browser review loop needs its own distinct coordination stage.

### Stage 10 - Human Review Of The Scene Graph

#### Core references

- Human Review Protocol for AI Extraction.md
- AI Structural Model Review Pipeline.md
- Scene Graph Contract for Browser Review.md
- Pipeline Object Identity and Naming.md
- Uncertainty and Conflict Pipeline Model.md
- engineering-drawing-vision.md

#### What these sources contribute

- Human Review Protocol for AI Extraction.md provides the strongest model for approve, reject, edit, reread, and targeted invalidation behavior.
- AI Structural Model Review Pipeline.md defines the actual browser-review responsibilities and staged workflow.
- Scene Graph Contract for Browser Review.md tells us what needs to be inspectable at review time: node identity, evidence links, issue markers, review status.
- Identity research is required so overrides survive reruns and export.
- Uncertainty research reinforces that low-confidence and conflicted objects should be highlighted rather than hidden.
- engineering-drawing-vision.md remains relevant as a guardrail: do not accept critical values without visible evidence.

#### What HugePrompt3 should carry forward

- Final review should be structured, evidence-linked, and action-oriented.
- Override objects should be first-class artifacts with provenance and invalidation rules.
- The reviewed model should be an overlay on top of the AI model, not a destructive rewrite with no history.

### Stage 11 - Downstream Export Later

#### Core references

- Pipeline Object Identity and Naming.md
- Structural Graph Builder Research.md
- Scene Graph Contract for Browser Review.md

#### Support references

- Geometry Solver Research for Structural Drawings.md
- AI Structural Model Review Pipeline.md

#### What these sources contribute

- Identity and naming research is the most important export prerequisite because stable IDs and canonical names are what let later IFC/Revit export stay consistent with review history.
- Structural graph builder research matters because export should flow from the stable neutral model, not directly from ad hoc browser geometry.
- Scene graph contract research is useful mainly as a downstream bridge, not as the export source of truth.
- Geometry solver work becomes more important once the system is producing export-ready geometry rather than just review geometry.

#### What HugePrompt3 should carry forward

- Export is downstream of the reviewed neutral model.
- The system should not treat Revit or BIM placement as the first internal representation.
- Export readiness depends on identity stability, topology coherence, geometry maturity, and review status.

## 4. Cross-Stage Conclusions That Should Shape HugePrompt3

### 4.1 The skills pack is the methodological baseline

- engineering-drawing-vision.md should remain the baseline reading discipline.
- openai-model-calls.md should remain the baseline for structured outputs, prompt families, run traceability, and model configuration.
- vision-document-pipeline.md is mostly useful as a warning against generic document-processing assumptions.

### 4.2 The strongest architectural correction is the Stage 5 and Stage 6 split

- The research corpus often drifts toward blending evidence organization and model creation.
- MainPlan3 is stronger because it inserts coherent observation packaging before neutral-model synthesis.
- HugePrompt3 should preserve that split explicitly.

### 4.3 Deterministic extraction is still important, but no longer owns the architecture

- Deterministic Evidence Bundle for Drawings.md, PDF Vector and OCR Extraction Pipeline.md, and AI for Australian Steel Schedule Extraction.md are still highly valuable.
- Their value is highest when they operate as selective support evidence under orchestrator control.
- HugePrompt3 should not let them silently become the backbone again.

### 4.4 Ground-up spatial reasoning is the right organizing bias

- Structural Plan Interpretation Research.md, Structural Elevation Resolution Research.md, and Structural Drawing Reference Framework Research.md together support the MainPlan3 idea that interpretation should begin from the lowest reliable plan-level manifestation and then rise into vertical and dependent geometry.
- HugePrompt3 should keep that as a persistent reasoning rule.

### 4.5 Identity, uncertainty, and review are not downstream polish

- Pipeline Object Identity and Naming.md
- Uncertainty and Conflict Pipeline Model.md
- Human Review Protocol for AI Extraction.md

These three documents should be treated as system-wide contracts, not late-stage extras.

They govern whether the pipeline can survive reruns, preserve trust, and support human correction without chaos.

### 4.6 The browser is a review surface, not the source of truth

- Scene Graph Contract for Browser Review.md and AI Structural Model Review Pipeline.md are valuable because they clarify how to expose the model for inspection.
- They should not replace the neutral model as the core internal representation.

## 5. Suggested Priority For HugePrompt3 Authoring

1. Lock the artifact and run backbone using AI Drawing Interpretation Pipeline Architecture.md, LLM Pipeline Run Management Design.md, and openai-model-calls.md.
2. Lock the reading methodology using engineering-drawing-vision.md plus the plan, elevation, and reference framework research.
3. Lock Stage 5 and Stage 6 contracts before going deeper into browser detail.
4. Add identity, uncertainty, and human review rules as system-wide constraints, not optional modules.
5. Treat Three.js review details as a later layer that consumes the stable neutral model rather than defining it.
