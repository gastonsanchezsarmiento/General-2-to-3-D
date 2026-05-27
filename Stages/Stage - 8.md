# Stage 8 - Scene Graph Generation

## 0. Purpose

Stage 8 turns the Stage 6 neutral model and Stage 7 verification state into a browser-facing scene graph.

Its job is not to build the neutral model.

Its job is not to perform human review.

Its job is to publish a structured spatial graph that later browser layers can inspect.

This is the first stage where the interpreted project becomes a formal scene artifact with nodes, edges, geometry references, issue markers, uncertainty state, and evidence hooks.

Stage 8 is still interpretive.

It must be able to represent partial truth honestly.

---

## 1. Core Role

Stage 8 is the scene-graph generation layer.

It should:

- consume Stage 6 neutral-model artifacts as the primary structural source
- consume Stage 7 verification artifacts as the primary trust and issue source
- convert neutral-model objects, relationships, anchors, and unresolved states into scene-graph nodes and edges
- preserve topology, uncertainty, issue linkage, and evidence lineage in browser-facing form
- assign geometry representation modes without overcommitting to later UI detail
- publish a scene graph that Stage 8A and later review workflows can deepen

It should not:

- re-synthesize the model
- silently repair Stage 6 defects
- hide verification failures behind visually clean output
- collapse unresolved or conflicted state into false certainty
- become the final detailed browser review model
- become a BIM export contract

---

## 2. Important Rule

Stage 8 is a downstream representation stage.

That means:

- Stage 6 decides what exists in the neutral model
- Stage 7 decides what is verified, weak, conflicted, blocked, or review-worthy
- Stage 8 turns that state into a browser-facing scene graph

If Stage 8 repeatedly has to invent missing structure or reinterpret raw evidence directly, the upstream contracts are failing.

---

## 3. What This Stage Receives

Stage 8 receives structured model state from Stage 6 and structured verification state from Stage 7.

### 3.1 Primary inputs from Stage 6

Primary Stage 6 inputs should include:

- run ID
- scene generation cycle ID
- Stage 6 neutral model manifest
- Stage 6 verification-readiness summary
- Stage 6 neutral object records
- Stage 6 neutral relationship records
- Stage 6 spatial anchor registry
- Stage 6 geometry maturity registry
- Stage 6 topology graph artifacts
- Stage 6 unresolved model-state artifacts
- Stage 6 conflict-linked model-state artifacts
- Stage 6 synthesis slice results

### 3.2 Primary inputs from Stage 7

Primary Stage 7 inputs should include:

- Stage 7 verification manifest
- Stage 7 verification slice results for the included Stage 6 slices
- Stage 7 verification findings
- Stage 7 issue registry
- Stage 7 confidence-adjustment artifacts
- Stage 7 contradiction or conflict records
- Stage 7 invalidation recommendations
- Stage 7 rerun recommendations
- Stage 7 review-queue items

### 3.3 Supporting inputs

Supporting inputs may include:

- orchestrator scene-generation instructions
- evidence lineage references that point back to Stage 5A, Stage 3, and Stage 4 artifacts
- prior Stage 8 scene graph artifacts during reruns
- project profile modules when representation rules depend on domain conventions

### 3.4 Inputs Stage 8 should not depend on directly

Stage 8 should not depend on raw Stage 3 or Stage 4 findings as its primary working input.

It may follow evidence references for linkage metadata.

It should not go back to raw extraction as the main source of truth.

---

## 4. Scene Eligibility And Gating Policy

Stage 8 should not blindly emit every Stage 6 object as a normal scene object.

It should apply a strict eligibility policy using both Stage 6 and Stage 7 outputs.

### 4.1 Default inclusion

An object, relationship, or anchor should normally be included when:

- Stage 6 committed it into the neutral model
- it has stable enough identity for browser reference
- it has stable enough spatial anchoring for scene placement
- Stage 7 has not recommended direct invalidation of that item or slice

### 4.2 Provisional inclusion

An item may still be included as provisional scene state when:

- Stage 6 committed it with unresolved or inferred state
- Stage 7 marked it as verified-with-warnings, human-review-recommended, or partial-failure
- showing it is useful for later review as long as the issue state remains visible

These items should not be hidden.

They should be marked clearly as provisional, conflicted, inferred, or unresolved.

### 4.3 Blocked or invalidated items

An item should not be emitted as a normal scene object when:

- Stage 7 recommends direct invalidation
- the slice exit status is blocked or rerouted and no provisional display was allowed by the orchestrator
- identity or anchoring is too weak for honest placement

When useful, Stage 8 may still emit a scene-level issue marker or missing-coverage marker for that blocked area instead of pretending the object exists.

### 4.4 Orchestrator override

The orchestrator should be able to decide whether the scene graph contains:

- only verified slices
- verified plus provisional slices
- blocked slices represented only as issue markers

That decision should be recorded in the Stage 8 manifest.

---

## 5. What This Stage Actually Does

Stage 8 should behave like a controlled graph-publication workflow.

### 5.1 Select the scene slice or scene scope

Stage 8 should not always emit the whole project as one giant payload first.

The orchestrator may assign:

- a whole approved model scope
- one level
- one grid zone
- one structural subsystem
- one review bundle
- one delta slice after a rerun

### 5.2 Load Stage 6 structural state

For the selected scope, Stage 8 should load:

- object records
- relationship records
- anchor registry entries
- topology graph data
- unresolved and conflict-linked model state
- geometry maturity data

### 5.3 Overlay Stage 7 verification state

Stage 8 should then overlay the machine-side challenge results onto that structural state.

This means attaching:

- verification status
- issue references
- confidence adjustments
- contradiction flags
- review-queue flags
- invalidation or rerun markers

### 5.4 Convert model state into scene nodes and edges

Stage 8 should convert the neutral-model state into browser-facing scene entities.

At minimum, it should emit:

- scene nodes for objects, anchors, zones, surfaces, openings, or issue markers when needed
- scene edges for support, span, containment, dependency, alignment, or connection relations

### 5.5 Assign geometry representation modes

Stage 8 should assign a geometry representation mode to each scene node that needs spatial depiction.

This is not the final UI styling decision.

It is the representation contract that says what kind of spatial artifact the node can provide.

### 5.6 Publish layer and filter structures

Stage 8 should emit enough structure for later browser layers to filter the graph by:

- object family
- geometry maturity
- verification state
- issue severity
- subsystem
- level or zone
- unresolved or inferred status

### 5.7 Publish evidence and issue linkage

Every scene node and edge that matters for review should preserve linkage to:

- source neutral-model IDs
- verification findings and issue IDs
- evidence references
- lineage references where needed

### 5.8 Emit slice results and manifest updates

Stage 8 should publish a slice result that tells the orchestrator exactly what scene state was generated, skipped, or blocked.

---

## 6. What Stage 8 Must Be Able To Represent

The browser-facing graph must be able to represent more than just solved meshes.

At minimum, Stage 8 must be able to represent:

- structural objects such as columns, beams, rafters, portal frames, walls, slabs, footings, bracing, openings, and placed elements
- reference framework objects such as grids, grid intersections, levels, RL markers, FFL, TOS, eaves, and ridge anchors
- zones and extents such as bays, roof zones, floor zones, canopy zones, office blocks, and bounding extents
- unresolved or partially solved objects that still have stable identity or anchoring
- conflict-heavy or issue-heavy areas that need review emphasis
- topology relations even when final geometry is still weak
- evidence and issue handles that let later review layers trace claims back to source support

If the neutral model knows something semantically but not yet metrically, Stage 8 should still be able to carry that fact into the scene graph.

---

## 7. Scene Graph Representation Contract

Stage 8 should define a browser-facing scene graph contract that remains semantically meaningful even before rich geometry exists.

### 7.1 Node kinds

Recommended node kinds include:

- object
- anchor
- zone
- surface
- opening
- issue-marker
- missing-coverage-marker

### 7.2 Edge kinds

Recommended edge kinds include:

- supports
- spans-between
- belongs-to
- contained-in
- aligned-with
- connected-to
- depends-on
- references-anchor

