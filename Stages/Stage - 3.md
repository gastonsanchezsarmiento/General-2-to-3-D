# Stage 3 - Iterative Targeted Reading

## 0. Purpose

Stage 3 reads the important pages and regions in detail.

Its job is to take the read plan from Stage 2 and perform the actual focused reading work through orchestrated GPT-5.5 vision loops.

This is the first stage where the system starts to work at a meaningful reading depth.

It is not the final synthesis stage.

It is not the final review stage.

It is the detailed reading layer that turns the plan into actual evidence.

---

## 1. Core Role

Stage 3 is the targeted reading execution layer.

It should:

- read the pages or regions assigned by Stage 2
- focus on the most important pages first
- follow the anchor-sheet strategy chosen by the orchestrator
- produce evidence-linked findings
- separate direct observations from inferred observations
- support repeated reads when the first pass is incomplete

It should not:

- invent its own reading strategy
- replace the Stage 2 plan
- jump straight into final object synthesis
- silently promote guesses into facts

---

## 2. What This Stage Receives

Stage 3 receives the typed read plan from Stage 2.

Its main inputs are:

- read-plan summary
- task list
- task priorities
- task dependencies
- prompt-family assignments
- target page IDs
- target region IDs when known
- crop priorities when known
- support-escalation markers
- unresolved-question handling instructions

Stage 3 may also use supporting Stage 0 and Stage 1 artifacts when needed, especially:

- page manifest
- image asset manifest
- preview images
- high-resolution master renders
- page atlas
- page metadata
- title or sheet-number hints
- candidate page-role information

If optional support extraction has already been invoked for a task, Stage 3 may also receive support artifacts from Stage 4.

---

## 3. What This Stage Actually Does

Stage 3 performs detailed reading one task at a time or in a controlled small batch.

### 3.1 Read assigned sheets and regions

Stage 3 should read the targeted pages or regions from the Stage 2 plan.

The default bias should remain:

- plan-space first
- then vertical and relational follow-up

That means the stage should pay attention to:

- plan geometry
- object placement
- grids and levels
- openings
- structural members
- vertical logic
- notes and schedules
- detail references
- cross-sheet references

### 3.2 Produce evidence-linked observations

Every useful observation should be attached to evidence.

Stage 3 should try to record:

- what was directly seen
- what was derived from explicit evidence
- what was inferred schematically
- what is still unresolved

This distinction is essential.

### 3.3 Support follow-up reads

Stage 3 should be able to ask for more focused reads when the first pass is incomplete.

Examples:

- revisit a crop because text was unclear
- inspect a detail because a connection remains ambiguous
- re-read a schedule because a mark is unresolved
- widen the field of view because the first crop was too narrow

This is the core iterative behavior of the stage.

### 3.4 Produce page-level and region-level findings

Stage 3 should write findings that are useful both immediately and later.

It should be able to produce:

- per-sheet findings
- region findings
- object candidates
- relationship candidates
- direct-read observations
- inferred observations
- unresolved notes
- follow-up requests

### 3.5 Request support extraction when needed

Stage 3 may flag tasks for Stage 4 when the vision-led read is not enough.

This does not mean Stage 3 should automatically invoke Stage 4 every time.

It means Stage 3 should be able to say:

- vision-only was enough
- vision was not enough and support extraction should be requested
- the support path is optional but helpful here

---

## 4. What This Stage Outputs

Stage 3 should produce structured reading artifacts, not just prose.

Core outputs should include:

- per-sheet findings
- region findings
- object candidates
- relationship candidates
- direct-read observations
- inferred observations
- unresolved notes
- follow-up requests
- evidence references
- task completion status

More specifically, a Stage 3 output package should try to include fields such as:

- run ID
- task ID
- page IDs read
- region IDs read when known
- prompt family used
- evidence image IDs or crop IDs
- direct observations
- inferred observations
- unresolved questions still open
- reread requests
- support-escalation recommendations

These outputs should be stable enough that Stage 5 can later package them into a coherent observation layer.

---

## 5. Is Stage 3 Iterative

Yes.

Stage 3 is iterative by design.

The orchestrator should be able to learn from one read and request another more focused read.

Iteration in Stage 3 can happen when:

- a crop is too small
- a detail is still ambiguous
- a schedule mark remains unclear
- a page appears more important than first thought
- human steering changes priorities
- support extraction produces a conflicting or useful clue

The important difference is that Stage 3 is iterative inside the reading process, not because it is re-planning the whole workflow.

Stage 2 handles planning.

Stage 3 handles repeated reading.

---

## 6. Relationship To The Orchestrator

Stage 3 is orchestrated, not autonomous.

The orchestrator should:

- read the Stage 2 typed plan
- select which Stage 3 task to run next
- provide the relevant page or crop context
- decide whether Stage 3 needs a follow-up read
- decide whether Stage 4 support extraction should be triggered
- decide whether Stage 3 should be repeated with a different crop or page focus

Stage 3 should not decide the whole workflow.

It should execute the work assigned by the orchestrator and write the evidence back into shared artifacts.

In an implementation, the same model family may be used for orchestrator reasoning and Stage 3 reading.

