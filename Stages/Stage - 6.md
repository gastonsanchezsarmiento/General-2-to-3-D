# Stage 6 - Neutral Model Synthesis

## 0. Purpose

Stage 6 turns the coherent observation package into the stable internal model of the project.

Stage 5A makes the evidence coherent.

Stage 5B exposes that interpretation visually for first-milestone review.

Stage 6 makes the model.

This is the first stage where the system should commit project objects, spatial anchors, and topology into a durable internal representation that later stages can verify, review, visualize, and export from.

This stage should not re-run the reading workflow.

It should not treat raw page findings as its primary input.

It should consume the Stage 5A package and synthesize from it.

---

## 1. Core Role

Stage 6 is the neutral-model synthesis layer.

It should:

- consume the Stage 5 coherent observation package
- create stable internal object identities
- create stable internal relationship and topology state
- anchor objects in plan-space and level-space before over-committing geometry
- preserve evidence, uncertainty, conflict, and review status on model objects
- support semantic placement before full metric completeness
- prepare a model that later stages can verify, visualize, and refine

It should not:

- invent missing structure when the package is too weak
- replace Stage 5 packaging logic
- collapse conflicts just to force a cleaner model
- tie the internal model directly to Revit, Three.js, or an export-specific shape
- require perfect geometry before an object may exist in the neutral model

---

## 2. What This Stage Receives

Stage 6 receives the Stage 5A coherent observation package as its primary working input.

Primary inputs should include:

- run ID
- synthesis cycle ID
- Stage 5A package manifest
- Stage 5A readiness summary
- Stage 5A observation index
- Stage 5A candidate object groups
- Stage 5A candidate relationship groups
- Stage 5A conflict registry
- Stage 5A unresolved registry
- Stage 5A identity registry
- Stage 5A evidence linkage index
- orchestrator synthesis instructions
- current project profile or active domain modules

Useful supporting inputs may include:

- Stage 0 manifests for source provenance
- Stage 1 reconnaissance context
- Stage 2 read-plan context when synthesis routing needs to understand original intent
- prior Stage 6 model state during reruns
- human approval or human review actions from the Stage 5A and Stage 5B checkpoint

---

## 3. What This Stage Actually Does

Stage 6 should behave like a controlled retrieval-and-commit synthesis workflow.

### 3.1 Validate the handoff from Stage 5A and Stage 5B

Stage 6 should begin by reading the Stage 5A package manifest and structured readiness summary.

If a Stage 5B board was required for the run, Stage 6 should also confirm that the orchestrator has recorded the resulting human disposition.

If the readiness summary says the package is not eligible for synthesis, Stage 6 should stop and return control to the orchestrator.

Stage 6 should not begin until the orchestrator records explicit human approval of the first milestone.

### 3.2 Select a narrow synthesis slice

Stage 6 should not ingest the whole package as one giant reasoning context.

It should work on narrow synthesis slices selected by the orchestrator.

Example synthesis slices include:

- one object family
- one level
- one grid zone
- one structural subsystem
- one conflict-focused subset
- one profile-specific template area such as portal frames or footing groups

### 3.3 Resolve candidate objects into internal model entities

Stage 6 should take candidate object groups from Stage 5 and decide whether they become:

- committed neutral-model objects
- explicit alternative hypotheses
- unresolved model placeholders
- rejected weak candidates

This is the transition from evidence of an object to identity of an object.

### 3.4 Resolve candidate relationships into internal topology

Stage 6 should take candidate relationship groups and turn them into neutral-model relationship state.

This includes relations such as:

- located at
- belongs to level
- spans between
- supports
- connected to
- aligned with
- references mark
- depends on

Stage 6 should be able to express topology even when not all geometry is final.

### 3.5 Anchor the model from the ground up

The model should be built from the lowest reliable spatial logic upward.

This means Stage 6 should prefer this order of truth:

- reference framework
- plan anchors
- support points and base structure
- spanning members and enclosing logic
- secondary or dependent members
- later geometry refinement

This is a critical continuity rule in the overall plan.

### 3.6 Preserve evidence and epistemic state

Every committed object and relationship should preserve:

- evidence links
- direct versus derived versus inferred state
- unresolved state where applicable
- conflict references where applicable
- review state

The neutral model is not just geometry.

It is evidence-backed interpreted structure.

### 3.7 Emit synthesis results back into shared artifacts

Stage 6 should write structured model artifacts back into the shared project artifact space.

These outputs should be stable enough that Stage 7 can verify them and Stage 8 can visualize them.

