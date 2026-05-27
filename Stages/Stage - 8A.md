# Stage 8A - Detailed Three.js Review Model

## 1. Goal

Build a richer browser review model from the Stage 8 scene graph without changing the underlying interpreted truth.

---

## 2. Purpose

Stage 8A exists to make the interpreted project easier for a human to inspect inside a browser review environment.

It should deepen the Stage 8 scene graph into a more inspectable model where:

- line-like members can become beams, columns, braces, rails, or other richer proxies
- walls, slabs, roofs, and openings can gain thickness or more informative sectional form
- lightweight placeholders can be replaced with richer low-cost geometry when the source maturity allows it
- evidence, issues, confidence state, and inferred geometry remain visible during inspection
- review-oriented interaction structures such as focus targets, pickable regions, and annotation anchors become explicit

This is still a review model.

It is not yet a BIM authoring model and it should not invent a second semantic truth layer.

---

## 3. Important Rule

Stage 8A must deepen Stage 8, not bypass it.

That means:

- Stage 8 remains the browser-facing semantic source of truth
- Stage 8A may enrich geometry, interaction, grouping, and presentation structure
- Stage 8A must preserve the verification, issue, provisional, and evidence state already decided upstream
- if Stage 8 does not publish a thing, Stage 8A should not silently add it as normal scene content

---

## 4. Primary Inputs

The primary Stage 8A inputs should be the published Stage 8 artifacts for the allowed review scope.

Required input families:

- Stage 8 scene graph manifest
- Stage 8 scene nodes
- Stage 8 scene edges
- Stage 8 geometry payloads
- Stage 8 layer registry
- Stage 8 filter index
- Stage 8 issue markers
- Stage 8 evidence links
- Stage 8 viewpoint seeds
- Stage 8 scene slice results

These inputs should carry canonical `schema_id` and `schema_version` values from `Schemas/stage8/`.

---

## 5. Secondary Inputs

Stage 8A may use upstream artifacts as supporting enrichment inputs when the Stage 8 payload deliberately points back to them.

Useful secondary inputs include:

- Stage 6 neutral objects and relationships
- Stage 6 spatial anchor registry
- Stage 6 geometry maturity registry
- Stage 6 topology graph
- Stage 7 verification manifest
- Stage 7 verification slice results
- Stage 7 verification issues
- Stage 7 verification findings
- Stage 7 confidence adjustments
- Stage 7 review-queue items when the browser should focus a reviewer on specific targets

These upstream artifacts should be used for enrichment, tooltips, traceability, and review emphasis.

They should not be used to bypass the Stage 8 publication policy.

---

## 6. Eligibility And Publication Rules

Stage 8A should only deepen entities that Stage 8 already published into the review path.

Recommended policy:

- verified Stage 8 entities may receive richer geometry and richer interaction affordances
- provisional Stage 8 entities may also be deepened when orchestrator policy allows it, but their provisional state must remain explicit
- blocked Stage 8 entities should remain issue-oriented markers, ghosted placeholders, or omitted from solid review geometry
- stale Stage 8 slices should produce stale Stage 8A bundles rather than silently refreshed-looking geometry

If Stage 8 published an issue-only marker instead of a normal object, Stage 8A should preserve that distinction.

---

## 7. Representation Contract

Stage 8A should preserve a stable mapping between review geometry and Stage 8 scene truth.

### 7.1 Review Entity Identity

Every review entity should trace back to one or more Stage 8 scene IDs.

Allowed patterns:

- one Stage 8 scene node to one Stage 8A review entity
- one Stage 8 scene node to many Stage 8A geometry fragments
- many Stage 8 scene nodes grouped into a review assembly only when each source link remains explicit

There should be no orphan Stage 8A geometry with no upstream lineage.

### 7.2 Geometry Deepening Modes

Recommended Stage 8A geometry modes:

- `proxy-solid` for thickened but still approximate structural solids
- `extruded-profile` for members that can be shown with a simple cross-section
- `surface-thickened` for walls, slabs, roofs, and similar surfaces
- `asset-placeholder` for recognizable families rendered by reusable lightweight assets
- `annotation-only` when the browser should expose an inspectable target without pretending solid geometry exists

Stage 8A should preserve the upstream geometry maturity and epistemic status alongside any richer render geometry.

### 7.3 Review State Overlay

Each review entity should retain enough state to show:

- whether the source claim is direct, derived, inferred, unresolved, or human-corrected
- the current confidence tier
- whether the entity is verified, verified-with-warnings, provisional, blocked, or stale
- linked issues, findings, and evidence targets
- geometry maturity and whether the richer geometry is approximate or source-backed

### 7.4 Coordinate Contract

Stage 8A should inherit the Stage 8 scene coordinate contract.

It may add local render transforms, camera presets, exploded review offsets, or section helpers, but those should be presentation transforms rather than semantic coordinate rewrites.

---

## 8. Output Families

Stage 8A should publish structured review-model artifacts.

Recommended output families:

- review model manifest
- review entity bundles
- geometry fragment artifacts
- material or profile registry
- interaction index
- issue presentation registry
- evidence presentation registry
- focus and viewpoint preset bundle
- review slice results

At this stage of the plan, these Stage 8A artifacts may remain stable stage-local templates rather than fully canonical schemas.

If they are written into the shared artifact space for repeated cross-stage consumption, they should preserve stable IDs, explicit source references, and a clear upgrade path to future `Schemas/stage8a/` contracts.

---

## 9. Recommended Review Model Manifest Fields

The review model manifest should act as the root index for Stage 8A outputs.

Recommended fields:

- review model ID
- run ID
- review-model generation cycle ID
- source Stage 8 scene graph ID
- source Stage 6 model ID when available through lineage
- source Stage 7 verification run ID when available through lineage
- included Stage 8 scene node IDs
- included Stage 8 scene edge IDs
- overall review model status
- coordinate contract summary
- review entity bundle refs
- interaction index ref
- issue presentation registry ref
- evidence presentation registry ref
- focus and viewpoint preset ref
- review slice result refs

---

## 10. Review Slice Result Contract

Each Stage 8A review slice should state what was deepened and what remained unresolved.

Recommended fields:

- review slice ID
- source Stage 8 slice ID
- source Stage 8 node and edge IDs included
- review entities emitted
- geometry fragments emitted
- issue presentation items emitted
- evidence presentation items emitted
- skipped or blocked targets
- stale dependencies if any
- exit status

Useful exit status values:

- emitted
- emitted-with-provisional
- partial
- blocked
- stale

---

## 11. Relationship To Stage 8

Stage 8 owns the semantic scene truth for the browser path.

The boundary is:

- Stage 8 defines what exists in the published review scope
- Stage 8A defines how that published scope is deepened into a richer inspectable model

If Stage 8A repeatedly has to invent missing identity, topology, issue linkage, or geometry mode data, the fix belongs upstream in Stage 8 or Stage 6 rather than inside the review model layer.

---

## 12. Relationship To Stage 10

Stage 10 should use the Stage 8A review model as an inspection surface, not as a freeform correction store.

That means:

- Stage 8A should expose stable pick targets and review anchors
- Stage 10 should record structured human review actions against those durable targets
- human corrections should flow back through the shared artifact space rather than living only inside transient browser state

---

## 13. Relationship To The Orchestrator

Stage 8A is orchestrator-controlled.

The orchestrator should decide:

- when the richer review model is worth generating
- what scene scope is allowed to deepen
- whether provisional content may appear in the richer review model
- whether a Stage 8A bundle is stale after Stage 6, Stage 7, or Stage 8 changes
- whether Stage 8A should regenerate a whole review model or only a narrow review slice

Stage 8A should not decide workflow transitions on its own.

---

## 14. Design Rules

Stage 8A should follow these rules.

### Rule 1

Never replace the Stage 8 scene graph as the semantic source of truth.

### Rule 2

Keep richer geometry separate from semantic truth and verification state.

