# Stage 7 - Verification

## 0. Purpose

Stage 7 challenges the synthesized neutral model before it is treated as trustworthy.

Its job is to test whether the Stage 6 model is actually supported, coherent, and safe to carry forward.

This is not the visual review stage.

This is not the human override stage.

This is the machine-side challenge stage that tries to break weak claims before later stages visualize or operationalize them.

---

## 1. Core Role

Stage 7 is the verification and invalidation layer.

It should:

- challenge the Stage 6 neutral model independently from the synthesis pass
- inspect whether evidence supports committed objects and relationships
- inspect whether cross-sheet consistency holds
- inspect whether topology is coherent
- inspect whether geometry is plausible for its stated maturity level
- inspect whether schedule-backed facts match model claims
- inspect whether inferred and approximate values are still acceptable as provisional state
- publish structured findings, issue objects, confidence adjustments, and rerun recommendations

It should not:

- silently re-synthesize the model
- invent new geometry or topology as a hidden repair step
- overwrite Stage 6 artifacts destructively
- collapse conflicts to force a clean pass result
- replace later human review

---

## 2. Important Rule

Verification is a separate stage, not an afterthought.

The system should not rely only on the same synthesis logic that built the model to decide that it is correct.

Where practical, verification should be independent enough to reduce agreement bias.

---

## 3. What This Stage Receives

Stage 7 receives the Stage 6 neutral-model artifacts and the lineage needed to challenge them.

Primary inputs should include:

- run ID
- verification cycle ID
- Stage 6 neutral model manifest
- Stage 6 verification-readiness summary
- Stage 6 object records
- Stage 6 relationship records
- Stage 6 spatial anchor registry
- Stage 6 topology graph artifacts
- Stage 6 unresolved model-state artifacts
- Stage 6 conflict-linked model-state artifacts
- Stage 6 synthesis slice results
- orchestrator verification instructions

Supporting inputs should include:

- Stage 5 package lineage references
- evidence linkage references back to Stage 3 and Stage 4 artifacts
- prior verification results when rerunning
- project profile modules when verification logic depends on domain expectations

---

## 4. What This Stage Actually Does

Stage 7 should behave like a controlled challenge workflow.

### 4.1 Select a verification slice

Stage 7 should not verify the whole neutral model in one giant pass.

It should work on narrow verification slices selected by the orchestrator.

Example slices:

- one object family
- one level
- one grid zone
- one structural subsystem
- one high-risk or conflict-heavy subset
- one set of recently changed Stage 6 deltas

### 4.2 Retrieve model state and evidence lineage

For the selected slice, Stage 7 should load:

- relevant neutral-model objects
- relevant neutral-model relationships
- relevant anchors and topology edges
- relevant unresolved and conflict state
- the evidence chain behind the claims

Stage 7 should challenge the model through the artifact registry, not hidden chat memory.

### 4.3 Run evidence-support checks

Stage 7 should verify whether the evidence actually supports the committed claim.

This includes checks such as:

- object exists but evidence chain is too weak
- relationship exists but source evidence is missing or mismatched
- value was labeled direct even though it was only inferred

### 4.4 Run cross-sheet consistency checks

Stage 7 should compare model claims against cross-sheet evidence.

This includes checks such as:

- plan versus elevation mismatch
- plan versus schedule mismatch
- section versus topology mismatch
- detail-derived geometry conflicting with model anchors

### 4.5 Run topology coherence checks

Stage 7 should verify whether the graph of structural relations makes sense.

This includes checks such as:

- unsupported spans
- disconnected supports
- missing primary nodes in a frame
- relations that imply impossible or contradictory load path logic

### 4.6 Run geometry plausibility checks

Stage 7 should check whether geometry is plausible for the object's current maturity level.

It should not require metric completeness from schematic objects.

But it should still flag cases such as:

- anchored geometry that cannot fit its own supports
- slopes inconsistent with eaves and ridge logic
- impossible offsets or span order
- dimensions that contradict their own anchors

