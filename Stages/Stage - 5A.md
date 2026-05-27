# Stage 5A - Coherent Observation Packaging

## 0. Purpose

Stage 5A turns fragmented findings into a coherent observation package.

This is the first milestone where the system should be able to present a pack-level understanding that a human can judge.

It is the text-and-package half of that milestone.

Its job is not to build the final neutral model.

Its job is to:

- organize what the system currently understands
- show what is strongly supported and weakly supported
- preserve uncertainty and conflict honestly
- package observations into a form that Stage 6 can consume directly
- provide the structured base that Stage 5B will turn into a low-resolution visual interpretation board
- provide the first explicit human feedback checkpoint

Stage 5A is where local reading becomes project-level understanding.

Within the broader schema strategy, Stage 5A belongs to the flexible interpretation-package layer.

Its package may adapt its active object families, relation modules, and pack-specific sections based on project profile.

But it should still stay inside a stable package template rather than inventing a new downstream contract from scratch.

The stable neutral-model contract begins in Stage 6.

---

## 1. Core Role

Stage 5A is the coherent observation packaging layer.

It should:

- ingest Stage 3 findings and Stage 4 support artifacts
- normalize them into stable observation forms
- group related findings into candidate object and relationship groups
- preserve provenance, confidence, conflict, and unresolved state
- generate a human-readable overall understanding artifact
- generate a machine-readable observation package for Stage 6
- give Stage 5B a stable interpretation package it can visualize without inventing its own understanding layer

It should not:

- replace Stage 6 model synthesis
- silently resolve contradictions just to make the package look cleaner
- flatten uncertainty into fake certainty
- force later stages to clean up raw reading noise

---

## 2. What This Stage Receives

Stage 5A receives structured outputs from the earlier reading and support stages.

Primary inputs should include:

- run ID
- packaging cycle ID
- Stage 3 findings artifacts
- Stage 3 object candidate artifacts
- Stage 3 relationship candidate artifacts
- Stage 3 unresolved notes
- Stage 3 conflict hints
- Stage 4 support artifacts when invoked
- orchestrator packaging instructions
- current packaging profile

Useful supporting inputs may include:

- Stage 0 source document and page manifests
- Stage 1 reconnaissance artifacts
- Stage 2 typed read plan
- orchestrator routing logs
- prior Stage 5A package from an earlier loop when rerunning
- human feedback notes from a previous Stage 5A or Stage 5B review cycle

---

## 3. What This Stage Actually Does

Stage 5A should behave like a controlled packaging workflow.

### 3.1 Ingest and validate upstream artifacts

Stage 5A should ingest the relevant outputs from Stage 3 and Stage 4.

It should validate that the artifacts are structurally usable before packaging proceeds.

If core artifacts are malformed or incomplete, the stage should report that explicitly instead of masking the problem.

### 3.2 Normalize observations into stable forms

Stage 5A should normalize incoming findings into stable observation templates.

This means standardizing fields such as:

- observation type
- object family
- relationship family
- evidence references
- confidence or support strength
- direct, derived, inferred, unresolved classification

The goal is to reduce raw reading noise without prematurely forcing resolution.

### 3.3 Group related findings

Stage 5A should group related observations into candidate object groups and candidate relationship groups.

These groups are not yet the final neutral model.

They are intermediate structured packages that say:

- these findings appear to refer to the same candidate object
- these findings appear to refer to the same candidate relationship
- this grouping is strong, weak, or contested

### 3.4 Preserve conflict and unresolved state

Stage 5A must keep epistemic integrity intact.

It should explicitly preserve:

- contradictions
- ambiguity
- weak evidence
- missing evidence
- alternative hypotheses when needed

It should not collapse them just to make the package easier to consume.

### 3.5 Produce package-level understanding

Stage 5A should generate a text-based overall understanding artifact for human checking.

This is a required milestone output.

It should answer questions such as:

- what kind of drawing pack this appears to be
- what the apparent project structure is
- what the major object families are
- what is strongly supported versus weakly supported
- what the main unresolved areas are
- what the current maturity of understanding is

