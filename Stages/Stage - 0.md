# Stage 0 - Ingestion And Preparation

## 0. Purpose

Stage 0 prepares the drawing pack for the rest of the workflow.

Its job is to turn the incoming source files into a clean, traceable, reusable working set of assets and manifests.

It is not an interpretation stage.

It should not decide what the drawings mean.

It should only prepare the material that later stages will use.

---

## 1. Core Role

Stage 0 is the pack-preparation and run-initialization layer.

It should:

- accept the source files
- create a run container for the current processing attempt
- register the source files and page structure
- render page imagery for later vision use
- record whether text layers and vector content are available
- produce manifests and asset references that the orchestrator can consume

It should not:

- classify the pack semantically as a final truth
- decide what each sheet means
- extract structural objects
- create model objects
- produce final page-role claims

---

## 2. What This Stage Receives

Stage 0 should receive the raw project pack and basic run settings.

Typical inputs:

- one or more PDF files
- optional image files if the pack is not fully PDF-based
- optional filenames or user-supplied labels
- run configuration
- project identifier
- source location metadata

The preferred default assumption is that the input is one or more PDFs.

---

## 3. What This Stage Actually Does

Stage 0 should perform the following work.

### 3.1 Create the run container

Before touching interpretation, the stage should create a run-level working container.

This should include:

- run ID
- project ID
- timestamp
- source manifest
- processing configuration snapshot
- output folder structure

This is the traceability backbone for the rest of the pipeline.

### 3.2 Register the source documents

The stage should inspect each source file and register it in the project manifest.

For each source file, record:

- source file ID
- original filename
- file type
- page count if applicable
- file size
- checksum or stable hash
- source path or storage URI

This allows reruns, audits, and reproducibility.

### 3.3 Split the pack into page records

If the source is a PDF, Stage 0 should create a page-level record for every page.

Each page record should receive a stable page ID.

For each page, record:

- source file ID
- page number
- page dimensions if available
- orientation or rotation
- sheet number if already deterministically available
- page label if available

This is a registration step, not a semantic understanding step.

### 3.4 Render page imagery

Yes, this stage should render PDF pages into images for the first vision read.

But it should not reduce the project to only images.

It should usually create at least two raster forms:

1. low-resolution preview images for Stage 1 whole-pack reconnaissance
2. high-resolution master renders for later crops, tiles, and targeted reads

Recommended behaviour:

- preview render for orientation and pack-level reading
- high-resolution PNG render for detailed later use
- preserve the original source files unchanged

The high-resolution render is the base surface for later crop extraction and evidence traceability.

### 3.5 Record non-raster availability

Stage 0 should also determine what other usable representations exist.

For each page, it should record whether there is:

- embedded text layer
- vector geometry
- raster-only content
- likely scanned content
- low-confidence OCR need

This is critical because the orchestrator may later decide whether to rely on vision alone or request support extraction.

### 3.6 Record render and page metadata

For every rendered page asset, record:

- image ID
- page ID
- render DPI
- width in pixels
- height in pixels
- image format
- whether the render is preview or master
- mapping back to the original page

Stage 0 should preserve enough information so later crops and tiles can be traced back to exact page coordinates.

### 3.7 Produce optional preparation hints

Stage 0 may produce weak preparation hints when this can be done deterministically.

Examples:

- title block region candidates
- drawing index region candidates
- candidate page labels
- candidate sheet numbers
- candidate schedule-heavy pages

These are only hints.

They must not be treated as final interpretation.

---

## 4. What This Stage Outputs

Stage 0 should write artifacts, not prose.

Core outputs should include:

- project manifest
- run manifest
- source document manifest
- page manifest
- preview image set
- high-resolution render set
- page metadata summary
- text-layer availability summary
- vector availability summary
- optional preparation-hints artifact

These outputs should be stable, inspectable, and reusable by later stages.

They should also be narrow enough that the orchestrator can retrieve only the parts needed for the next task rather than loading every asset into context at once.

---

## 4A. Recommended Manifest Fields

At minimum, the Stage 0 manifests should make it possible to answer:

- what source files were uploaded
- how many pages exist
- what the stable IDs are for files, pages, and images
- where the preview and master images live
- whether text or vector support exists per page
- whether any deterministic title or sheet hints are available

Recommended page-level fields include:

- project ID
- run ID
- source ID
- page ID
- page number
- preview image ID
- master image ID
- preview image path
- master image path
- page title hint when available
- title source when available
- sheet number hint when available
- sheet number source when available
- page width and height
- render DPI for preview and master
- text-layer available
- vector-content available
- likely scanned
- rotation

These fields do not all need to live in one file.

They may be split across a run manifest, page manifest, and image asset manifest as long as the contracts remain stable.

---

## 5. How It Communicates With The Orchestrator

Stage 0 should communicate through artifacts and manifests, not through hidden conversation state.

The communication pattern should be:

1. Stage 0 writes its outputs into the project artifact space
2. Stage 0 marks its status as complete, partial, or failed
3. The orchestrator reads the resulting manifests
4. The orchestrator decides whether Stage 1 can begin

So the orchestrator and Stage 0 are separate.

Stage 0 is not the orchestrator.

Stage 0 is a preparation worker or subsystem under orchestrator control.

---

## 6. Relationship To Stage 1

Stage 0 and Stage 1 must stay separate.

### Stage 0

- prepares files
- registers pages
- renders images
- records technical availability
- emits manifests

### Stage 1

- performs the first broad GPT-5.5 vision read
- uses the preview images and metadata
- produces orientation, page atlas, and early hypotheses

The important handoff rule is:

Stage 0 makes all prepared artifacts available to the orchestrator.

In the long-term architecture, Stage 1 will often consume only a narrow slice of them.

However, in the current testing mode, Stage 1 may ingest the full Stage 0 preparation set.

That full set may include:

- preview images
- high-resolution master renders
- page manifests
- image asset manifests
- page metadata
- deterministic title or sheet hints when available
- text-layer and vector-availability summaries

The narrower future operating mode would normally emphasize:

- preview images
- page IDs and page numbers
- source file relationships
- page metadata
- deterministic title or sheet hints when available

The high-resolution render set would usually remain staged for later targeted reading rather than being pushed into the first broad reconnaissance pass.

For now, though, the system should allow Stage 1 to ingest everything from Stage 0 if that is the chosen testing configuration.

Stage 0 should finish before Stage 1 begins.

Stage 1 should never have to guess whether the page assets exist.

---

## 7. Should This Stage Use The OpenAI API

Usually, Stage 0 should be mostly local processing.

Typical Stage 0 work does not require a model call.

It is mainly:

- file handling
- PDF inspection
- page rendering
- metadata registration
- optional deterministic preprocessing

If an implementation later introduces model-assisted region proposal in Stage 0, that should be treated as optional and carefully bounded.

The default design should keep Stage 0 non-interpretive and mostly model-free.

---

## 8. API Key Implications

Stage 0 does not imply a separate API key by itself.

If Stage 0 is only doing local preparation, it may need no model key at all.

If later stages use OpenAI for vision or reasoning, that would normally use the same OpenAI API key as the rest of the orchestrated workflow.

Separate keys would only be needed if:

- another vendor is used for OCR
- another vendor is used for deterministic extraction
- another service is used for storage, queues, or external processing

The distinction is by external service, not by stage number.

---

## 9. Entry Conditions

Stage 0 can begin when:

- source files have been provided
- a project ID or run context can be created
- local processing tools for PDF rendering are available

Stage 0 should fail early if the source files are unreadable or missing.

---

## 10. Exit Conditions

Stage 0 is complete when:

- all source files have been registered
- page manifests exist
- preview renders exist
- high-resolution renders exist or failure has been explicitly logged
- text/vector availability has been recorded
- run status and artifact manifests have been written

Stage 0 should not silently succeed with missing critical artifacts.

---

## 11. Failure Modes To Watch

The system should explicitly detect and record problems such as:

- unreadable or corrupt PDFs
- password-protected files
- missing pages
- blank pages
- rotation errors
- failed renders
- very large pages that exceed local processing limits
- scanned pages with poor legibility
- broken text layers
- source duplication or revision conflicts

These should be written into preparation logs, not hidden.

---

## 12. Design Rules

Stage 0 should follow these rules.

### Rule 1

Do not interpret the project here.

### Rule 2

Do not collapse all representations into a single raster-only view.

### Rule 3

Keep stable IDs for files, pages, and rendered assets.

### Rule 4

Preserve coordinate traceability from render to page.

### Rule 5

Write reusable artifacts so reruns do not require repeating the same preparation work unnecessarily.

### Rule 6

Any page-role or region signal produced here is only a hint until later stages confirm it.

---

## 13. Practical Output Shape

At a practical level, Stage 0 should leave behind a folder and manifest structure that looks roughly like this:

- source files
- per-page preview renders
- per-page master renders
- page manifest
- run manifest
- preparation logs
- optional deterministic page hints

The exact file structure may change, but the architectural requirement is stable:

Stage 0 must leave the project in a state where Stage 1 can start reading immediately and the orchestrator can inspect what is available without reopening the whole source pack manually.

---

## 14. Build Guidance (No UI)

This section is about how this stage should be built in the current backend-oriented phase.

No UI decisions are included here.

### Recommended language and runtime

- Python 3.11 or newer
- local filesystem artifact store for the POC
- JSON artifacts as the machine-readable source of truth
- optional SQLite index later if artifact lookup becomes hard to manage by files alone

Python is the most practical choice here because it is strong for PDF processing, image handling, file orchestration, and later OpenAI pipeline integration.

### Recommended packages

- `pymupdf` for PDF inspection, page access, rendering, and text-layer probing
- `Pillow` for image handling and validation
- `pydantic` for manifest and artifact schemas
- `orjson` for fast JSON serialization
- standard library modules such as `pathlib`, `hashlib`, `json`, `logging`, `uuid`, and `sqlite3` when needed

Avoid introducing OCR or external extraction services into the base Stage 0 build unless they are explicitly being tested.

### Suggested file structure

```text
pipeline/
	common/
		artifact_store.py
		ids.py
		paths.py
		schema_utils.py
	stage0/
		ingest.py
		source_registry.py
		pdf_probe.py
		page_renderer.py
		manifest_models.py
		writer.py
outputs/
	runs/<run_id>/
		manifests/
		pages/
		logs/
```

### Implementation notes

- keep Stage 0 mostly model-free
- write JSON manifests first, then mark the stage complete
- use stable IDs for sources, pages, and images
- keep original files unchanged
- treat rendered assets and manifests as reusable cached outputs
- publish Stage 0 run and page artifacts against the canonical registry under `Schemas/stage0/` and shared reference types under `Schemas/common/`
- register any new shared manifest family in `Schemas/registry.json` before downstream stages depend on it

---

## 15. Summary

Stage 0 is the clean setup stage for the entire workflow.

It turns a raw drawing pack into a structured preparation layer made of page assets, manifests, metadata, and availability summaries.

It does not understand the drawings yet.

It makes understanding possible.

---

## 16. HOW TO

Use this stage at the beginning of every run, immediately after a project upload or source-pack selection.

Practical execution order:

1. receive the source files, project ID, and run configuration
2. create the run container and configuration snapshot
3. register every source document before any interpretation begins
4. probe each PDF for page count, page size, text-layer availability, and vector availability
5. render the page images needed for downstream vision work
6. write the run manifest, page manifest, and image asset references into the shared artifact space
7. validate the published Stage 0 artifacts against the canonical registry
8. return control to the orchestrator so Stage 1 can start from structured preparation rather than raw files

What to avoid:

- do not mutate the source files
- do not classify sheet meaning as if Stage 0 were an interpretation stage
- do not hide page-render or probe failures inside vague logs
- do not force later stages to reopen raw PDFs just to learn basic availability facts

What good looks like:

- stable run and page manifests
- reusable page imagery
- explicit availability summaries
- a preparation layer that Stage 1 can read immediately