### Rule 3

Preserve provisional, inferred, unresolved, and issue-heavy state explicitly.

### Rule 4

Use durable IDs and explicit source lineage for every review-relevant entity.

### Rule 5

Do not hide missing geometry by over-polishing low-confidence content.

### Rule 6

Preserve evidence jumps, issue jumps, and review focus targets as first-class artifacts.

### Rule 7

Allow partial refresh so small upstream changes do not force full browser-model rebuilds.

---

## 15. Build Guidance

Stage 8A is best treated as a review-model preparation step plus a browser consumer.

### Recommended backend runtime

- Python 3.11 or newer for enrichment and artifact generation
- orchestrator-controlled review-model worker for backend bundle creation

### Recommended browser runtime

- TypeScript with Three.js for rendering and interaction
- React Three Fiber optional if the eventual review app benefits from component composition

### Recommended packages

- backend: `pydantic`, `orjson`, `numpy`, `trimesh`, `shapely` optional
- browser: `three`, `three-mesh-bvh` optional, `zustand` or equivalent optional for review state orchestration

### Suggested file structure

```text
pipeline/
  stage8a_review_model/
    runner.py
    input_loader.py
    identity_mapper.py
    geometry_deepener.py
    interaction_index_builder.py
    issue_presentation_builder.py
    evidence_presentation_builder.py
    manifest_writer.py

frontend/
  review-app/
    src/
      model/
        reviewModelLoader.ts
        selectionIndex.ts
        focusPresets.ts
      viewer/
        sceneAssembler.ts
        issueOverlays.ts
        evidenceJumpLinks.ts

outputs/
  runs/<run_id>/
    stage8a/
      review-model/
        manifest.json
        entities/
        geometry/
        interaction/
        issues/
        evidence/
        viewpoints/
      slices/
      logs/
```

### Suggested backend flow

1. read the Stage 8 scene graph manifest for the allowed scope
2. load only the Stage 8 nodes, edges, geometry payloads, issues, evidence links, and slice results needed for that scope
3. load upstream Stage 6 or Stage 7 artifacts only where Stage 8 lineage or detail references require them
4. decide which scene entities receive richer geometry and which remain annotation-only or issue-only
5. build review entities and geometry fragments with durable source mappings
6. build interaction indexes, focus presets, issue presentations, and evidence presentations
7. write the review model manifest and slice outputs into the shared artifact space
8. let Stage 10 consume those outputs for structured human review

---

## 16. Exit Criteria

Stage 8A is successful when:

- every emitted review entity is traceable to Stage 8 scene truth
- richer geometry does not hide unresolved or provisional state
- evidence and issue links remain navigable
- partial or stale regions are clearly marked rather than silently blurred together
- the resulting review model is ready for Stage 10 structured human inspection

Stage 8A may be partially complete.

That is acceptable if the manifest and slice results state exactly what was deepened, what stayed schematic, what was skipped, and what is stale.

---

## 17. HOW TO

Use this stage after Stage 8 has produced a scene graph that is semantically stable enough for richer browser inspection.

Practical execution order:

1. let the orchestrator choose the review scope and freshness policy
2. read the Stage 8 manifest and only the scene artifacts needed for that scope
3. preserve Stage 8 IDs as the stable backbone for all Stage 8A entities
4. deepen geometry only where maturity and policy justify it
5. keep issue-heavy or low-confidence areas visibly approximate
6. emit explicit interaction, issue, evidence, and focus artifacts
7. write slice-level output so the review model can refresh incrementally
8. route the resulting review bundle to Stage 10 for structured human inspection

What to avoid:

- do not rebuild semantic truth from raw Stage 6 objects inside the browser layer
- do not let rich rendering hide weak evidence or blocked verification state
- do not let UI-only identifiers become the primary review target IDs
- do not store important review context only in transient client memory

What good looks like:

- a richer model that is still honest about uncertainty
- stable click targets tied to durable artifact IDs
- strong issue and evidence navigation
- partial refresh support when upstream slices change