---

## 4. Stable Neutral Model Contract

Stage 6 is where the stable neutral-model contract begins.

Unlike Stage 5A, which remains in the flexible interpretation-package layer, Stage 6 should use a stable internal contract.

The contract should stay stable around concepts such as:

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

At minimum, the neutral model should make it possible to answer:

- what this object is
- where it sits in the project spatially
- what it connects to or depends on
- how complete its geometry currently is
- what evidence supports it
- whether it is direct, derived, inferred, unresolved, conflicting, or human-corrected

This contract should remain stable across project types.

---

## 5. Adaptive Modules Versus Stable Core

The neutral model should not be reinvented from scratch for each project.

However, the orchestrator may activate different domain-oriented modules depending on project profile.

Examples:

- warehouse or portal-frame modules
- house or residential modules
- multi-floor building modules
- broader general-structural modules

This adaptation should change:

- which object families are emphasized
- which relationship families are emphasized
- which synthesis sequence is preferred
- which follow-up validations are important

It should not change the stable core shape of the neutral model.

So the correct design is:

- stable neutral-model skeleton
- optional profile-specific modules
- no unconstrained schema invention per run

---

## 6. Core Neutral Model Fields

Every committed neutral-model object should try to preserve a common minimum field set.

Recommended core fields for objects:

- neutral object ID
- object family or type
- display label when available
- project profile module when relevant
- spatial anchor
- level or elevation anchor when known
- geometry description
- geometry maturity
- topology references
- dimensions and dimension confidence
- evidence references
- epistemic status
- conflict references
- review status
- lineage back to Stage 5A candidate IDs

Recommended core fields for relationships:

- neutral relationship ID
- relationship family
- source object IDs
- target object IDs when applicable
- support or confidence status
- evidence references
- epistemic status
- conflict references
- review status
- lineage back to Stage 5A candidate relationship IDs

---

## 7. Geometry Maturity Model

Stage 6 should keep geometry maturity explicit.

Recommended maturity ladder:

### 7.1 Semantic

The system knows what the object is, but not enough yet about where or how it is shaped.

### 7.2 Anchored

The object is placed in the project using stable plan or level anchors.

Examples:

- column at Grid A-1
- footing at Grid B-3
- stair tied to Level 1 opening zone

### 7.3 Schematic

The object has rough extent, direction, or role, but not yet reliable full dimensions.

Examples:

- beam spans between two anchored supports
- portal frame exists between two grid lines
- wall line is known but thickness is weak

### 7.4 Approximate

Most geometry is known, but some values remain inferred, coarse, or insufficiently verified.

### 7.5 Metric

Geometry is supported strongly enough for deterministic downstream use.

### 7.6 Unresolved

The system cannot honestly place or size the object enough to promote it beyond unresolved model state.

This maturity should be explicit on objects and relationships where relevant.

---

## 8. Unresolved Pass-Through Policy

Stage 6 must decide when unresolved information may still enter the neutral model as unresolved state.

This applies especially to missing distances, spans, heights, and other geometric dimensions.

### 8.1 Pass-through allowed

An object or relationship may pass through as unresolved state when:

- identity is plausible enough to keep stable
- spatial anchor is reliable enough to preserve
- unresolved attributes are secondary rather than foundational
- keeping the item in the model helps downstream understanding without creating false certainty

Examples:

- a column is clearly present at a grid location, but exact section size remains unresolved
- a beam span is known, but exact depth is still weak
- a slab zone is anchored, but thickness is uncertain

### 8.2 Pass-through blocked

An object or relationship should block synthesis for that slice when:

- object identity itself is too weak
- spatial placement is too unstable
- topology would become misleading
- contradictions are too strong to preserve as a single committed state
- downstream consequences of a wrong promotion would be structurally harmful to the model

Examples:

- an element may be either a wall or a beam line
- a support relationship is contradicted by core sources
- a candidate cannot be anchored to a reliable plan or level reference

### 8.3 Route on block

When pass-through is blocked, Stage 6 should not invent a resolution.

It should emit a blocked synthesis result and return control to the orchestrator.

---

## 8A. Inferred And Approximate Dimension Policy

Stage 6 should be allowed to carry inferred or approximate dimensions when explicit dimensions are missing or could not be recovered from the documentation.

This is useful when the inferred value helps the model preserve structural logic, spatial coherence, or review usefulness.

However, inferred dimensions must never be silently treated as authoritative metric truth.

### 8A.1 When inference is allowed