### 7.3 Geometry representation modes

Stage 8 should use representation modes rather than UI-specific styling rules.

Recommended modes include:

- none-symbolic
- point-marker
- line-proxy
- polyline-proxy
- planar-proxy
- volume-proxy
- placeholder-asset-ref
- external-mesh-ref
- ghost-unresolved

This allows Stage 8 to represent everything the model knows without forcing one rendering style too early.

### 7.4 Coordinate and transform contract

Stage 8 should record an explicit coordinate contract in the scene graph manifest.

Recommended fields include:

- units
- handedness
- up-axis
- local-origin strategy
- scene-origin reference

Stage 8 should prefer local scene offsets over giant global coordinates when browser precision would suffer.

The contract should remain explicit even if the exact browser renderer is chosen later.

### 7.5 Geometry maturity carry-through

Every node with spatial significance should preserve the Stage 6 geometry maturity status.

At minimum, the scene graph should preserve:

- semantic
- anchored
- schematic
- approximate
- metric
- unresolved

Stage 8 should not erase that maturity boundary just because a node is visualized.

---

## 8. What This Stage Outputs

Stage 8 should emit structured scene-graph artifacts.

Recommended output families:

- scene graph manifest
- scene node registry
- scene edge registry
- geometry payload registry
- layer registry
- filter index
- issue marker registry
- evidence-link registry
- viewpoint seed registry
- scene slice results

### 8.1 Scene graph manifest

The scene graph manifest should be the root contract for Stage 8 outputs.

It should contain:

- scene graph ID
- run ID
- scene generation cycle ID
- source Stage 6 model ID
- source Stage 7 verification run ID
- included Stage 6 slice IDs
- included Stage 7 slice result IDs
- scene graph version
- overall scene status
- scope policy such as verified-only or verified-plus-provisional
- coordinate contract
- links to node, edge, geometry, layer, issue, evidence, and slice artifacts

### 8.2 Scene node registry

The scene node registry should hold the browser-facing node records.

Recommended node fields:

- scene node ID
- node kind
- source neutral object ID or anchor ID when applicable
- source Stage 6 slice ID
- object family or semantic role
- display label when available
- transform or anchor reference
- geometry representation mode
- geometry payload reference when present
- geometry maturity
- epistemic state
- verification state
- issue references
- evidence references
- layer references
- filter tags
- review status

### 8.3 Scene edge registry

The scene edge registry should hold the browser-facing relationship records.

Recommended edge fields:

- scene edge ID
- source scene node ID
- target scene node ID
- edge kind
- source neutral relationship ID
- topology role
- epistemic state
- verification state
- issue references
- evidence references
- review status

### 8.4 Geometry payload registry

The geometry payload registry should describe what spatial payload each node can use.

This registry should be independent from later material, theme, or interaction decisions.

Recommended fields:

- geometry payload ID
- source scene node ID
- representation mode
- payload type
- payload reference or inline descriptor
- spatial extent or bounds when known
- coordinate frame reference
- maturity compatibility
- unresolved or approximate flags

### 8.5 Layer registry

The layer registry should organize scene content into useful browser-facing groups.

Recommended layer groups include:

- reference framework
- primary structure
- secondary structure
- surfaces and enclosure
- openings and placed elements
- unresolved or provisional
- issues and warnings
- evidence and review markers

### 8.6 Filter index

The filter index should let later browser layers query scene content efficiently.

Recommended filter dimensions include:

- object family
- level
- bay or zone
- geometry maturity
- verification state
- issue severity
- unresolved state
- inferred or approximate state
- subsystem

### 8.7 Issue marker registry

The issue marker registry should expose review-relevant Stage 7 outputs spatially.

Recommended fields:

- issue marker ID
- source Stage 7 issue ID
- target scene node or edge IDs
- severity
- category
- spatial anchor or transform reference
- linked evidence references
- review-queue linkage

### 8.8 Evidence-link registry

The evidence-link registry should preserve the bridge from scene entities back to source support.

Recommended fields:

- evidence link ID
- target scene node or edge ID
- source Stage 6 object or relationship ID
- linked evidence artifact IDs
- linked page, region, crop, or support artifact IDs when available
- lineage note or provenance summary

### 8.9 Viewpoint seed registry

Stage 8 should emit viewpoint seeds, not final UI camera behavior.

These seeds help later review layers jump to meaningful locations.

Recommended seed types include:

- object focus seed
- issue focus seed
- level overview seed
- subsystem overview seed
- unresolved cluster seed

### 8.10 Scene slice result contract

Each scene-generation slice should emit a structured slice result.

That result should record:

- scene slice ID
- scope definition
- Stage 6 artifacts consumed
- Stage 7 artifacts consumed
- nodes emitted
- edges emitted
- issue markers emitted
- blocked or skipped items
- overall slice status

Recommended slice status values:

- emitted
- emitted-with-provisional
- partial
- blocked
- waiting-on-stage7
- reroute-recommended

---

## 9. How Stage 8 Uses Stage 6 And Stage 7 Together

Stage 8 should combine the two upstream stages in a disciplined order.

Recommended order:

1. read the Stage 6 neutral model manifest
2. read the Stage 7 verification manifest
3. determine the allowed scene scope from orchestrator policy
4. load only the Stage 6 objects, relationships, anchors, and topology for that scope
5. load the matching Stage 7 slice results, issues, findings, and confidence adjustments
6. decide normal versus provisional versus blocked publication status for each item
7. emit scene nodes and edges from the surviving structural state
8. attach issues, verification state, evidence, and filter tags
9. write the scene graph artifacts back into shared storage

This keeps Stage 8 clearly downstream from synthesis and verification.

---

## 10. Relationship To Stage 6

Stage 6 is the structural source stage for Stage 8.

The boundary is:

- Stage 6 defines the neutral model
- Stage 8 expresses that model as a browser-facing scene graph

Stage 8 should preserve the Stage 6 semantics, anchors, topology, geometry maturity, unresolved state, and lineage.

If Stage 8 has to invent replacement structure because Stage 6 did not preserve enough information, the Stage 6 contract is insufficient.

---

## 11. Relationship To Stage 7

Stage 7 is the trust and issue source stage for Stage 8.

The boundary is:

- Stage 7 challenges the neutral model
- Stage 8 publishes the challenged model with its verification state visible

Stage 8 should not hide Stage 7 warnings.

It should surface them as:

- verification status on nodes and edges
- issue markers
- filterable warning and conflict state
- provisional scene content when allowed

---

## 12. Relationship To Stage 8A

Stage 8A should deepen Stage 8.

It should not redefine Stage 8 from scratch.

That means Stage 8 should already provide:

- stable scene node IDs
- stable scene edge IDs
- geometry representation modes
- evidence linkage
- issue linkage
- filterable semantic structure

Stage 8A can then add richer geometry, richer review ergonomics, and stronger browser interaction without changing the underlying scene truth.

---

## 13. Relationship To The Orchestrator

Stage 8 is orchestrator-controlled.

The orchestrator should decide:

- what scene scope to publish
- whether only verified slices may be shown or whether provisional slices may also be shown
- whether blocked slices become issue-only markers
- whether Stage 8 should emit a whole-scene graph or a smaller review bundle
- when Stage 8 should rerun after Stage 6 or Stage 7 changes

Stage 8 should not own workflow transitions.

It should publish scene artifacts and slice results back into the shared artifact space.

---

## 14. Design Rules

Stage 8 should follow these rules.

### Rule 1

Consume Stage 6 as the structural source and Stage 7 as the trust source.

### Rule 2

Do not re-synthesize or silently repair the model.

### Rule 3

Preserve unresolved, inferred, conflicted, and provisional state explicitly.

### Rule 4

Represent everything the model knows semantically, even when final geometry is not ready.

### Rule 5

Keep geometry representation mode separate from later UI styling.

### Rule 6

Preserve evidence and issue linkage for every review-relevant scene entity.

### Rule 7

Use stable scene IDs so later review layers and overrides remain durable.

