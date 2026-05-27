# Stage 2 - Orchestrator Read-Plan Generation

## 0. Purpose

Stage 2 turns broad reconnaissance into an actual reading strategy.

Its job is to answer:

- what should be read next
- in what order it should be read
- which pages should anchor understanding first
- which prompt family should be used for each task
- what each later reading task is expected to return

This is the stage where the system stops saying "this pack probably contains these things" and starts saying "this is how we will read it."

It is a planning and routing stage.

It is not the extraction stage.

It is not the synthesis stage.

---

## 1. Core Role

Stage 2 is the execution-planning layer for the orchestrator.

It should:

- consume the Stage 1 reconnaissance outputs
- decide which information matters most
- decide which sheets or regions should be read first
- choose plan-anchor sheets before expanding to elevations, sections, details, and schedules
- decide whether optional support extraction should be requested later
- define typed reading tasks for Stage 3

It should not:

- directly perform the detailed reading itself
- create final model objects
- silently resolve uncertainty that Stage 1 marked as unresolved
- blur into Stage 3 by writing freeform reading notes instead of an actual plan

---

## 2. What This Stage Receives

Stage 2 should primarily consume the outputs of Stage 1.

Its main inputs are:

- pack reconnaissance summary
- page atlas
- page-role candidates
- page importance ranking
- candidate object families
- anchor-sheet candidates
- uncertainty flags
- unresolved questions
- recommended next-look pages or regions

Stage 2 may also use supporting Stage 0 artifacts when needed, especially:

- page manifest
- image asset manifest
- preview image paths
- master image paths
- title hints
- sheet-number hints
- text-layer availability
- vector-content availability

Stage 2 should not need to rediscover the pack from scratch.

It should plan from the reconnaissance package and only reach back to Stage 0 artifacts when those artifacts sharpen routing decisions.

---

## 3. Is Stage 1 Output Detailed Enough For Stage 2

Yes, if Stage 1 produced the outputs defined in Stage 1.

Stage 2 does not need detailed extraction values yet.

It needs planning-grade information.

That means Stage 1 is detailed enough for Stage 2 if it can answer questions like:

- which pages are probably plans
- which pages are probably elevations or sections
- which pages look schedule-heavy
- which pages appear central to understanding the structure
- which uncertainties are important enough to shape the read plan

If Stage 1 cannot answer those questions, then the problem is not that Stage 2 needs more detail.

The problem is that Stage 1 reconnaissance was too weak.

What Stage 2 adds is not deeper sheet understanding.

What it adds is task structure.

---

## 4. What This Stage Actually Does

Stage 2 should convert reconnaissance into a typed plan.

### 4.1 Decide what the project most likely is

Stage 2 should review the Stage 1 hypotheses and determine the most operationally useful current interpretation of the pack.

This does not mean forcing certainty where none exists.

It means choosing the working hypothesis that will guide reading order.

Examples:

- portal-frame structural pack
- mixed architectural plus structural pack
- residential drawing pack
- technical set with unclear discipline boundaries

### 4.2 Decide what must be collected

Stage 2 should determine what categories of information the system actually needs in order to progress.

Typical collection goals include:

- plan-level spatial anchors
- major object families
- grid and level framework
- vertical logic from elevations or sections
- schedules and marks
- key detail sheets
- major unresolved ambiguities

### 4.3 Choose reading order

Stage 2 should choose a deliberate reading sequence.

The preferred default is:

1. anchor plan or ground-level sheets
2. supporting plan-adjacent pages
3. elevations and sections
4. schedules
5. details
6. special follow-up regions

This preserves the MainPlan3 rule that spatial understanding should be grounded from the plan upward.

### 4.4 Create typed reading tasks

Stage 2 should create specific tasks for later readers.

Each task should specify things such as:

- task ID
- task type
- target page IDs
- target regions if known
- prompt family
- expected output shape
- collection goal
- escalation rule
- whether support extraction may be requested

This is one of the most important outputs of the stage.

### 4.5 Define what remains unresolved

Stage 2 should explicitly preserve unresolved questions.

It should not erase Stage 1 uncertainty just to make the plan look cleaner.

Instead, it should decide whether each unresolved item should be:

- addressed by Stage 3 reading
- deferred until later
- surfaced to human steering
- left open until more evidence exists

### 4.6 Decide whether Stage 4 is a possible support path

Stage 2 should decide whether optional PDF-native support extraction should be available as a later branch.

This does not mean Stage 2 must invoke Stage 4 immediately.

It means Stage 2 can mark certain tasks as:

- vision-first only
- vision-first with possible support escalation
- support-friendly if ambiguity persists

---

## 5. What This Stage Outputs

Stage 2 should produce a typed read-plan package.

Core outputs should include:

- read-plan summary
- working project hypothesis
- collection goals
- ordered reading sequence
- per-task reading instructions
- prompt-family assignments
- crop priorities when already known
- support-escalation markers
- unresolved-question handling plan

More specifically, a Stage 2 output package should try to include fields such as:

- run ID
- plan version
- working project hypothesis
- prioritized information goals
- anchor-sheet list
- task list
- task dependency list
- prompt family per task
- target pages per task
- target regions per task when known
- expected output schema per task
- support-eligible tasks
- human-review escalation candidates
- still-unresolved issues