Inference or approximation is allowed when:

- the object identity is already stable enough
- the spatial anchor is already stable enough
- the inferred dimension helps keep the model usable
- the inference can be tied to a stated basis
- the orchestrator allows that level of inference for the current synthesis slice

Examples:

- approximate beam span inferred from anchored supports
- approximate wall thickness inferred from repeated conventions in the same pack
- approximate roof height inferred from eaves and ridge logic
- approximate footing spacing inferred from stable grid spacing

### 8A.2 What must be stored with inferred dimensions

Every inferred or approximate dimension should preserve:

- dimension value
- dimension type such as span, offset, height, width, thickness, pitch, or spacing
- epistemic status such as inferred schematic or inferred approximate
- inference basis
- evidence references used for the inference
- confidence or support strength
- review-required flag
- user-resolvable flag

The model should be able to distinguish between:

- directly read dimensions
- derived dimensions from explicit evidence
- inferred approximate dimensions
- unresolved dimensions with no useful estimate

### 8A.3 Who decides

The orchestrator should decide whether a synthesis slice is allowed to use inferred dimensions.

Stage 6 should apply the allowed policy inside the slice, but it should not widen the inference policy on its own.

That means:

- the orchestrator sets whether approximation is allowed
- Stage 6 computes and records the approximation if justified
- the resulting model object stores the value as reviewable inferred state

### 8A.4 When inference should be blocked

Inference should be blocked when:

- the object anchor is weak
- multiple competing inferences are equally plausible and materially different
- the inference would create misleading topology or geometry
- the value is too critical to approximate safely at this stage

In those cases, the dimension should remain unresolved and the slice should either continue with unresolved state or route backward, depending on orchestrator policy.

### 8A.5 Future review and visualizer implications

Inferred and approximate dimensions should be visible later in the visualizer and review workflows.

They should be clearly flagged so a user can:

- see that the value is approximate
- inspect the inference basis
- compare it with supporting evidence
- correct or confirm it in a later feedback loop

Human correction should be able to replace the inferred value while preserving lineage to the original inferred state.

This makes inferred dimensions useful for continuity now without hiding that they remain provisional.

---

## 9. Synthesis Sequence

Stage 6 should prefer a dependency-aware synthesis order rather than one monolithic pass.

Recommended order:

### 9.1 Reference framework first

Resolve and commit:

- grids
- datums
- levels
- reference axes
- major plan anchors

### 9.2 Spatial structure next

Resolve and commit:

- building extents
- bays
- major zones
- storey or level partitions
- major plan groupings

### 9.3 Primary supports next

Resolve and commit:

- columns
- primary load-bearing walls
- footings
- major support nodes

### 9.4 Primary spanning members next

Resolve and commit:

- beams
- rafters
- portal frames
- slabs
- primary roof members

### 9.5 Dependent and secondary systems next

Resolve and commit:

- secondary framing
- openings
- stairs
- canopies
- local supporting members
- other dependent objects

### 9.6 Geometry refinement after structural logic exists

Only after the symbolic and topological structure is stable should later refinement strengthen geometry toward deterministic quality.

---

## 10. Spatial Anchoring And Vertical Logic

Stage 6 should synthesize from a reference framework of grids, levels, and datums.

Horizontal anchoring should prioritize:

- plan grids
- grid intersections
- offsets from grids
- major plan zones

Vertical anchoring should prioritize:

- RL markers
- FFL
- TOS
- eaves level
- ridge or apex level
- section or elevation-based node heights

For frame-based structures such as portal-frame warehouses, Stage 6 should understand vertical frame nodes such as:

- base
- knee or eaves
- apex or ridge

These should act as symbolic structural nodes before exact coordinates are fully solved.

---

## 11. Symbolic Topology Before Full Geometry

Stage 6 should represent structural logic symbolically before requiring final coordinates.

This means the neutral model should be able to express facts such as:

- a column is at Grid A-1 and rises from FFL to Eaves
- a beam spans between two support objects
- a portal frame exists on a grid line and has a knee and apex structure
- a footing supports a base node
- an opening creates a negative zone in a wall or roof surface

This symbolic representation is not a weakness.

It is what allows the system to remain useful before exact geometry is complete.

---

## 12. Relationship To The Orchestrator

Stage 6 is orchestrator-controlled.

The orchestrator should decide:

- whether Stage 6 starts at all
- whether the Stage 5 package is accepted for synthesis
- whether first-milestone human approval has been recorded
- which synthesis slice should run next
- which project profile modules are active
- what inference level is allowed for that slice
- whether unresolved items may pass through or must block
- when a synthesis slice should stop
- when failures should be routed backward to Stage 2, Stage 3, or Stage 4