### Rule 8

Prefer local scene coordinate strategies when browser precision would otherwise degrade.

---

## 15. Build Guidance (No UI)

This section describes how Stage 8 should be built as an artifact generation step.

It does not define the final browser UI.

### Recommended language and runtime

- Python 3.11 or newer
- backend scene-graph generation worker or scene publication agent under orchestrator control
- artifact-backed persistence on filesystem for POC

### Recommended packages

- `pydantic` for typed scene graph schemas
- `orjson` for fast JSON serialization
- `networkx` for graph translation and validation
- `numpy` optional for transform and bounds helpers
- `trimesh` optional for lightweight proxy geometry payload generation
- `shapely` optional for planar zones, openings, and footprint helpers

### Suggested file structure

```text
pipeline/
  stage8_scene_graph/
    __init__.py
    runner.py
    input_loader.py
    eligibility.py
    node_builder.py
    edge_builder.py
    geometry_registry.py
    issue_registry.py
    evidence_registry.py
    filter_index.py
    manifest_writer.py
    output_schema.py

outputs/
  runs/<run_id>/
    stage8/
      scene/
        manifest.json
        nodes/
          node-*.json
        edges/
          edge-*.json
        geometry/
          geometry-registry.json
          payload-*.json
        layers/
          layer-registry.json
          filter-index.json
        issues/
          issue-marker-*.json
        evidence/
          evidence-link-*.json
        viewpoints/
          viewpoint-seeds.json
      slices/
        scene-slice-*.json
      logs/
```

### Suggested backend flow

1. read the Stage 6 manifest and Stage 7 manifest
2. ask the orchestrator which scene scope is allowed
3. load only the needed Stage 6 and Stage 7 artifacts for that scope
4. apply the eligibility policy to decide normal, provisional, blocked, or issue-only publication
5. build scene nodes from objects, anchors, zones, openings, and surfaces
6. build scene edges from topology relations
7. assign geometry representation modes and geometry payload references
8. attach issue, evidence, maturity, and filter metadata
9. write the scene manifest and slice outputs back into the artifact space

Scene manifests, nodes, edges, geometry payloads, issue markers, evidence links, viewpoint seeds, and slice outputs published from this stage should conform to the canonical registry under `Schemas/stage8/`.

---

## 16. Exit Criteria

Stage 8 should not be considered successful just because it emitted JSON files.

It is successful when:

- the scene graph preserves the semantics of the Stage 6 model
- the scene graph preserves the trust and issue state from Stage 7
- browser-facing nodes and edges have stable IDs and stable source lineage
- geometry representation modes are explicit even when final UI detail is deferred
- unresolved, inferred, conflicted, and issue-heavy areas remain visible as state rather than hidden loss
- the resulting scene graph is ready for Stage 8A or later browser review layers to consume

Stage 8 may be partially complete for a run.

That is acceptable if the manifest and slice results state exactly what was emitted, skipped, blocked, or left provisional.

---

## 17. HOW TO

Use this stage after Stage 6 has produced a neutral model slice and Stage 7 has produced the trust and issue state for that slice.

Practical execution order:

1. read the Stage 6 and Stage 7 manifests for the allowed publication scope
2. let the orchestrator decide what verified or provisional slices may publish
3. load only the needed Stage 6 and Stage 7 artifacts for that scope
4. apply the eligibility policy to decide what becomes normal scene content, provisional content, or issue-only markers
5. build scene nodes, scene edges, geometry payload references, issue markers, evidence links, and filter metadata
6. write the manifest and slice outputs back into the shared artifact space under the canonical Stage 8 contracts
7. return the published scene bundle to the orchestrator for later Stage 8A or review-loop use

What to avoid:

- do not re-synthesize the model inside Stage 8
- do not hide blocked or issue-heavy content as if it were verified
- do not invent scene IDs that break lineage durability
- do not let UI styling concerns replace semantic publication rules

What good looks like:

- a stable browser-facing scene graph
- explicit verification and issue state on published content
- durable source lineage
- a scene bundle that Stage 8A can deepen without redefining the truth layer