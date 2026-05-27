# Stage 4 - Optional PDF-Native Support Extraction

## 0. Purpose

Stage 4 provides optional support evidence to help resolve uncertainties found in Stage 3.

Its job is to run selective deterministic or PDF-native extraction only when the orchestrator decides it is useful.

Stage 4 is not the default reading backbone.

Stage 3 remains the primary vision-led reading path.

---

## 1. Core Role

Stage 4 is the support extraction layer.

It should:

- extract support artifacts from PDF-native and deterministic signals
- target only specific unresolved tasks, pages, or regions
- produce structured support outputs that can be traced to source evidence
- help reduce ambiguity in text, dimensions, marks, or repeated schedule patterns
- return machine-usable support data without replacing Stage 3 findings

It should not:

- run by default on every page
- become a hidden mandatory dependency
- overwrite Stage 3 evidence without traceable conflict handling
- silently promote low-confidence extracted values into facts

---

## 2. What This Stage Receives

Stage 4 should be invoked with narrow scope.

Primary inputs should include:

- run ID
- invocation ID
- source document ID
- target page IDs
- target region IDs when known
- uncertainty or escalation reason from Stage 3
- extraction objective type
- expected output contract

Useful supporting inputs may include:

- Stage 0 source document and page manifests
- Stage 0 image asset manifest
- Stage 2 task metadata
- Stage 3 unresolved notes and follow-up requests
- Stage 3 evidence references

Possible extraction objective types:

- schedule parse
- title block parse
- text layer extraction
- vector path hint extraction
- dimension candidate extraction
- repeated mark lookup

---

## 3. What This Stage Actually Does

Stage 4 should execute support extraction for clearly defined uncertainties.

### 3.1 Apply targeted support routines

Stage 4 should run only the routines needed for the requested objective.

Examples:

- run table extraction on a specific schedule zone
- read text layer snippets for a target area
- collect vector hints for a detail region
- extract dimension candidates around a flagged relation

### 3.2 Keep evidence traceability

Every extracted candidate should include source traceability.

At minimum, Stage 4 should preserve:

- source page ID
- region bounds when available
- extraction method
- confidence score when available
- raw value and normalized value when applicable

### 3.3 Produce support, not final truth

Stage 4 should emit candidate support artifacts.

These artifacts are evidence inputs for orchestrator and downstream stages.

Stage 4 should not finalize object models.

### 3.4 Report extraction quality and limits

Stage 4 should explicitly report:

- what was extracted successfully
- what could not be extracted
- low-confidence items
- parser ambiguities
- format anomalies

This keeps downstream decisions auditable.

---

## 4. What This Stage Outputs

Stage 4 should output typed support artifacts.

Core outputs should include:

- support artifact package metadata
- extracted schedule candidates
- extracted text snippets
- vector and geometry hints
- dimension candidates
- extraction warnings and unresolved items
- evidence trace references

Recommended Stage 4 output fields:

- run ID
- invocation ID
- task ID or escalation ID
- page IDs processed
- region IDs processed when known
- extraction objective type
- method or parser used
- candidate list
- per-candidate confidence
- source trace references
- quality and limitation notes

Outputs should be stable JSON artifacts, with optional markdown summaries for review.

---

## 5. Is Stage 4 Iterative

Yes, but only when orchestrator requests it.

Typical Stage 4 iteration patterns:

- rerun extraction with tighter region bounds
- switch extraction routine for the same target
- reprocess after Stage 3 narrows the uncertainty
- run a second pass for normalization and cleanup

Stage 4 should not self-loop indefinitely.

Iteration boundaries should be set by orchestrator policy.

---

## 6. Relationship To The Orchestrator

Stage 4 is fully orchestrator-controlled.

The orchestrator should decide:

- whether Stage 4 is invoked at all
- which uncertainties justify Stage 4 invocation
- which pages or regions are in scope
- what extraction objective is expected
- whether Stage 4 output is sufficient or requires rerun

Stage 4 should be treated as optional support.

Core policy:

- Stage 3 is default reading path
- Stage 4 is selective support path

This policy should remain explicit in code and artifacts.

---

## 7. How It Communicates With The Orchestrator

Stage 4 should read narrow task context and write structured support artifacts.

Communication pattern:

1. orchestrator creates a Stage 4 support task
2. Stage 4 runs requested extraction objective
3. Stage 4 writes typed support artifacts with traceability
4. Stage 4 reports quality, limits, and unresolved items
5. orchestrator routes results back to Stage 3, Stage 5, or both

Stage 4 should not directly re-route workflow transitions.

---

## 8. Relationship To Stage 3

Stage 4 supports Stage 3 when vision-led reads are insufficient for specific uncertainties.

Expected relationship:

- Stage 3 identifies uncertainty
- orchestrator decides if Stage 4 is justified
- Stage 4 produces support candidates
- Stage 3 or later packaging stages consume support evidence

Stage 4 should not replace Stage 3 direct observations.

It should enrich them.

---

## 9. Relationship To Stage 5

Stage 4 is a source stage for Stage 5 packaging.

Stage 5 should be able to ingest Stage 4 outputs as support evidence alongside Stage 3 findings.

To make this possible, Stage 4 outputs should be:

- typed
- evidence-linked
- source-traceable
- confidence-scored when possible
- explicit about limitations

This helps Stage 5 merge support artifacts without losing provenance.

---

## 10. Design Rules

Stage 4 should follow these rules.

### Rule 1

Do not run by default. Run only by orchestrator decision.

### Rule 2

Keep scope narrow and task-specific.

### Rule 3

Every extracted item must be source-traceable.

### Rule 4

Preserve confidence and uncertainty explicitly.

### Rule 5

Do not silently override Stage 3 findings.

### Rule 6

Output machine-usable artifacts, not only prose.

---

## 11. Build Guidance (No UI)

This section describes how Stage 4 should be built as a backend support-extraction step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- backend worker callable by orchestrator
- artifact-backed output persistence

### Recommended packages

- `pydantic` for typed extraction task and output schemas
- `orjson` for fast JSON serialization
- `tenacity` for retry and backoff
- `pymupdf` for PDF-native text and vector access
- `pdfplumber` optional for table and text extraction workflows
- `rapidfuzz` optional for schedule token matching and normalization
- standard library modules such as `pathlib`, `logging`, `uuid`, `re`, and `datetime`

### Suggested file structure

```text
pipeline/
  common/
    artifact_store.py
    ids.py
    schema_utils.py
  stage4/
    dispatcher.py
    text_layer_extractor.py
    table_extractor.py
    vector_hint_extractor.py
    dimension_extractor.py
    normalizer.py
    output_schema.py
    writer.py
outputs/
  runs/<run_id>/
    stage4/
      support-artifacts/
      extraction-logs/
      unresolved/
```

### Implementation notes

- keep each Stage 4 invocation tied to one orchestrator support task
- capture raw extraction output and normalized output separately when possible
- preserve method and parser metadata per candidate
- enforce strict schema validation before publishing support artifacts
- record failure modes explicitly so rerun strategies remain deterministic

---

## 12. Summary

Stage 4 is an optional support extraction stage.

It is orchestrator-invoked, narrow in scope, and evidence-traceable.

Its purpose is to reduce specific uncertainties, not to replace the vision-led reading backbone.

When implemented this way, Stage 4 improves robustness without turning into a hidden mandatory dependency.

---

## 13. HOW TO

Use this stage only when the orchestrator has a specific support-extraction objective that Stage 3 could not resolve confidently on its own.

Practical execution order:

1. let the orchestrator invoke one narrow support task with a clear objective type
2. load only the target pages, regions, and source artifacts needed for that objective
3. run the needed support routine such as text-layer extraction, vector hints, table parsing, or dimension extraction
4. keep raw extraction output and normalized support artifacts separate
5. validate the support artifacts before publishing them into shared artifact space
6. return control to the orchestrator so it can decide whether Stage 3 should reread the affected slice or whether Stage 5A now has enough evidence to package

What to avoid:

- do not run support extraction across the whole pack by default
- do not let Stage 4 overwrite Stage 3 evidence silently
- do not publish unvalidated support artifacts as if they were final truth
- do not let this stage become a hidden mandatory backbone

What good looks like:

- narrow deterministic support artifacts
- explicit extraction scope and method metadata
- failures recorded clearly enough for targeted reruns
- improved certainty without undermining the vision-led reading model