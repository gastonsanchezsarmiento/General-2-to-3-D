# Playbooks Guide

This file explains how [playbooks.py](./playbooks.py) works, why it exists, where it is used in the pipeline, and how to change it safely.

## What This File Is For

The playbook system is the human-editable policy layer for how the pipeline should read different types of structural drawing packs.

In plain terms, it answers:

- What kind of pack are we probably looking at?
- Which pages should matter more for this type of pack?
- What should Stage 2 emphasize when building the read plan?
- What should Stage 3 emphasize when reading a plan sheet versus an elevation sheet versus a detail sheet?
- What concepts should Stage 5 expect to see if the run covered the pack properly?

The core module lives in [playbooks.py](./playbooks.py).

## Mental Model

Think of a playbook as a reading policy, not as a model or an agent.

The model still performs the reasoning, but the playbook biases that reasoning.

It does that in four main ways:

1. It helps Stage 1 choose one active policy for the run.
2. It changes which pages get pushed toward the front of the queue.
3. It changes the natural-language instructions sent to Stage 2 and Stage 3.
4. It changes what Stage 5 considers "covered enough" for that pack family.

## The Main Objects

### `CoverageTarget`

Defined in [playbooks.py](./playbooks.py), this is the smallest completeness-check unit.

Each target has:

- `key`: internal identifier
- `label`: human-readable name
- `description`: what the target means
- `keywords`: words used to search the run outputs
- `required`: whether missing it should count as a coverage miss

This is used later by `evaluate_coverage()`.

### `ReadingPlaybook`

Also defined in [playbooks.py](./playbooks.py), this is the main configuration object.

A playbook contains:

- `key`: stable internal key
- `label`: UI-friendly name
- `description`: summary of what the policy is for
- `focus_items`: global priorities for Stage 3 reading
- `priority_keywords`: keywords that boost page ranking
- `stage2_biases`: guidance injected into Stage 2 planning
- `stage3_notes`: extra notes grouped by page-reading category
- `coverage_targets`: concepts Stage 5 should expect to see mentioned

## The Registry

All playbooks live in the `PLAYBOOKS` dictionary in [playbooks.py](./playbooks.py).

Today the built-in registry contains:

- `generic_structural_pack`
- `warehouse_portal_frame`
- `warehouse_tilt_panel`
- `steel_frame_industrial`

The default fallback is controlled by `DEFAULT_PLAYBOOK_KEY`.

If nothing specialized matches, the system falls back to the generic structural policy.

## How A Playbook Is Chosen

Selection is handled by `choose_playbook()` in [playbooks.py](./playbooks.py).

It returns a tuple:

- `playbook`
- `source`
- `rationale`

That means the system not only chooses a playbook, it also records why it chose it.

### Selection order

The function follows this order:

1. explicit user override
2. Stage 1 hypothesis matching
3. generic fallback

### Example

If Stage 1 produces something like:

- `project_type_hypothesis = "warehouse structural pack"`
- `candidate_object_families = ["portal_frame", "column", "beam"]`

then `choose_playbook()` will usually select `warehouse_portal_frame`.

If the user explicitly chooses a playbook in the UI, that override wins.

## Where It Is Used In The Pipeline

### Stage 1: choose the active playbook and bias important pages

In [openai_pipeline.py](./openai_pipeline.py), Stage 1 calls `choose_playbook()` after it builds the page atlas and pack synthesis, then calls `prioritize_pages()`.

Relevant references:

- [openai_pipeline.py](./openai_pipeline.py)
- [playbooks.py](./playbooks.py)

What happens here:

1. Stage 1 classifies pages broadly.
2. Stage 1 synthesizes the whole pack.
3. The code picks one active playbook.
4. The code ranks likely high-value pages using that playbook.
5. The chosen playbook key, source, rationale, focus items, and prioritized page ids get written into `Stage1Reconnaissance`.

This is why playbooks affect the run very early, even before Stage 2 builds the read plan.

### Stage 2: build planner guidance

Stage 2 uses `get_playbook()` and `build_stage2_guidance()` in [openai_pipeline.py](./openai_pipeline.py).

The important thing here is that Stage 2 does not read the registry directly. It reads the already-selected playbook and converts it into planner instructions.

`build_stage2_guidance()` turns the playbook into plain English such as:

- which page families to prioritize
- which concepts to protect
- which page ids were playbook-prioritized

That guidance is then injected into the Stage 2 prompt.