---

## 6. Relationship To The Orchestrator

Stage 2 is the most direct expression of the orchestrator role.

If Stage 1 is a bounded reconnaissance worker, Stage 2 is where the orchestrator becomes most visible as a planning intelligence.

Stage 2 is still a stage with its own outputs, but unlike Stage 1, it is much closer to the orchestrator itself.

The orchestrator should:

- read the Stage 1 artifacts
- perform or supervise Stage 2 planning
- write the Stage 2 read-plan package
- use that package to route Stage 3 tasks

In a practical implementation, Stage 2 may be performed directly by the orchestrator rather than by a separate worker.

That is acceptable.

But even then, Stage 2 should still produce a distinct artifact package so the plan is inspectable and reusable.

So the answer here is:

Stage 2 is not separate from the orchestrator in the same way that Stage 1 is.

Stage 2 is usually the orchestrator acting in its planning mode.

---

## 7. How It Communicates With The Orchestrator

Because Stage 2 is usually the orchestrator in planning mode, the communication pattern is slightly different from Stage 1.

The orchestrator:

1. reads Stage 0 and Stage 1 artifacts
2. produces the Stage 2 read-plan package
3. writes that plan into shared artifacts
4. uses that plan to launch or route Stage 3 tasks

So the important communication rule is not Stage 2 back to the orchestrator.

It is Stage 2 into the shared artifact space so later steps can be audited, rerun, and understood.

---

## 8. Relationship To Stage 3

Stage 3 should not decide its own mission from scratch.

It should receive that mission from Stage 2.

That means Stage 3 should inherit from Stage 2:

- task list
- task order
- page targets
- region targets when known
- prompt family selection
- expected output shape
- escalation rules

If Stage 3 starts behaving like it is inventing the reading strategy itself, then Stage 2 has failed or the boundary has blurred.

---

## 9. Design Rules

Stage 2 should follow these rules.

### Rule 1

Produce a typed read plan, not a loose narrative.

### Rule 2

Choose plan-anchor reading first unless a strong reason exists not to.

### Rule 3

Preserve unresolved questions explicitly.

### Rule 4

Do not perform detailed extraction here.

### Rule 5

Do not silently turn support extraction into the backbone of the workflow.

### Rule 6

Make the read plan inspectable enough that a human can understand why the next tasks were chosen.

---

## 10. Build Guidance (No UI)

This section describes how Stage 2 should be built as a backend orchestration-planning step.

No UI work is included here.

### Recommended language and runtime

- Python 3.11 or newer
- the same backend runtime as the orchestrator
- JSON read-plan artifacts as the machine-readable source of truth
- optional markdown planning notes only as a secondary human-readable output

### Recommended packages

- `openai` for orchestrator planning calls when the plan is model-generated
- `pydantic` for typed read-plan and task schemas
- `orjson` for JSON serialization
- `tenacity` for retries
- `jinja2` if prompt families are stored as templates
- standard library modules such as `pathlib`, `logging`, `uuid`, and `dataclasses` where useful

Avoid treating this stage as a generic chat exchange.

The output should be a typed plan package.

### Suggested file structure

```text
pipeline/
	common/
		artifact_store.py
		model_config.py
		prompt_loader.py
	stage2/
		planner.py
		task_models.py
		prompt_builder.py
		dependency_builder.py
		writer.py
prompts/
	stage2/
		read_plan_generation.md
outputs/
	runs/<run_id>/
		stage2/
			read-plan.json
			task-list.json
			plan-summary.md
```

### Implementation notes

- Stage 2 is usually the orchestrator acting in planning mode
- keep the plan versioned so revised plans can be compared later
- separate the task list from the human-readable summary
- make Stage 3 consume the typed task package rather than ad hoc freeform instructions
- publish the read plan against the canonical registry under `Schemas/stage2/read-plan.schema.json`
- make each task declare the expected downstream `schema_id` rather than leaving output shape implied

---

## 11. Summary

Stage 2 is the read-plan generation stage.

It consumes the broad reconnaissance outputs of Stage 1 and turns them into an actual reading strategy.

It is where the orchestrator becomes most concrete as a planning role.

Its output should tell the rest of the system what to read, in what order, for what purpose, with which prompt family, and under which escalation rules.

---

## 12. HOW TO

Use this stage after Stage 1 has produced a broad reconnaissance package that is good enough to route detailed reading.

Practical execution order:

1. read the Stage 1 reconnaissance package, page atlas, and unresolved questions
2. choose the first anchor sheets and the highest-value early reads
3. define typed Stage 3 tasks with priorities, dependencies, prompt families, and expected downstream outputs
4. mark where Stage 4 support extraction may be needed if Stage 3 encounters specific uncertainty types
5. write a versioned read-plan package plus task list and summary
6. return control to the orchestrator so Stage 3 can execute the plan task by task

What to avoid:

- do not perform detailed reading inside the planning stage
- do not leave the plan as vague prose with no typed task boundaries
- do not hide escalation rules that later stages will need
- do not make downstream output shape implicit when a schema contract is already known

What good looks like:

- a readable and inspectable plan
- narrow, typed reading tasks
- explicit priorities and dependencies
- a plan package that the orchestrator can revise without losing continuity