Even then, the two roles should stay logically separate:

- the orchestrator chooses and routes tasks
- Stage 3 performs the reading task and writes the findings

Stage 3 output should be distinct enough that the orchestrator can inspect it and decide what happens next.

---

## 7. How It Communicates With The Orchestrator

Stage 3 should write its outputs into the shared project artifact space.

The communication pattern should be:

1. the orchestrator reads Stage 2 and selects a reading task
2. Stage 3 performs the targeted read
3. Stage 3 writes structured findings and evidence references
4. Stage 3 may emit follow-up requests or support-escalation markers
5. the orchestrator reads the outputs and decides the next action

So Stage 3 is not a one-way fire-and-forget reader.

It is a task-driven reading step that can trigger additional reading or downstream support.

---

## 8. Relationship To Stage 4

Stage 3 is the main vision-led reading layer.

Stage 4 is optional support extraction.

The relationship should be:

- Stage 3 tries vision-first reading
- Stage 3 notes when vision is insufficient
- Stage 3 can recommend Stage 4 for support evidence
- Stage 4 may then produce structured support artifacts
- Stage 3 or later stages may use those support artifacts to clarify unresolved items

Stage 3 should not depend on Stage 4 being always present.

But it should be able to ask for it when useful.

---

## 9. Relationship To Stage 5

Stage 3 is a source stage for Stage 5.

That means Stage 3 should produce findings that are clean enough to be packaged later.

Stage 5 will later collect, normalize, deduplicate, and group those findings.

So Stage 3 should preserve:

- evidence references
- observation types
- unresolved states
- conflict hints
- candidate object and relationship signals

If Stage 3 outputs are too freeform, Stage 5 will have to clean up too much noise.

---

## 10. Design Rules

Stage 3 should follow these rules.

### Rule 1

Use the Stage 2 plan as the mission.

### Rule 2

Stay evidence-linked.

### Rule 3

Preserve direct, derived, inferred, and unresolved distinctions.

### Rule 4

Be iterative when the first read is incomplete.

### Rule 5

Request support extraction only when vision is not enough.

### Rule 6

Do not silently turn reading into final synthesis.

---

## 11. Build Guidance (No UI)

This section describes how Stage 3 should be built as a backend reading pipeline step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- OpenAI Responses API for the vision reads
- JSON artifacts as the machine-readable stage output
- optional markdown summaries for human inspection

### Recommended packages

- `openai` for model calls
- `pydantic` for typed task and output schemas
- `orjson` for fast JSON serialization
- `tenacity` for retries and backoff
- `Pillow` for image validation and crop preparation
- `pymupdf` if Stage 3 needs local page access or crop extraction support
- standard library modules such as `pathlib`, `logging`, `uuid`, `dataclasses`, and `json`

### Suggested file structure

```text
pipeline/
  common/
    artifact_store.py
    model_config.py
    prompt_loader.py
    evidence_ids.py
  stage3/
    reader.py
    task_runner.py
    prompt_builder.py
    crop_loader.py
    output_schema.py
    writer.py
prompts/
  stage3/
    targeted_reading.md
outputs/
  runs/<run_id>/
    stage3/
      findings/
      observations/
      follow-ups/
      logs/
```

### Implementation notes

- run Stage 3 task-by-task, not as one giant unreadable pass
- keep each task output separate so it can be rerun independently
- store raw model outputs and parsed JSON separately if possible
- keep the evidence image IDs or crop IDs attached to every claim
- let Stage 3 emit a follow-up task request instead of forcing every uncertainty to be resolved immediately
- normalize published observations to `Schemas/core/observation.schema.json`
- normalize promoted candidate objects and relationships to the canonical core schemas before later stages depend on them

---

## 12. Summary

Stage 3 is the iterative targeted reading stage.

It takes the Stage 2 read plan and performs the actual detailed reading work.

It is evidence-linked, iterative, and orchestrated.

It does not build the final model.

It produces the detailed findings that later stages will package, synthesize, and verify.

---

## 13. HOW TO

Use this stage after Stage 2 has emitted a typed read plan.

Practical execution order:

1. let the orchestrator select one narrow reading task or one controlled small batch from the Stage 2 plan
2. load only the assigned pages, crops, and task context needed for that iteration
3. run the focused vision read for that task
4. write findings, observations, and any follow-up requests back into artifact space
5. if uncertainty remains, emit a follow-up task request or a Stage 4 support-escalation request instead of forcing resolution
6. return the task outputs to the orchestrator
7. let the orchestrator decide whether the next iteration is another Stage 3 task, a Stage 4 support task, or a move toward Stage 5A packaging
8. repeat task by task until the current slice is read well enough for packaging

What to avoid:

- do not read the whole pack in one giant pass
- do not invent your own routing logic separate from Stage 2 and the orchestrator
- do not silently convert direct reading into final synthesis
- do not hide uncertainty when a follow-up loop is the correct next action

What good looks like:

- narrow, evidence-linked reading loops
- outputs that are rerunnable independently
- explicit follow-up requests when the first read is insufficient
- orchestrator-controlled iteration scope rather than uncontrolled reading drift