### Stage 3: build reading instructions for each task

Stage 3 uses `get_playbook()` and `build_stage3_instructions()` in [openai_pipeline.py](./openai_pipeline.py).

This is one of the most important parts of the system.

The Stage 3 instruction block is composed from four layers:

1. a stable structural-reading base
2. the playbook's global `focus_items`
3. generic notes for the prompt category from `BASE_STAGE3_NOTES`
4. the playbook's extra notes for that category from `stage3_notes`

So a portal-frame playbook does not usually create a brand-new reading mode. Instead, it strengthens the existing reading modes like `plan`, `elevation`, and `detail`.

### Australian drawing conventions

The current milestone should be tuned first for Australian structural drawing sets.

In practice, that means the base Stage 3 notes should treat the following as high-value evidence when visible:

- title or index sheets: NCC/BCA references, Australian Standards, issue status, revision history, design criteria notes, and structural sheet numbering patterns such as S000, S100, S200, S300, and S400
- schedules: exact mark syntax, member section notation, concrete strength, reinforcement notation, base plate marks, hold-down bolt marks, footing tags, and references to typical details
- cross references: when a plan mark is only defined elsewhere, link it to the schedule, detail, section, or elevation instead of resolving it from the plan view alone

This matters because Australian packs often hide governing structural truth in title sheets, general notes, and schedules rather than only in the main drawing views.

### Stage 5A: evaluate coverage

In [services.py](./services.py), Stage 5A calls `evaluate_coverage()` using the active playbook.

This checks whether the run output mentioned the concepts that the playbook considers important.

It is a completeness guardrail, not a correctness score.

Important consequence:

- a coverage hit does not prove the interpretation is correct
- a coverage miss means the run probably did not surface that concept clearly enough

## The Important Functions

### `list_playbook_summaries()`

Purpose: create the compact list used by the API/UI.

Use it when you need to expose the available playbooks without sending the whole registry internals.

### `has_playbook()`

Purpose: check whether a key is valid.

This is mainly used before accepting an override.

### `get_playbook()`

Purpose: fetch a playbook or safely fall back to the default.

Use this whenever later stages need the active playbook.

### `choose_playbook()`

Purpose: select one playbook for the run.

This is the policy-selection point. If you add a new playbook and want it to be selected automatically, this function usually needs to be updated.

### `prioritize_pages()`

Purpose: bias the most important page ids for the chosen playbook.

It combines:

- the page's `importance_rank`
- a role bonus for plans, elevations, sections, schedules, and details
- keyword hits against `priority_keywords`

This does not hard-filter pages out. It only boosts the likely anchors.

### `build_stage2_guidance()`

Purpose: turn the playbook into Stage 2 planner text.

This is where `stage2_biases` and `coverage_targets` become prompt content.

### `prompt_category()`

Purpose: map a `prompt_family` string to a broad reading category.

Examples:

- `stage3_plan` -> `plan`
- `stage3_elevation` -> `elevation`
- `stage3_detail` -> `detail`
- anything unknown -> `generic`

This is important because `stage3_notes` are keyed by category, not by every possible prompt family string.

### `build_stage3_instructions()`

Purpose: assemble the final Stage 3 instruction block.

This is the function that actually turns the playbook into task-time behavior.

### `evaluate_coverage()`

Purpose: estimate whether the run covered the concepts expected by the playbook.

It searches a text corpus assembled from:

- Stage 1 pack hypotheses
- Stage 1 unresolved questions
- Stage 1 page atlas summaries
- Stage 3 observations

It does not read raw images or rerun inference.

## How To Read One Existing Playbook

Take `warehouse_portal_frame` in [playbooks.py](./playbooks.py) as an example.

### What it is saying conceptually

The system should read this kind of pack as if the structural backbone is:

- portal frames
- bays and grids
- columns
- rafters
- bracing
- footings and base plates

### How that changes behavior

- `priority_keywords` push portal-frame-like pages up the queue
- `stage2_biases` tell the planner to anchor on slabs, footing plans, framing plans, and portal elevations
- `stage3_notes.plan` tells readers to focus on grids, bay spacing, portal positions, and footing tags
- `stage3_notes.elevation` tells readers to focus on frame geometry and bracing zones
- `coverage_targets` later check whether the run surfaced portal frames, grids, columns, bracing, and foundation support

## Example: What Happens In A Real Run

### Example 1: automatic selection

Suppose Stage 1 says:

- pack type: warehouse structural pack
- project type: portal-frame warehouse
- object families: `portal_frame`, `column`, `beam`, `bracing`

Likely result:

1. `choose_playbook()` selects `warehouse_portal_frame`
2. `prioritize_pages()` pushes framing plans and portal elevations up
3. Stage 2 gets planner guidance biased toward grids, bays, footings, and portal lines
4. Stage 3 gets stronger plan/elevation/detail instructions for that system
5. Stage 5 checks whether portal-frame concepts surfaced clearly enough

### Example 2: user override

Suppose Stage 1 is uncertain, but the user knows it is a tilt-panel pack and sets the override.

Likely result:

1. `choose_playbook()` accepts the override
2. the playbook source becomes `user_override`
3. Stage 2 and Stage 3 follow the tilt-panel priorities even if Stage 1 was ambiguous

This is why playbooks are useful even when Stage 1 is not perfect.

## How To Add A New Playbook

The safest process is:

1. copy the closest existing playbook in [playbooks.py](./playbooks.py)
2. change `key`, `label`, and `description`
3. tune `focus_items`
4. tune `priority_keywords`
5. tune `stage2_biases`
6. tune `stage3_notes`
7. tune `coverage_targets`
8. update `choose_playbook()` if you want automatic selection

### Example skeleton

```python
"concrete_parking_structure": ReadingPlaybook(
    key="concrete_parking_structure",
    label="Concrete Parking Structure",
    description="Concrete parking structure policy focused on ramps, columns, slabs, beams, shear walls, and level coordination.",
    focus_items=(
        "Anchor the pack by ramp layouts, slabs, grids, columns, and vertical circulation first.",
        "Treat level changes and wall/core relationships as primary reading targets.",
    ),
    priority_keywords=(
        "parking",
        "ramp",
        "slab",
        "column",
        "beam",
        "core",
        "shear wall",
    ),
    stage2_biases=(
        "Prioritize ramp plans, slab framing plans, level coordination sheets, sections, and wall schedules.",
        "Treat grids, levels, ramps, column lines, slab edges, and core walls as first-class anchors.",
    ),
    stage3_notes={
        "plan": (
            "Look for ramps, slab edges, expansion joints, core walls, and column grids.",
        ),
        "section": (
            "Use sections to confirm level changes, slab thickness transitions, and ramp geometry.",
        ),
    },
    coverage_targets=(
        CoverageTarget("ramps", "Ramps", "Ramp geometry and level transitions.", ("ramp", "slope", "parking")),
        CoverageTarget("slabs", "Slabs", "Main suspended slab system.", ("slab", "deck")),
        CoverageTarget("columns", "Columns", "Primary support columns.", ("column", "pier")),
    ),
)
```

Then add matching logic to `choose_playbook()` only if automatic selection is needed.

## How To Tune A Playbook Without Breaking The System

### Safe changes

- improve wording in `description`
- add or refine `focus_items`
- add or remove `priority_keywords`
- add category notes inside `stage3_notes`
- broaden `coverage_targets` keywords

### Higher-risk changes

- creating many new prompt categories
- over-specializing `stage3_notes`
- making `priority_keywords` too broad, so every page ranks high
- making `coverage_targets` too strict, so good runs look incomplete

## Practical Rule Of Thumb

If you want the system to read a known family of packs differently, add or tune a playbook.

If you only want stronger emphasis within an existing reading mode like plan/elevation/detail, change `stage3_notes`.

If you want a new playbook to be chosen automatically, update `choose_playbook()`.

If you want Stage 5 to stop flagging an expected concept as missing, review `coverage_targets` and the actual Stage 3 evidence wording.

## References

- Core registry and helper functions: [playbooks.py](./playbooks.py)
- Stage 1 playbook selection and page prioritization: [openai_pipeline.py](./openai_pipeline.py)
- Stage 2 guidance injection: [openai_pipeline.py](./openai_pipeline.py)
- Stage 3 instruction injection: [openai_pipeline.py](./openai_pipeline.py)
- Stage 5 coverage evaluation use: [services.py](./services.py)

## Short Summary

`playbooks.py` is the policy layer that tells the pipeline how to read different pack families.

It does not replace the model.

It biases the model by:

- choosing one reading policy
- ranking pages differently
- changing Stage 2 planner instructions
- changing Stage 3 reader instructions
- checking Stage 5 coverage expectations

If you understand those five effects, you understand the file.