Stage 6 should not decide the whole workflow.

It should synthesize the slice assigned by the orchestrator and write results back into shared artifacts.

---

## 13. How It Communicates With The Orchestrator

The communication pattern should be:

1. orchestrator reads the Stage 5 package and approval state
2. orchestrator selects the next synthesis slice
3. Stage 6 reads only the needed package artifacts for that slice
4. Stage 6 writes neutral-model outputs, blocked states, or unresolved pass-through states
5. Stage 6 reports whether the slice was committed, partial, blocked, or requires back-routing
6. orchestrator decides the next synthesis step or a backward loop

This keeps context narrow and auditable.

---

## 14. Relationship To Stage 5

Stage 5 is the immediate source stage for Stage 6.

The boundary is strict:

- Stage 5 packages observations
- Stage 6 synthesizes the neutral model

Stage 6 should not use raw Stage 3 or Stage 4 findings as its primary working input.

If Stage 6 repeatedly needs to clean raw upstream noise, then the Stage 5 package is not doing its job.

Stage 6 should begin only when:

- the Stage 5 readiness summary says the package is eligible for synthesis if approved
- the orchestrator accepts the package for synthesis
- explicit first-milestone human approval has been recorded

---

## 15. Relationship To Stage 7

Stage 6 is the source stage for Stage 7 verification.

That means Stage 6 outputs should preserve enough detail that Stage 7 can challenge them.

This includes:

- model object identity
- topology commitments
- geometry maturity
- evidence links
- unresolved and conflict state
- review status
- lineage back to Stage 5A candidates

Stage 7 should be able to ask not only whether an object exists, but why the system believed it exists and how mature that belief currently is.

---

## 16. Relationship To Stage 8 And Later Stages

Stage 6 should remain independent from browser scene graph and export formats.

Later stages may consume it for:

- interpretive scene graph generation
- richer review model generation
- human review workflows
- export-oriented downstream work

But none of those later stages should define the neutral model itself.

---

## 17. What This Stage Outputs

Stage 6 should write structured neutral-model artifacts.

Recommended output families:

- neutral model manifest
- neutral object records
- neutral relationship records
- spatial anchor registry
- geometry maturity registry
- topology graph artifacts
- unresolved model-state artifacts
- conflict-linked model-state artifacts
- synthesis logs and slice results

### 17.1 Neutral model manifest

The neutral model manifest should be the root contract for Stage 6 outputs.

It should contain:

- model ID
- run ID
- synthesis cycle ID
- accepted Stage 5A package ID
- active project profile modules
- model version
- overall synthesis status
- links to object, relationship, anchor, topology, unresolved, and conflict artifacts
- verification-readiness summary for Stage 7

### 17.2 Synthesis slice result contract

Each synthesis slice should emit a structured slice result.

That result should record:

- slice ID
- slice type
- scope definition
- input package artifacts used
- objects committed
- relationships committed
- unresolved items passed through
- blocked items
- backward-route recommendation when needed
- exit status

Recommended exit status values:

- committed
- partial
- blocked
- reroute-stage2
- reroute-stage3
- reroute-stage4

### 17.3 Spatial anchor registry

The spatial anchor registry should preserve the model's reference backbone.

It should include anchors such as:

- grid intersections
- grid offsets
- levels
- RL anchors
- FFL anchors
- TOS anchors
- eaves anchors
- apex or ridge anchors

This registry should remain usable even before all coordinates are fully metric.

### 17.4 Topology graph artifacts

The topology layer should be queryable independently from object attribute storage.

At minimum it should support:

- support relations
- span relations
- containment or belongs-to relations
- dependency relations
- connection relations
- alignment relations

This allows Stage 7 and later stages to inspect structural logic without reparsing object records.

Recommended Stage 6 output fields should include:

- run ID
- synthesis cycle ID
- synthesis slice ID
- neutral object or relationship IDs
- lineage to Stage 5A candidate IDs
- object family or relationship family
- spatial anchor and vertical anchor
- geometry description and maturity
- evidence references
- epistemic state
- conflict references
- review status
- blocked or partial synthesis markers when applicable

### 17.5 Suggested output structure

