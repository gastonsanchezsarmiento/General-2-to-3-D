# Stage 1 - Whole-Pack Reconnaissance

## 0. Purpose

Stage 1 is the first broad understanding pass over the pack.

Its job is to look across the full drawing set and answer:

- what kind of project this appears to be
- what kinds of sheets are present
- which sheets seem most important
- which object families are likely present
- where uncertainty is already visible

This is an orientation stage.

It is not the final extraction stage.

It is not the model-building stage.

---

## 1. Core Role

Stage 1 is the pack-level reconnaissance layer.

It should:

- read across the pack broadly
- establish early hypotheses
- identify page families and likely roles
- identify where the important information probably lives
- produce the first usable page atlas for the orchestrator
- surface uncertainty early

It should not:

- lock final sheet meaning
- extract all dimensions in detail
- build the neutral model
- silently promote weak guesses into facts

---

## 2. What This Stage Receives

Stage 1 receives the prepared outputs of Stage 0.

In the current testing mode, Stage 1 should be allowed to ingest the full Stage 0 preparation set.

That may include:

- all low-resolution page previews
- all high-resolution master renders
- page manifests
- image asset manifests
- source-document manifest
- page metadata
- title or sheet-number hints
- text-layer availability summary
- vector-availability summary
- optional deterministic preparation hints

This full-ingest mode exists because the workflow is still being tested for effectiveness.

Later, this can be narrowed so Stage 1 consumes only the minimal slice needed for reliable reconnaissance.

That later narrowing could be controlled by:

- configuration
- testing mode selection
- run profile
- a future UI control or slider

---

## 3. What This Stage Actually Does

Stage 1 should perform a broad orientation pass over the pack.

### 3.1 Read the pack as a set, not as isolated pages

Stage 1 should look across the whole set of pages and understand the pack as a coordinated drawing package.

It should pay attention to:

- file grouping
- page ordering
- repeated naming patterns
- title blocks
- sheet-number sequences
- obvious drawing families
- page density and likely information value

### 3.2 Produce first-pass page understanding

For each page, Stage 1 should try to identify early clues such as:

- likely sheet family
- likely page role
- likely discipline emphasis
- whether the page is probably a plan, elevation, section, detail, note sheet, schedule, or title/index sheet
- whether the page looks likely to be high-value for later reading

These are still provisional outputs.

### 3.3 Produce pack-level understanding

Stage 1 should try to answer broad questions such as:

- does this look like a structural pack, mixed pack, or broader technical set
- does the project appear warehouse-like, portal-frame-like, residential, or something else
- what object families are likely present
- which pages seem to anchor the spatial understanding of the project
- where important schedules, notes, details, and support pages may be located

### 3.4 Produce early uncertainty and follow-up signals

Stage 1 should explicitly identify what it does not know yet.

Examples:

- unclear sheet-role assignments
- missing or conflicting title information
- pages that appear important but are ambiguous
- unclear project type
- pages that need a more detailed reread later

This is critical because Stage 2 should plan around uncertainty rather than pretending the first read is complete.

---

## 4. What This Stage Outputs

Stage 1 should produce structured reconnaissance artifacts, not just prose.

Core outputs should include:

- pack reconnaissance summary
- page atlas
- initial page-role candidates
- initial importance ranking
- candidate object-family list
- early unresolved-question list
- notes about pages needing targeted follow-up

These outputs should be stable enough for Stage 2 to consume as planning inputs.

More specifically, Stage 1 should try to emit a reconnaissance package with fields such as:

- run ID
- source file list
- page list
- pack type hypothesis
- discipline hypothesis
- candidate project-type hypothesis
- candidate object families
- page atlas entries
- page-role candidates per page
- page importance ranking per page
- anchor-sheet candidates
- schedule-sheet candidates
- detail-sheet candidates
- note-sheet candidates
- uncertainty flags
- unresolved questions
- recommended next-look pages or regions

The output should remain broad and provisional.

It should not pretend to be the final extraction package.

---

## 5. Relationship To The Orchestrator

Stage 1 is not the main orchestrator.

Stage 1 is a bounded reconnaissance task under orchestrator control.

The orchestrator is the cross-stage reasoning role that:

- decides when Stage 1 should run
- decides what Stage 1 should receive
- decides whether Stage 1 runs in full-ingest or narrower mode
- reads the Stage 1 outputs afterward
- uses those outputs to construct Stage 2

In an early implementation, the same model family may perform both the orchestrator role and the Stage 1 reconnaissance task.

Even in that case, they should still be treated as logically separate roles.

That means Stage 1 should still write a distinct Stage 1 artifact package rather than leaving its output only in temporary conversational state.

The orchestrator should be understood as "awake" from the moment a run begins.

It first routes Stage 0.

Then, after Stage 0 artifacts exist, it invokes Stage 1 and waits for the Stage 1 outputs before planning Stage 2.