### 3.6 Produce a machine-readable observation package

Stage 5A should also generate the structured package that Stage 6 will consume.

This package should be navigable through manifests and indexes rather than a single giant blob.

### 3.7 Publish a milestone result for review

At the end of each Stage 5A cycle, the system should be able to present a milestone package for orchestrator and human review.

That milestone may then be paired with the Stage 5B visual board before the human decides whether the first milestone is approved for exit from the loop.

The orchestrator should record that human decision and route the result.

This is the first point where the run should be judged at a project-understanding level.

---

## 4. Should This Stage Produce Human-Readable And Machine-Readable Outputs Every Time

Yes.

Both outputs should be produced in every normal Stage 5A loop.

However, they should not be produced as two unrelated products.

Recommended order inside Stage 5A:

1. build and validate the machine-readable observation package
2. derive the human-readable overall understanding from that packaged state
3. publish both artifacts together as the Stage 5A milestone result

This is the safest design because:

- the structured package remains the canonical source of truth
- the human-readable artifact stays aligned with what Stage 6 will actually consume
- human feedback can map back to concrete packaged objects, conflicts, and unresolved sets

Stage 5A may emit a provisional brief overview earlier for monitoring if needed.

But the official Stage 5A checkpoint should contain both outputs.

---

## 5. What This Stage Outputs

Stage 5A should output two coordinated artifact families.

### 5.1 Human-readable understanding artifacts

Stage 5A should always emit a text-based overall understanding report.

This report should have two sections.

#### Section A - Overall description

This should provide the broad, high-level description of the pack.

It should describe:

- what type of drawing set this seems to be
- the overall project structure
- the dominant sheet roles
- the major object families present
- the apparent maturity of understanding

#### Section B - Precise understanding

This should provide the detailed current understanding.

It should describe:

- what the system believes sheet by sheet or sheet group by sheet group
- object-family-level understanding
- strong evidence areas
- weak evidence areas
- major conflicts
- unresolved regions or questions
- what Stage 6 is ready to synthesize and what it is not ready to synthesize

### 5.2 Machine-readable observation package

Stage 5A should emit a coherent observation package for Stage 6.

Recommended package components:

- package manifest
- packaging profile metadata
- package readiness summary
- observation index
- candidate object group artifacts
- candidate relationship group artifacts
- evidence linkage index
- conflict registry
- unresolved registry
- identity registry
- optional package-level markdown summaries for audit

The package should remain deterministic enough for software navigation even if its contents are produced through adaptive agentic behavior.

---

## 6. Recommended Package Structure For Stage 6 Consumption

Stage 5A should not hand Stage 6 a single monolithic JSON document.

It should hand Stage 6 a package made of typed artifacts plus indexes.

### 6.1 Package manifest

The package manifest should contain:

- package ID
- run ID
- packaging cycle ID
- packaging version
- packaging profile
- source stage references
- readiness flags
- package quality summary
- links to all sub-artifacts and indexes

Stage 6 should read this file first.

It is the package root and the entry point for all downstream consumption.

### 6.2 Package readiness summary

The readiness summary should be a structured gate, not just prose.

It should state:

- whether the package is ready for first-milestone human review
- whether the package would be eligible for Stage 6 if human approval is recorded
- current maturity by understanding category
- major blockers
- major warnings
- package coverage summary
- what can be synthesized now versus later

### 6.3 Overall understanding report

This is the human-readable review artifact.

It is not the primary Stage 6 input, but it is part of the package and should be stored alongside it.

### 6.4 Observation index

The observation index should let later stages retrieve observations by:

- page ID
- sheet role
- object family
- candidate object ID
- candidate relationship ID
- mark
- grid
- level
- confidence tier
- conflict state
- unresolved state

Stage 6 should use this index to retrieve only the candidate groups relevant to the current synthesis task.

### 6.5 Candidate object groups

Each object group should try to include:

- candidate object ID
- object family
- display label when available
- grouped observations
- grouped evidence references
- direct observations
- derived observations
- inferred observations
- unresolved flags
- alternative hypotheses when needed

These are the main Stage 6 synthesis inputs for object creation.

They are not yet final neutral-model objects.

### 6.6 Candidate relationship groups

Each relationship group should try to include:

- candidate relationship ID
- relationship family
- source candidate object IDs
- supporting observations
- supporting evidence references
- confidence or support status
- unresolved or conflict state

These are the main Stage 6 synthesis inputs for topology construction.

### 6.7 Conflict registry

Each conflict record should try to include:

- conflict ID
- participating observations or groups
- conflict type
- severity or tension score when available
- downstream impact
- resolution status
- review requirement

Stage 6 should not silently ignore these records.

It should preserve them or route them back through orchestrator policy.

### 6.8 Unresolved registry

Each unresolved record should try to include:

- unresolved ID
- unresolved type
- affected scope
- missing evidence reason
- recommended next action
- whether Stage 6 may proceed anyway

### 6.9 Evidence linkage index

The evidence linkage index should support reverse tracing from packaged observations back to source evidence.

At minimum it should preserve links to:

- page ID
- region ID
- crop ID when used
- Stage 4 support artifact ID when used
- source text, vector, or schedule artifact IDs when available

Stage 6 should use this when it needs provenance trace-back, not as its primary working representation.

### 6.10 Identity registry

The identity registry should stabilize intermediate candidate identities before final synthesis.

It should preserve:

- candidate IDs
- display names or labels
- lineage from evidence artifacts
- merge or split lineage when regrouping occurs
- durable references for later review and synthesis

### 6.11 Consumption sequence for Stage 6

Stage 6 should consume the package in a controlled order.

Recommended sequence:

1. read the package manifest
2. inspect the package readiness summary
3. stop and return control to the orchestrator if Stage 6 is not allowed to proceed
4. use the observation index to select the next candidate slice to synthesize
5. read candidate object groups and candidate relationship groups for that slice
6. consult conflict and unresolved registries before promoting candidates into the neutral model
7. use the evidence linkage index only when provenance trace-back is required

This keeps Stage 6 from drifting back into raw artifact cleanup.

---

## 6A. Role Of The Orchestrator At The Stage 5A To Stage 6 Boundary

The orchestrator is the coordinator, recorder, and router at this boundary.

Human approval is the authority that exits the first milestone loop.

Its responsibilities should include:

- deciding when a Stage 5A package is ready for review
- reading the package manifest and readiness summary
- deciding whether Stage 6 may begin
- deciding whether the workflow must loop back to Stage 2, Stage 3, Stage 4, or Stage 5B first
- deciding which synthesis slice Stage 6 should attempt next
- deciding whether unresolved or conflicted items may pass through into Stage 6 as explicit unresolved model state

So Stage 5A produces the package.

Stage 5B may add visual review artifacts around that package.

Stage 6 consumes the package.

The orchestrator decides whether that handoff is allowed and how synthesis work is sequenced.

---

## 7. Human Feedback Loop

The first explicit human feedback gate should enter across Stage 5A and Stage 5B.

The expected loop is:

1. Stage 2 defines or revises the read plan
2. Stage 3 performs targeted reading
3. Stage 4 runs optional support extraction when justified
4. Stage 5A packages the current understanding
5. Stage 5B renders the low-resolution interpretation board when requested
6. the human reviews the Stage 5A and Stage 5B milestone outputs
7. the orchestrator records the resulting human approval or requested changes
8. requested changes trigger re-planning, re-reading, support reruns, or packaging reruns as needed
9. the workflow loops back through Stage 2 to Stage 5A and Stage 5B until the human approves the checkpoint for Stage 6

So Stage 5A is not a one-time packaging pass.

It is the checkpoint where the system learns whether its current understanding is acceptable.

---

## 8. Relationship To The Orchestrator

Stage 5A is orchestrator-guided.

The orchestrator should decide:

- when a Stage 5A packaging cycle is triggered
- which upstream artifacts are in scope for the cycle
- which packaging profile is active
- whether the Stage 5A milestone output is ready to present for human checkpoint review
- whether a paired Stage 5B visual board is required before advancing
- whether the workflow should loop back to Stage 2, 3, or 4
- record the human milestone decision before advancing to Stage 6

Stage 5A may be implemented by a dedicated packaging worker or packaging agent under the orchestrator.

But the orchestrator should not replace the human as the authority for exiting the first loop.

It should own the routing logic, scope control, and recording of the human decision.

---

## 9. Relationship To Stage 2

Stage 5A is the first strong feedback checkpoint for Stage 2.

If the package or its paired Stage 5B board reveals that:

- key sheet roles were misunderstood
- important object families are still weakly covered
- major unresolved questions remain
- important conflicts need targeted evidence

then the orchestrator should be able to loop back to Stage 2 and revise the read plan.

So Stage 2 is not finished forever after its first pass.

It may need to adapt based on what Stage 5A and Stage 5B reveal.

---

## 10. Relationship To Stage 3 And Stage 4

Stage 5A packages what Stages 3 and 4 discovered.

It depends on them for evidence input, but it also evaluates whether their outputs are sufficient.

If Stage 5A or Stage 5B finds weak coverage, weak grouping, or unresolved dependency gaps, it may trigger orchestrator follow-up into:

- Stage 3 rereads
- Stage 4 support extraction
- both

Stage 5A should not replace those stages.

It should make their current evidence coherent and expose where more evidence is needed.

---

## 11. Relationship To Stage 6

Stage 6 should consume the Stage 5A observation package rather than raw findings as its primary working input.

This is one of the most important architectural boundaries in the workflow.

Stage 5A makes the evidence coherent.

Stage 6 makes the model.

If Stage 6 has to clean up raw Stage 3 noise directly, then Stage 5A has failed its role.

---

## 12. Milestone Criteria And Exit Criteria

Stage 5A should be judged primarily by criteria and structure.

### 12.1 Coherence criteria

The package should provide a believable project-level understanding.

Minimum expectations:

- an overall understanding report exists
- the broad pack type is identified
- the apparent project structure is described
- major object families are recognized
- strong and weak understanding areas are distinguished

### 12.2 Structural criteria

The package should be navigable for software.

Minimum expectations:

- package manifest exists
- observation indexes exist
- candidate object and relationship groups exist
- evidence links remain intact
- conflict and unresolved registries exist

### 12.3 Epistemic criteria

The package should preserve uncertainty honestly.

Minimum expectations:

- direct, derived, inferred, and unresolved states remain distinct
- contradictions are not silently flattened
- weak support remains visible
- unresolved areas are explicit

### 12.4 Readiness criteria

The package should state whether it is ready for first-milestone human review and whether it would be eligible for Stage 6 if approved.

Minimum expectations:

- readiness flags exist
- major blockers are explicit
- candidate identities are stable enough for synthesis to begin
- package quality is summarized clearly

Stage 5A should not be considered complete just because files were emitted.

It is complete only when the package is coherent, structured, epistemically honest, and sufficiently clear for the next decision.

---

## 13. Deterministic Slider Entry Point

Stage 5A is the correct place to introduce the future deterministic slider.

Not because Stage 5A itself is purely deterministic.

But because Stage 5A is where the quality of different upstream evidence mixes becomes measurable.

For now, this should be represented as a packaging profile or evidence-mix profile.

Examples:

- vision-first only
- vision plus OCR support
- vision plus OCR plus vector hints
- schedule-heavy assist
- strict deterministic enrichment
- minimal deterministic enrichment

The active profile should be recorded in the package manifest.

This makes Stage 5A the comparison point for future tuning.

---

## 14. Future UI And Review Hooks

Some important control surfaces should be flagged now for later UI or review tooling.

These include:

- a Stage 5A and Stage 5B first-milestone review interface
- packaging profile comparison across runs
- expandable human-readable understanding levels
- comment attachment to summary sections, object families, sheet groups, conflicts, and unresolved sets
- future invalidation and rerun controls
- future promotion controls for what may or may not pass into Stage 6

The human-readable understanding artifact should be designed so future UI can expose different complexity levels instead of a single flat wall of text.

---

## 15. Design Rules

Stage 5A should follow these rules.

### Rule 1

Always emit both the human-readable report and the machine-readable package in the normal loop.

### Rule 2

Build the structured package first and derive the human-readable report from it.

### Rule 3

Treat Stage 5A as the text-and-package half of the first explicit human-review milestone.

### Rule 4

Never hide conflicts or unresolved states to make the package look cleaner.

### Rule 5

Do not let Stage 6 consume raw upstream noise as its primary input.

### Rule 6

Record the active packaging profile so future deterministic tuning remains comparable.

---

## 16. Build Guidance (No UI)

This section describes how Stage 5A should be built as a backend packaging step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- backend packaging worker or packaging agent under orchestrator control
- artifact-backed persistence on filesystem for POC

### Recommended packages

- `pydantic` for typed package schemas
- `orjson` for fast JSON serialization
- `tenacity` for retries and backoff
- `networkx` optional for candidate grouping and relationship graph handling
- `jinja2` optional for rendering structured human-readable reports from packaged state
- standard library modules such as `pathlib`, `logging`, `uuid`, `datetime`, and `collections`

### Suggested file structure

```text
pipeline/
  common/
    artifact_store.py
    ids.py
    schema_utils.py
  stage5/
    packager.py
    normalizer.py
    grouper.py
    conflict_registry.py
    unresolved_registry.py
    identity_registry.py
    readiness_evaluator.py
    report_builder.py
    output_schema.py
    writer.py
outputs/
  runs/<run_id>/
    stage5/
      package/
        manifest.json
        readiness-summary.json
        overall-understanding.md
        observation-index.json
        object-groups/
        relationship-groups/
        conflicts/
        unresolved/
        identity/
```

### Implementation notes

- keep packaging rerunnable without requiring full-run reset
- store machine-readable package artifacts separately from human-readable report artifacts
- derive the report from package state so the two do not drift apart
- let human comments reference stable package IDs
- keep package-level readiness explicit so Stage 6 never has to guess if it may proceed
- keep candidate objects, candidate relationships, conflicts, unresolved records, and review actions aligned with the canonical registry under `Schemas/core/` and `Schemas/review/`

---

## 17. Summary

Stage 5A is the coherent observation packaging milestone.

It is the first explicit human feedback checkpoint.

It should always emit both a human-readable overall understanding artifact and a machine-readable observation package.

It should package the current understanding honestly, preserve uncertainty and conflict, and make clear whether the workflow should loop back to Stage 2 through Stage 4 or proceed to Stage 6.

---

## 18. HOW TO

Use this stage when Stage 3 and Stage 4 have produced enough structured reading artifacts for one packaging cycle.

Practical execution order:

1. read the relevant Stage 3 findings, Stage 4 support artifacts, and any prior human feedback for the current slice
2. validate upstream artifacts before packaging begins
3. normalize the findings into stable observation templates
4. group the observations into candidate objects and candidate relationships
5. preserve conflicts, unresolved items, lineage, and evidence state explicitly
6. write the machine-readable package, indexes, registries, and readiness summary
7. derive the human-readable overall understanding artifact from the package state
8. return the package to the orchestrator and to Stage 5B for the first-milestone checkpoint
9. rerun packaging whenever upstream rereads or human feedback materially change the evidence base

What to avoid:

- do not package raw upstream noise as if it were already coherent
- do not hide conflict or uncertainty to make the milestone look cleaner
- do not emit a giant opaque blob that later stages have to re-interpret manually
- do not let Stage 5A drift into Stage 6 synthesis

What good looks like:

- a coherent and navigable package
- explicit readiness for first-milestone review
- stable candidate IDs and evidence lineage
- a text summary that matches the machine-readable package instead of competing with it