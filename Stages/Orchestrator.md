# Orchestrator Specification

## 0. Purpose

This document defines the orchestrator as the controlling role of the workflow.

It explains when the orchestrator starts, what it can access, what it decides, and how it routes work across stages.

---

## 1. What The Orchestrator Is

The orchestrator is not a single stage.

It is the cross-stage control role that:

- reads shared artifacts
- decides what runs next
- assembles narrow task context
- invokes stage workers
- validates outputs
- routes retries and follow-ups
- keeps the run coherent

The orchestrator is the execution brain of the system.

Stages are specialized workers.

---

## 2. When The Orchestrator Enters

The orchestrator should be considered active from run start.

It enters at Stage 0 and remains the controlling role through the entire run.

High-level lifecycle:

1. create or load run context
2. route Stage 0 ingestion and preparation
3. route Stage 1 reconnaissance
4. generate Stage 2 read plan
5. route Stage 3 targeted reading tasks
6. optionally route Stage 4 support extraction tasks
7. route Stage 5A coherent observation packaging
8. route Stage 5B visual interpretation feedback when required
9. record whether human approval exits the first milestone loop or whether human feedback routes it backward
10. route Stage 6 synthesis slices
11. route Stage 7 verification slices
12. decide whether verified or provisional model slices may publish into Stage 8
13. route Stage 8 scene graph generation
14. route Stage 8A richer browser review model generation when needed
15. route Stage 10 human review actions and resulting reruns

So the orchestrator does not wake at Stage 2.

Stage 2 is where orchestrator planning behavior becomes most visible.

---

## 3. Access To Shared Artifact Space

Yes.

The orchestrator should have direct read and write access to the shared artifact space.

It should use that space as its primary memory and coordination mechanism.

The orchestrator should:

- read run manifests
- read stage outputs
- write control artifacts
- write routing decisions
- write rerun decisions
- write stage status updates

It should not depend on long hidden conversation context as the main source of continuity.

---

## 4. What The Orchestrator Reads

Typical read inputs include:

- run manifest
- project manifest
- stage output packages
- task lists
- unresolved-question lists
- conflict and issue artifacts
- verification findings
- human review actions

For the first milestone and downstream review loops, the orchestrator should also read:

- Stage 5A package manifests and readiness summaries
- Stage 5B board manifests, card artifacts, and feedback targets
- Stage 6 neutral model manifests, slice results, and unresolved or conflict state
- Stage 7 verification manifests, slice results, issues, and rerun recommendations
- Stage 8 scene graph manifests and slice results
- Stage 8A browser review artifacts when present

For Stages 3 and 4 specifically, the orchestrator reads:

- Stage 2 read-plan package
- Stage 3 task outputs and follow-up flags
- Stage 4 support artifacts when invoked

---

## 5. What The Orchestrator Writes

Typical orchestrator-owned outputs should include:

- next-task routing decisions
- stage invocation records
- stage status transitions
- task context bundles
- escalation decisions
- rerun decisions
- invalidation scope decisions
- milestone approval decisions
- scene publication policy decisions
- review-loop routing decisions

Recommended orchestrator artifacts:

- orchestrator-state.json
- task-queue.json
- routing-log.json
- stage-status.json
- rerun-plan.json
- milestone-decisions.json
- publication-policy.json

These can be renamed, but the behavior should remain explicit and inspectable.

---

## 6. Relationship To Stage 3 And Stage 4

Yes, the orchestrator should command what happens in Stage 3 and Stage 4.

### Stage 3

The orchestrator should:

- select the next Stage 3 task from Stage 2 plan
- provide narrow context for that task
- decide whether a follow-up read is needed
- decide when Stage 3 can stop for that task

### Stage 4

The orchestrator should:

- decide whether Stage 4 is needed
- decide which Stage 3 uncertainties justify support extraction
- decide where Stage 4 results feed back
- prevent Stage 4 from becoming the default backbone silently

Core rule:

Stage 3 is default reading.

Stage 4 is optional support under orchestrator control.

---

## 6A. Relationship To Stage 5A And Stage 5B

The orchestrator is the coordinator, recorder, and router for the first milestone.

Human approval is the authority that exits the first loop.

### Stage 5A

The orchestrator should:

- decide when a Stage 5A packaging cycle is triggered
- decide which upstream reading and support artifacts are in scope
- read the Stage 5A package manifest and readiness summary
- decide whether the package is ready for first-milestone human review

### Stage 5B

The orchestrator should:

- decide whether Stage 5B is required for the current run or slice
- decide which interpretation slice or board scope should be shown
- read Stage 5B board artifacts, feedback targets, and recorded human actions
- route human-requested loop backs to Stage 2, Stage 3, Stage 4, or Stage 5A

Core rule:

Stage 5A and Stage 5B together form the first milestone checkpoint.

The human decides whether that checkpoint is approved for exit from the loop.

The orchestrator records that human decision and routes the next action.

---

## 6B. Relationship To Stage 6 And Stage 7

The orchestrator controls the machine-side model loop.

### Stage 6

The orchestrator should:

- allow Stage 6 to start only after first-milestone human approval has been recorded
- decide which synthesis slice runs next
- decide what inference policy is allowed for that slice
- decide whether unresolved items may pass through or must block