```text
outputs/
  runs/<run_id>/
    stage6/
      model/
        manifest.json
        verification-readiness.json
        objects/
          obj-*.json
        relationships/
          rel-*.json
        anchors/
          anchor-registry.json
        topology/
          topology-graph.json
        unresolved/
          unresolved-*.json
        conflicts/
          conflict-*.json
      slices/
        slice-*.json
      logs/
```

---

## 18. Model Acceptance And Exit Criteria

Stage 6 should not be considered successful just because it emitted model files.

It is successful when:

- the model contract remains stable and interpretable
- committed objects have stable identities
- committed relationships form coherent topology
- geometry maturity is explicit rather than implied
- unresolved and conflict state remain honest
- evidence traceability is preserved
- the resulting model is ready for Stage 7 verification

Stage 6 may be only partially complete for a given run.

That is acceptable if the state is explicit and auditable.

---

## 19. Design Rules

Stage 6 should follow these rules.

### Rule 1

Consume the Stage 5 package, not raw reading noise, as the primary working input.

### Rule 2

Use a stable neutral-model contract with optional profile modules.

### Rule 3

Build from reference framework and plan anchors upward.

### Rule 4

Preserve symbolic topology before forcing exact geometry.

### Rule 5

Keep geometry maturity explicit.

### Rule 6

Allow unresolved pass-through only when identity and anchoring are sufficiently stable.

### Rule 7

Block and route backward instead of inventing missing structure.

### Rule 8

Keep the neutral model independent from browser and export-specific targets.

---

## 20. Build Guidance (No UI)

This section describes how Stage 6 should be built as a backend synthesis step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- backend synthesis worker or synthesis agent under orchestrator control
- artifact-backed persistence on filesystem for POC

### Recommended packages

- `pydantic` for typed neutral-model schemas
- `orjson` for fast JSON serialization
- `tenacity` for retries and backoff
- `networkx` for topology graph construction and traversal
- `numpy` optional for coordinate refinement and symbolic-to-metric transition helpers
- standard library modules such as `pathlib`, `logging`, `uuid`, `datetime`, and `collections`

### Suggested file structure

```text
pipeline/
  common/
    artifact_store.py
    ids.py
    schema_utils.py
    provenance.py
  stage6/
    synthesizer.py
    slice_selector.py
    object_resolver.py
    relationship_resolver.py
    topology_builder.py
    anchor_registry.py
    maturity_model.py
    pass_through_policy.py
    output_schema.py
    writer.py
outputs/
  runs/<run_id>/
    stage6/
      model/
        manifest.json
        objects/
        relationships/
        anchors/
        topology/
        unresolved/
        conflicts/
      logs/
      slices/
```

### Implementation notes

- keep synthesis slice-based rather than monolithic
- keep identity resolution deterministic where possible
- preserve lineage to Stage 5A candidate IDs on every committed object
- store symbolic anchors even when metric coordinates are not yet solved
- keep blocked synthesis results explicit so orchestrator can route reruns intelligently
- publish Stage 6 manifests, slice results, backbone registries, neutral objects, and neutral relationships against the canonical registry under `Schemas/stage6/`

---

## 21. Summary

Stage 6 is the stable neutral-model synthesis stage.

It consumes the Stage 5 package, builds durable internal objects and relationships, preserves evidence and uncertainty, and anchors the project from the ground up before over-committing geometry.

It is orchestrator-controlled, profile-aware, and deliberately independent from browser and export-specific representations.

---

## 22. HOW TO

Use this stage when the Stage 5 package has been accepted for synthesis.

Practical execution order:

1. read the Stage 5 manifest and readiness summary
2. verify the orchestrator has authorized synthesis and that explicit first-milestone human approval is recorded
3. select one narrow synthesis slice
4. load only the object groups, relationship groups, conflicts, and unresolved artifacts needed for that slice
5. commit reference framework and anchor state first
6. promote stable candidate objects into neutral-model objects
7. promote stable candidate relationships into topology
8. mark geometry maturity explicitly on every committed object
9. allow unresolved pass-through only when identity and anchoring are stable enough
10. if the slice is too weak, emit a blocked synthesis result and return control to the orchestrator
11. write the slice outputs back into the neutral-model artifact space
12. repeat slice by slice until the model is coherent enough for Stage 7 verification

What to avoid:

- do not read the whole package into one giant prompt
- do not invent missing geometry to keep the model moving
- do not hide conflicts or unresolved states inside a seemingly clean model
- do not tie the neutral model directly to later scene graph or export formats

What good looks like:

- stable object identity
- stable topology
- evidence-linked commitments
- explicit geometry maturity
- honest unresolved state
- clean handoff to verification