### 4.7 Run dimension and approximation checks

Stage 7 should inspect:

- directly read dimensions
- derived dimensions
- inferred approximate dimensions
- unresolved dimensions

It should verify whether inferred dimensions remain clearly flagged, justified, and safe enough to keep as provisional state.

### 4.8 Emit verification findings

Stage 7 should write structured findings rather than freeform critique only.

These findings should drive confidence changes, issue creation, invalidation, and rerun routing.

---

## 5. What Stage 7 Is Allowed To Modify Directly

Stage 7 may annotate, downgrade, and invalidate.

It should be allowed to:

- write verification findings
- write issue objects
- adjust confidence or support status
- mark objects or relationships as conflicted or unresolved
- mark a slice as verified, warned, blocked, or stale
- publish rerun recommendations and invalidation scope

Stage 7 should usually not:

- create new structural objects
- reposition objects creatively
- rewrite topology freely
- silently upgrade unresolved claims into resolved ones
- perform hidden repairs that should belong to Stage 6 or earlier stages

The guiding rule is:

- verification may annotate
- verification may downgrade
- verification may invalidate
- verification should not silently re-synthesize

---

## 6. How This Stage Checks Stage 6 Output

Stage 7 checks the Stage 6 output through structured artifact reads.

It should not rely on one giant prompt containing the whole model.

Recommended verification pattern:

1. read the Stage 6 model manifest
2. read the verification-readiness summary
3. select a verification slice
4. retrieve only the relevant object, relationship, anchor, topology, unresolved, and conflict artifacts
5. retrieve the evidence lineage for those artifacts
6. run challenge checks against that slice
7. write structured verification artifacts back into shared storage

This keeps verification narrow, auditable, and cheap enough to rerun selectively.

---

## 7. How It Communicates With The Orchestrator

Stage 7 should communicate with the orchestrator through artifact-space outputs, not hidden internal state.

The communication pattern should be:

1. orchestrator selects a verification slice
2. Stage 7 reads the relevant Stage 6 artifacts for that slice
3. Stage 7 writes verification findings, issue objects, confidence adjustments, and rerun recommendations
4. Stage 7 writes a verification slice result with explicit status
5. orchestrator reads those outputs and decides whether to:
   - accept the slice
   - accept with warnings
   - route back to Stage 6 for a local rebuild
   - route back to Stage 3 or Stage 4 for stronger evidence
   - route back to Stage 2 if planning was wrong
   - hold the slice for later human review

This keeps the workflow artifact-driven and auditable.

---

## 8. Artifact Space And Ownership

Yes.

All meaningful verification state should be saved in the shared artifact space.

Stage 7 should own verification artifacts.

It should not destructively overwrite Stage 6 model artifacts.

Instead, it should write:

- verification manifests
- verification slice results
- verification findings
- issue objects
- confidence adjustments
- conflict confirmations or escalations
- invalidation and rerun recommendations

This preserves auditability and lets the orchestrator reason from durable state.

Stage ownership should remain clear:

- Stage 6 owns neutral-model synthesis artifacts
- Stage 7 owns verification artifacts
- orchestrator owns routing, invalidation decisions, and rerun planning artifacts

---

## 9. Verification Output Families

Stage 7 should output structured verification artifacts.

Recommended output families:

- verification manifest
- verification slice results
- verification findings
- issue registry
- confidence-adjustment artifacts
- contradiction or conflict records
- invalidation recommendations
- rerun recommendations
- review-queue items

---

## 10. Verification Manifest

The verification manifest should be the root contract for Stage 7 outputs.

It should contain:

- verification run ID
- run ID
- verification cycle ID
- source Stage 6 model ID
- source Stage 6 slice IDs verified
- verification version
- overall verification status
- links to findings, issues, confidence adjustments, invalidation recommendations, rerun recommendations, review-queue artifacts, and any conflict records carried forward

---

## 11. Verification Slice Result Contract

Each verification slice should emit a structured slice result.

That result should record:

- verification slice ID
- slice scope definition
- Stage 6 artifacts checked
- findings created
- issues created
- confidence adjustments applied
- invalidation scope recommendation
- rerun recommendation
- exit status

Recommended exit status values:

- verified
- verified-with-warnings
- partial-failure
- blocked
- reroute-stage6
- reroute-stage3
- reroute-stage4
- reroute-stage2
- human-review-recommended

---

## 12. Issue Objects

When Stage 7 detects a failure that requires tracking rather than a trivial note, it should emit an issue object.

Recommended issue fields:

- issue ID
- severity
- category
- target reference
- evidence references
- finding summary
- reproduction or verification context
- suggested next action
- rerun recommendation
- status

Useful severity values:

- critical
- major
- minor
- enhancement

Useful category values:

- schema-mismatch
- hallucination
- missing-data
- logic-error
- topology-error
- cross-sheet-contradiction
- geometry-plausibility-failure
- unsupported-inference

---

## 13. Confidence Adjustments

Stage 7 should be able to adjust confidence or support levels without rewriting the model itself.

Confidence adjustments should be used when:

- evidence is weaker than Stage 6 implied
- inferred values were acceptable but weak
- contradictions reduce trust without fully invalidating the slice
- strong verification evidence justifies a higher confidence tier

These adjustments should be explicit artifacts rather than hidden state.

---

## 13A. Good Enough Policy

Stage 7 should make the machine-side exit criteria explicit.

A verification slice is good enough to move forward only when the foundational claims in that slice remain sound at the slice's stated maturity level.

### 13A.1 Verified

A slice should return `verified` when:

- no critical issues exist
- no major issues affect object identity, spatial anchoring, core topology, or evidence lineage
- every committed object and relationship in scope retains source traceability
- any inferred or approximate values are explicitly flagged and allowed by the current synthesis policy
- remaining unresolved items are secondary rather than foundational

### 13A.2 Verified-with-warnings

A slice should return `verified-with-warnings` when:

- core object identity, anchoring, and topology remain sound
- no critical issues exist
- any major issues are confined to non-foundational attributes and do not make the slice misleading
- open weaknesses are limited to secondary geometry, dimensions, labeling, or other reviewable details
- the slice is still safe to carry forward as provisional state

### 13A.3 Reroute Or Block

A slice should return `partial-failure`, a reroute status, or `blocked` when any of the following is true:

- object existence is unsupported or materially contradicted
- spatial anchoring is unstable
- core topology is contradictory or structurally misleading
- committed claims are missing required evidence lineage
- an inferred or approximate value was used where policy did not allow it
- unresolved items are foundational enough that downstream use would be misleading

### 13A.4 Human-review-recommended

A slice may return `human-review-recommended` when:

- the machine-side gate is passable or near-passable
- a semantically important ambiguity remains visible
- presenting the slice to a human is more valuable than forcing another immediate machine rerun

---

## 14. Invalidation And Rerun Policy

A failing verification should invalidate only the dependent slice when possible.

Stage 7 should recommend targeted invalidation rather than whole-run resets.

Recommended invalidation types:

- direct invalidation when a specific object or relationship is unsound
- relational invalidation when graph associations are wrong
- structural invalidation when the synthesis branch for a slice is conceptually wrong

The orchestrator should use these outputs to mark the minimum stale downstream set.

---

## 15. Relationship To The Orchestrator

Stage 7 is orchestrator-controlled.

The orchestrator should decide:

- what verification slice to run
- whether verification is mandatory before moving forward
- how to apply the Stage 7 good-enough policy and any run-specific overrides to trigger reroute
- whether a failure should route to Stage 6 or earlier stages
- whether the slice may proceed with warnings
- whether human review should be scheduled immediately

The orchestrator should read Stage 7 artifacts and decide the workflow transition.

Stage 7 should not own the workflow.

---

## 16. Relationship To Stage 6

Stage 6 is the immediate source stage for Stage 7.

The boundary is:

- Stage 6 synthesizes the neutral model
- Stage 7 challenges the neutral model

Stage 7 should use Stage 6 manifests, objects, relationships, anchors, topology, unresolved state, conflicts, and lineage as verification input.

If Stage 7 repeatedly has to compensate for poor Stage 6 artifact structure, the Stage 6 contract is not doing its job.

---

## 17. Relationship To Stage 8 And Human Review

Stage 7 sits before browser-facing visualization and later human review.

Its outputs should help later stages by:

- identifying issue markers
- flagging low-confidence areas
- preserving contradictions
- creating review-queue targets
- marking which slices are safe to visualize as verified versus provisional

Stage 7 is not a replacement for human review.

It is the machine-side challenge pass that prepares safer downstream review.

---

## 18. Design Rules

Stage 7 should follow these rules.

### Rule 1

Verification must be separate from synthesis.

### Rule 2

Write all meaningful verification state into the shared artifact space.

### Rule 3

Use narrow verification slices, not one giant verification prompt.

### Rule 4

Annotate, downgrade, and invalidate when needed, but do not silently re-synthesize.

### Rule 5

Preserve evidence lineage for every challenged claim.

### Rule 6

Prefer targeted invalidation and rerun over whole-run resets.

### Rule 7

Keep verification outputs structured enough for orchestrator routing and later human review.

---

## 19. Build Guidance (No UI)

This section describes how Stage 7 should be built as a backend verification step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- backend verification worker or verification agent under orchestrator control
- artifact-backed persistence on filesystem for POC

### Recommended packages

- `pydantic` for typed verification schemas
- `orjson` for fast JSON serialization
- `tenacity` for retry and backoff
- `networkx` for topology checks and graph traversal
- `jsonschema` optional for schema and artifact validation checks
- standard library modules such as `pathlib`, `logging`, `uuid`, `datetime`, and `collections`

### Suggested file structure

```text
pipeline/
  common/
    artifact_store.py
    ids.py
    schema_utils.py
    provenance.py
  stage7/
    verifier.py
    slice_selector.py
    evidence_checker.py
    consistency_checker.py
    topology_checker.py
    geometry_checker.py
    issue_builder.py
    invalidation_recommender.py
    output_schema.py
    writer.py
outputs/
  runs/<run_id>/
    stage7/
      verification/
        manifest.json
        slice-results/
        findings/
        issues/
        confidence/
        invalidation/
        rerun/
        review-queue/
        conflicts/
      logs/
```

### Implementation notes

- use artifact handles and indexes rather than large payload passing
- keep verifier state in artifacts, not hidden chat memory
- make verification rerunnable slice by slice
- preserve the exact Stage 6 artifact references that were challenged
- keep issue and rerun outputs machine-readable for orchestration
- publish verification manifests, slice results, findings, issues, confidence adjustments, invalidation recommendations, rerun recommendations, and review-queue items against the canonical registry under `Schemas/stage7/`
- validate shared artifact `schema_id` and `schema_version` before trusting upstream payloads

---

## 20. HOW TO

Use this stage after Stage 6 has produced a neutral model slice that is ready to be challenged.

Practical execution order:

1. read the Stage 6 model manifest and verification-readiness summary
2. let the orchestrator select one verification slice
3. load only the objects, relationships, anchors, topology edges, unresolved state, and conflicts for that slice
4. load the evidence lineage behind those claims
5. run evidence, consistency, topology, geometry, and dimension checks
6. emit structured findings and issue objects
7. emit a verification slice result with explicit status
8. write invalidation and rerun recommendations into artifact space
9. let the orchestrator decide whether to accept, warn, reroute, or escalate

What to avoid:

- do not verify the entire model in one giant prompt
- do not mutate Stage 6 model artifacts destructively
- do not let the verifier silently repair the model
- do not keep important verification reasoning only in temporary memory

What good looks like:

- evidence-backed verification findings
- explicit issue objects
- targeted invalidation scope
- clear rerun recommendations
- structured communication back to the orchestrator