### Stage 7

The orchestrator should:

- decide which verification slice runs next
- decide what severity thresholds trigger reroute
- read verification findings, issues, invalidation recommendations, and rerun recommendations
- decide whether a slice is accepted, accepted with warnings, rerouted, or held for later human review

Core rule:

Stage 6 synthesizes.

Stage 7 challenges.

The orchestrator decides how that loop continues.

---

## 6C. Relationship To Stage 8, Stage 8A, And Stage 10

The orchestrator controls what becomes visible in downstream review.

### Stage 8

The orchestrator should:

- decide what verified or provisional scope may publish into the scene graph
- decide whether blocked slices become issue-only or missing-coverage markers
- route Stage 8 scene-generation slices

### Stage 8A

The orchestrator should:

- decide when the richer browser review model is needed
- decide whether Stage 8 output is sufficient to deepen into Stage 8A
- route partial reruns when the review model needs refresh after upstream changes

### Stage 10

The orchestrator should:

- read structured human review actions
- decide whether those actions route back to Stage 6, Stage 7, Stage 8, or earlier stages
- record invalidation scope and rerun plans

Core rule:

The orchestrator should treat the downstream browser path as a controlled review loop, not as a detached frontend concern.

---

## 7. Orchestrator Decision Model

At each step, the orchestrator should answer:

1. what is the current stage state
2. what is still missing
3. what is the next highest-value task
4. what narrow context is needed for that task
5. what output contract is expected
6. what escalation rule applies if output is insufficient

This keeps execution controlled and auditable.

---

## 8. Orchestrator State Machine

A minimal state machine can be:

- initialized
- preparing
- reconnaissance
- planning
- targeted-reading
- support-extraction
- packaging-5a
- interpretation-board-5b
- milestone-review
- synthesis
- verification
- scene-graph
- detailed-review-model
- human-review
- export-ready
- blocked
- complete

The orchestrator should move between these states based on artifact evidence, not ad hoc chat decisions.

---

## 9. Should There Be A Separate Orchestrator File

Yes.

A separate orchestrator specification is recommended and should be maintained as a first-class contract.

Why:

- stage files define worker behavior
- orchestrator file defines control behavior
- keeping them separate reduces ambiguity
- execution planning becomes easier to audit and improve

This file is that contract baseline.

---

## 10. Build Guidance (No UI)

### Recommended language and runtime

- Python 3.11 or newer
- backend service or job runner process
- artifact-backed persistence on filesystem for POC

### Recommended packages

- pydantic for typed task and state models
- orjson for fast artifact serialization
- tenacity for retry and backoff around stage invocations
- networkx optional for dependency graph handling
- standard library modules such as pathlib, logging, uuid, datetime, and sqlite3 when needed

### Suggested backend structure

```text
pipeline/
  orchestrator/
    controller.py
    state_machine.py
    task_queue.py
    context_builder.py
    router.py
    rerun_manager.py
    models.py
  common/
    artifact_store.py
    ids.py
    logging_utils.py
outputs/
  runs/<run_id>/
    orchestrator/
      orchestrator-state.json
      task-queue.json
      routing-log.json
      stage-status.json
      rerun-plan.json
```

### Implementation notes

- keep decisions explicit in artifacts
- keep stage calls idempotent where possible
- never rely on hidden context as the only continuity source
- make rerun scope explicit to avoid full-run resets unnecessarily
- keep first-milestone approval state explicit before Stage 6 begins
- keep scene publication policy explicit before Stage 8 begins
- validate shared stage outputs against the canonical schema registry before advancing orchestrator state
- keep task and state control artifacts separate from interpretation payload schemas even when both are typed and versioned

---

## 11. Summary

The orchestrator is the persistent control role across all stages.

It has access to the shared artifact space, decides what happens next, records and routes the human decision at the Stage 5A and Stage 5B first milestone, controls the Stage 6 and Stage 7 machine loop, and controls what becomes visible in the Stage 8, Stage 8A, and Stage 10 review path.

Stages perform specialized work.

The orchestrator keeps the whole run coherent.

---

## 12. HOW TO

Use the orchestrator from run start to run end as the controlling role of the workflow.

Practical execution order:

1. create or load the run state and the current artifact-backed context
2. inspect stage status, unresolved state, milestone decisions, and queued work
3. choose one narrow next task, milestone checkpoint, or rerun action
4. assemble only the artifact context needed for that decision or worker invocation
5. invoke the target stage worker and persist the invocation record
6. validate the resulting outputs, including canonical schema checks for published artifacts
7. decide whether to advance, loop, reroute, escalate to human review, or pause for input
8. write the routing decision, updated stage status, and rerun scope back into artifact space
9. repeat until the run reaches a terminal or waiting state

What to avoid:

- do not rely on hidden chat continuity as the real workflow state
- do not route huge monolithic tasks when narrower slices exist
- do not skip milestone approval gates just because downstream work is possible
- do not let reruns happen implicitly with no recorded scope decision

What good looks like:

- explicit routing decisions
- inspectable task queues and stage status
- targeted reruns instead of full-run resets
- stable continuity across long-running multi-stage workflows