So Stage 1 does not awaken the orchestrator.

The orchestrator already exists as the controlling role for the run and uses Stage 1 as one of its tasks.

---

## 6. How It Communicates With The Orchestrator

Stage 1 should write its outputs into the shared project artifact space.

The communication pattern should be:

1. Stage 1 reads the Stage 0 artifacts selected for reconnaissance
2. Stage 1 writes pack-level and page-level reconnaissance artifacts
3. Stage 1 marks what is provisional, uncertain, or unresolved
4. The orchestrator reads those artifacts and uses them to construct Stage 2

So Stage 1 does not directly decide the whole workflow.

It informs the orchestrator.

---

## 7. Relationship To Stage 2

Stage 2 should primarily consume the Stage 1 outputs, supported by Stage 0 manifests.

That means Stage 2 should mainly read:

- pack reconnaissance summary
- page atlas
- page-role candidates
- page importance ranking
- unresolved questions

And it may support those with Stage 0 data such as:

- page IDs
- image paths
- page title hints
- sheet-number hints
- text-layer and vector-availability flags

Stage 2 should not need to rediscover the pack from scratch.

---

## 8. Current Operating Mode Versus Future Narrowing

The current decision is:

Stage 1 may ingest everything prepared by Stage 0.

This is acceptable for now because the project is still prioritizing effectiveness and understanding over strict intake minimization.

But this should be treated as a testing mode, not as a permanent architectural law.

The future narrower version of Stage 1 will likely:

- rely mainly on preview images
- only selectively use the high-resolution render set
- use manifests as navigation rather than trying to pass everything into a live reasoning context

That narrowing can happen later, once the team knows what full-ingest reconnaissance actually improves and what it only adds as noise.

---

## 9. Design Rules

Stage 1 should follow these rules.

### Rule 1

Stay broad and orienting.

### Rule 2

Do not treat first-pass page-role guesses as final truth.

### Rule 3

Output structured reconnaissance artifacts, not just summaries.

### Rule 4

Explicitly record unresolved questions.

### Rule 5

The current full-ingest approach is allowed for testing, but it should remain clearly marked as a configurable choice.

---

## 10. Build Guidance (No UI)

This section describes how Stage 1 should be built as a backend pipeline step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- OpenAI Responses API for the reconnaissance calls
- JSON artifacts as the machine-readable output
- markdown or text summaries only as optional human-readable companions

### Recommended packages

- `openai` for model calls
- `pydantic` for reconnaissance output schemas
- `orjson` for JSON writing
- `tenacity` for retries and backoff on model calls
- `Pillow` for image validation and lightweight preprocessing when needed
- standard library modules such as `pathlib`, `logging`, and `uuid`

If prompt-family templating becomes useful, add:

- `jinja2` for prompt-template rendering

### Suggested file structure

```text
pipeline/
	common/
		artifact_store.py
		model_config.py
		prompt_loader.py
	stage1/
		reconnaissance_runner.py
		prompt_builder.py
		image_loader.py
		schema.py
		writer.py
prompts/
	stage1/
		reconnaissance.md
outputs/
	runs/<run_id>/
		stage1/
			pack-reconnaissance.json
			page-atlas.json
			unresolved-questions.json
```

### Implementation notes

- Stage 1 may currently ingest the full Stage 0 preparation set for testing
- keep the output provisional and structured
- store the raw model output and the parsed JSON separately if possible
- write a stable reconnaissance package that Stage 2 can consume without re-reading the raw pages manually

---

## 11. Summary

Stage 1 is the whole-pack reconnaissance pass.

It takes the prepared outputs of Stage 0 and creates the first broad operational understanding of the pack.

For now, it may ingest the full preparation set so the workflow can be tested broadly.

Later, that can be narrowed.

Its output is what gives the orchestrator enough orientation to decide how the pack should actually be read in Stage 2.

---

## 12. HOW TO

Use this stage after Stage 0 has produced the preparation manifests and page assets for a run.

Practical execution order:

1. read the Stage 0 run manifest, page manifest, and image asset references
2. inspect the pack broadly rather than diving into detailed extraction immediately
3. identify likely sheet families, likely anchor sheets, likely object families, and obvious unknowns
4. write a structured reconnaissance package with pack-level understanding, page atlas, and unresolved questions
5. keep weak guesses explicit instead of promoting them into fixed truth
6. return the reconnaissance package to the orchestrator so Stage 2 can plan the next reads

What to avoid:

- do not treat reconnaissance as final extraction
- do not hide uncertainty behind overconfident page labels
- do not emit only prose when later stages need structured artifacts
- do not let this stage collapse into a one-shot summary with no reusable page atlas

What good looks like:

- a believable broad understanding of the pack
- a usable page atlas for the orchestrator
- explicit unresolved questions
- enough orientation for Stage 2 to build a real read plan