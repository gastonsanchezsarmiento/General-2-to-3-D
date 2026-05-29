"""Human-editable reading policies for Stage 1, Stage 2, and Stage 3.

This file is meant to be the easiest backend place for engineers to tune how
the system reads different drawing packs.

How to work in this file:
- Add or tune playbooks in PLAYBOOKS to change page priorities, Stage 2 planner
    guidance, Stage 3 reading emphasis, and Stage 5 coverage checks.
- Keep prompt categories broad. They describe the kind of reading task
    (plan/elevation/section/detail/schedule), not the object being detected.
- If a new building family needs different priorities, first add a new
    playbook. Only add a new prompt category when the reading behavior is truly
    different from the existing buckets.
- When adding a new playbook, also update choose_playbook() if you want Stage 1
    to select it automatically; otherwise it will only be available by explicit
    user override.

For example, portal-frame logic usually belongs in the warehouse portal-frame
playbook under the existing plan/elevation/detail categories. A dedicated
"portal" prompt category is only useful if those existing categories stop being
specific enough.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable


if TYPE_CHECKING:
    from .models import Observation, PageAtlasEntry, Stage1Reconnaissance


DEFAULT_PLAYBOOK_KEY = "generic_structural_pack"


@dataclass(frozen=True)
class CoverageTarget:
    """A concept the active playbook expects the run to cover.

    These targets are used by evaluate_coverage() as a lightweight completeness
    check. They do not prove correctness; they only help detect whether the run
    seems to have touched the important concepts for the selected playbook.
    """

    key: str
    label: str
    description: str
    keywords: tuple[str, ...]
    required: bool = True


@dataclass(frozen=True)
class ReadingPlaybook:
    """A high-level reading policy for one building or pack family.

    Field guide:
    - focus_items: repeated priorities injected into Stage 3 tasks
    - priority_keywords: words that boost page ranking in prioritize_pages()
    - stage2_biases: plain-English instructions for the Stage 2 planner
    - stage3_notes: extra instructions keyed by prompt category
    - coverage_targets: concepts Stage 5 should expect to see evidence for
    """

    key: str
    label: str
    description: str
    focus_items: tuple[str, ...]
    priority_keywords: tuple[str, ...]
    stage2_biases: tuple[str, ...]
    stage3_notes: dict[str, tuple[str, ...]]
    coverage_targets: tuple[CoverageTarget, ...]

# Generic Stage 3 instructions keyed by prompt category.
#
# These categories are mostly sheet-reading modes, not object families. In
# other words, "plan" means "read this like a plan sheet", not "look for plan
# objects". Prefer extending playbook.stage3_notes before creating a brand-new
# category.
BASE_STAGE3_NOTES: dict[str, tuple[str, ...]] = {
    "title_index": (
        "Confirm exact project name, sheet index, discipline split, revision cues, and any note that tells you which structural sheets matter most.",
        "Identify Australian project context when visible: state or territory, NCC/BCA references, Australian Standards, drawing issue status, revision history, design criteria notes, and structural sheet numbering patterns such as S000, S100, S200, S300, and S400.",
        "Prefer exact sheet identifiers and title block metadata over visual guesses.",
    ),
    "plan": (
        "Treat plans as the main spatial anchor: extract grids, bays, levels, member tags, footing or slab extents, and callout references.",
        "If a plan is ambiguous, state whether it behaves more like a foundation, slab, floor framing, or roof framing plan.",
    ),
    "elevation": (
        "Use elevations to identify vertical systems, repeated framing logic, openings, heights, bracing zones, and references back to plans/details.",
        "Do not invent member sizes or elevations if labels are unreadable; preserve them as unresolved.",
    ),
    "section": (
        "Use sections to understand vertical build-up, footing and slab relationships, wall build-ups, levels, and reinforcement requirements.",
        "Call out section/detail numbers whenever visible so later stages can cross-reference them.",
    ),
    "schedule": (
        "Prefer headers, row labels, member marks, footing tags, panel identifiers, and governing notes over trying to infer whole tables from weak text.",
        "For Australian structural schedules, preserve exact mark syntax, member section notation, concrete strength, reinforcement notation, base plate marks, hold-down bolt marks, footing tags, and references to typical details when present.",
        "If a schedule is only partly legible, capture the structure of the table and the readable keys instead of overfilling values.",
    ),
    "detail": (
        "Read details as supporting evidence for member interfaces, reinforcement, anchors, base plates, joints, and section callouts.",
        "Always state which broader system the detail seems to belong to if it is inferable from tags or geometry.",
    ),
    "stairs": (
        "Only extract stair and guard information that has structural consequences: slab edges, landings, walls, reinforcement, anchors, and support conditions.",
    ),
    "cross_reference": (
        "Use this task to connect plans, elevations, sections, schedules, and details into a coherent system rather than producing isolated facts.",
        "When an object appears in plan but its size or definition is given elsewhere, do not resolve it from vision alone. Link the plan mark to the schedule, detail, section, or elevation where the defining information appears.",
        "Prefer relationships such as plan grid to column line, column to footing, portal to bay, detail to callout, and schedule item to member tag.",
    ),
    "generic": (
        "Capture only what is directly supportable from the supplied pages, and separate unresolved questions from inferred structure.",
    ),
}

# Registry of human-editable reading policies.
#
# To add a new family:
# 1. Copy the closest existing playbook.
# 2. Tune focus_items, priority_keywords, stage2_biases, stage3_notes, and
#    coverage_targets.
# 3. Update choose_playbook() if it should be auto-selected from Stage 1.
PLAYBOOKS: dict[str, ReadingPlaybook] = {
    # Safe fallback when no specialized policy matches, or when the user wants a
    # neutral structural reading strategy.
    DEFAULT_PLAYBOOK_KEY: ReadingPlaybook(
        key=DEFAULT_PLAYBOOK_KEY,
        label="Generic Structural Pack",
        description="Balanced structural reading policy for mixed plan, elevation, section, schedule, and detail packs.",
        focus_items=(
            "Establish the main structural anchor pages before reading isolated details.",
            "Resolve grids, levels, primary members, supports, and governing notes first.",
            "Delay secondary detail interpretation until main plans/elevations/sections are grounded.",
        ),
        priority_keywords=(
            "plan",
            "framing",
            "foundation",
            "footing",
            "slab",
            "grid",
            "level",
            "elevation",
            "section",
            "schedule",
            "connection",
        ),
        stage2_biases=(
            "Prioritize title/index, anchor plans, major elevations, sections, schedules, and then detail sheets.",
            "Treat grids, levels, member tags, support conditions, and major callouts as primary anchors.",
            "Use schedules and notes to confirm nomenclature and governing requirements after the main geometry is understood.",
        ),
        stage3_notes={
            "plan": (
                "Identify the primary structural system, support layout, and main coordinate references before reading detail-heavy pages.",
            ),
            "cross_reference": (
                "Report which critical relationships were confirmed and which still need targeted rereads.",
            ),
        },
        coverage_targets=(
            CoverageTarget("anchor_plans", "Anchor plans", "Primary structural plan anchors.", ("plan", "framing", "foundation", "slab")),
            CoverageTarget("grid_levels", "Grid and levels", "Coordinate system used across the pack.", ("grid", "bay", "level", "rl")),
            CoverageTarget("primary_supports", "Primary supports", "Columns, walls, or other vertical supports.", ("column", "wall", "support", "stanchion")),
            CoverageTarget("primary_members", "Primary members", "Beams, rafters, frames, or main spanning members.", ("beam", "rafter", "frame", "girder", "portal")),
            CoverageTarget("foundations", "Foundations", "Footings, slab edges, or base support systems.", ("footing", "foundation", "slab", "base plate")),
            CoverageTarget("connections_notes", "Connections and notes", "Key connection details and governing notes.", ("connection", "anchor", "bolt", "note", "schedule")),
        ),
    ),
    # Best fit when portal frames are the main structural backbone and the key
    # task is coordinating portals, grids, columns, and foundations.
    "warehouse_portal_frame": ReadingPlaybook(
        key="warehouse_portal_frame",
        label="Warehouse Portal Frame",
        description="Portal-frame warehouse policy focused on bays, column grids, rafters, bracing, slabs, footings, and base connections.",
        focus_items=(
            "Anchor the warehouse by grids, bays, portal frame lines, column positions, and slab or footing plans.",
            "Prioritize portal elevations and framing sheets before isolated details.",
            "Track how columns, rafters, bracing, base plates, and footings relate across plans, elevations, and details.",
        ),
        priority_keywords=(
            "warehouse",
            "portal",
            "frame",
            "framing",
            "rafter",
            "purlin",
            "column",
            "grid",
            "bay",
            "bracing",
            "footing",
            "base plate",
            "slab",
            "elevation",
        ),
        stage2_biases=(
            "Prioritize title/index, main slab or footing plans, primary framing plans, portal frame elevations, and bracing layouts before secondary details.",
            "Treat grids, bay spacing, column lines, portal frame identifiers, footing tags, and base plate details as first-class targets.",
            "De-prioritize stairs, guards, and architectural details unless they materially affect structural support or anchorage.",
        ),
        stage3_notes={
            "plan": (
                "Find grids, bay spacing, portal frame positions, columns, slab edges, bracing lines, footing tags, and level references.",
                "Prefer explicit column-to-grid and footing-to-column relationships over generic plan summaries.",
            ),
            "elevation": (
                "Look for portal frame geometry: columns, rafters, knee regions, eaves, ridge, bracing zones, and openings affecting the frame.",
            ),
            "detail": (
                "Prioritize base plates, anchor bolts, footing interfaces, bracing connections, and frame junction details.",
            ),
            "cross_reference": (
                "Explicitly tie portals to bays, columns to grids, columns to footings, and details to their plan or elevation callouts.",
            ),
        },
        coverage_targets=(
            CoverageTarget("portal_frames", "Portal frames", "Main portal frame system.", ("portal frame", "portal", "frame", "rafter", "haunch")),
            CoverageTarget("grid_bays", "Grid and bays", "Gridlines and bay spacing.", ("grid", "bay", "gridline")),
            CoverageTarget("columns", "Columns", "Column locations and support lines.", ("column", "stanchion")),
            CoverageTarget("footings_baseplates", "Footings and base plates", "Foundation support for columns.", ("footing", "pad footing", "base plate", "anchor bolt", "foundation")),
            CoverageTarget("slab_foundation_plan", "Slab or foundation plan", "Main plan for slabs or footing layout.", ("slab", "foundation plan", "footing plan")),
            CoverageTarget("bracing", "Bracing", "Lateral bracing systems.", ("bracing", "brace", "tie rod")),
            CoverageTarget("connections_schedules", "Connections and schedules", "Connection details and member schedules.", ("connection", "schedule", "member mark", "purlin", "girt")),
        ),
    ),
    # Best fit when wall panels drive the pack and panel layouts/elevations are
    # more important than portal-frame geometry.
    "warehouse_tilt_panel": ReadingPlaybook(
        key="warehouse_tilt_panel",
        label="Warehouse Tilt Panel",
        description="Tilt-panel warehouse policy focused on panel layouts, elevations, braces, connections, slabs, and footing interfaces.",
        focus_items=(
            "Anchor the pack by panel layout, wall elevations, panel IDs, and the slab or footing support system.",
            "Treat panel schedules, panel connection details, braces, and hold-down conditions as critical supporting evidence.",
        ),
        priority_keywords=(
            "warehouse",
            "panel",
            "tilt",
            "precast",
            "wall",
            "brace",
            "connection",
            "slab",
            "footing",
            "elevation",
            "schedule",
        ),
        stage2_biases=(
            "Prioritize panel layouts, wall elevations, panel schedules, slab or footing plans, and connection or brace details before generic notes sheets.",
            "Treat panel IDs, brace points, footing interfaces, lifting or hold-down references, and connection schedules as core targets.",
        ),
        stage3_notes={
            "plan": (
                "Find panel lines, wall runs, slab interfaces, brace anchors, and grid or set-out references.",
            ),
            "elevation": (
                "Identify panel IDs, openings, panel joints, brace locations, and level references in wall elevations.",
            ),
            "schedule": (
                "Capture panel identifiers, schedule keys, panel thickness, inserts, and connection references when readable.",
            ),
            "detail": (
                "Prioritize braces, panel-to-footing or slab connections, joints, anchors, and lifting or temporary stability details.",
            ),
        },
        coverage_targets=(
            CoverageTarget("panel_layout", "Panel layout", "Primary panel set-out or wall layout.", ("panel", "wall layout", "set out")),
            CoverageTarget("panel_elevations", "Panel elevations", "Panel elevation views with identifiers.", ("elevation", "panel id", "wall elevation")),
            CoverageTarget("panel_schedules", "Panel schedules", "Panel schedules or tables.", ("schedule", "panel schedule", "panel mark")),
            CoverageTarget("brace_connections", "Braces and connections", "Bracing and connection system for panels.", ("brace", "connection", "hold down", "anchor")),
            CoverageTarget("slab_footings", "Slab and footings", "Support system for panels.", ("slab", "footing", "foundation")),
        ),
    ),
    # Broad industrial steel fallback for packs that look steel-framed but do
    # not clearly match the warehouse-specialized cases above.
    "steel_frame_industrial": ReadingPlaybook(
        key="steel_frame_industrial",
        label="Steel Frame Industrial",
        description="Steel-framed industrial policy focused on framing plans, grids, member schedules, bracing, base plates, and connection logic.",
        focus_items=(
            "Anchor the pack by framing plans, structural grids, column schedule logic, and primary steel member systems.",
            "Read schedules and connection details as first-class evidence once the framing system is identified.",
        ),
        priority_keywords=(
            "steel",
            "frame",
            "framing",
            "industrial",
            "column",
            "beam",
            "rafter",
            "girt",
            "purlin",
            "bracing",
            "schedule",
            "connection",
            "base plate",
        ),
        stage2_biases=(
            "Prioritize framing plans, grids, member schedules, elevations, and connection sheets before non-structural detail sets.",
            "Treat column lines, member marks, brace systems, base plates, and steel connection notes as the main reading backbone.",
        ),
        stage3_notes={
            "plan": (
                "Look for framing bay logic, member marks, steel grids, brace lines, and support locations.",
            ),
            "schedule": (
                "Capture member marks, section sizes, schedule headers, and references that tie schedules back to plans or elevations.",
            ),
            "detail": (
                "Prioritize steel connections, base plates, anchor bolts, braces, cleats, and splice or end conditions.",
            ),
        },
        coverage_targets=(
            CoverageTarget("grids", "Grids", "Primary structural grid system.", ("grid", "bay", "gridline")),
            CoverageTarget("columns", "Columns", "Column system and support points.", ("column", "stanchion")),
            CoverageTarget("primary_members", "Primary steel members", "Beams, rafters, or main frame members.", ("beam", "rafter", "girder", "frame")),
            CoverageTarget("secondary_members", "Secondary steel members", "Purlins, girts, or secondary framing.", ("purlin", "girt", "secondary member")),
            CoverageTarget("bracing", "Bracing", "Lateral bracing systems.", ("brace", "bracing", "tie rod")),
            CoverageTarget("connections", "Connections", "Connection details and notes.", ("connection", "cleat", "splice", "base plate", "anchor bolt")),
            CoverageTarget("schedules", "Schedules", "Member schedules and marks.", ("schedule", "member mark", "section size")),
        ),
    ),
}


def list_playbook_summaries() -> list[dict[str, str | bool]]:
    """Return the compact playbook list shown in the API/UI."""

    return [
        {
            "key": playbook.key,
            "label": playbook.label,
            "description": playbook.description,
            "default": playbook.key == DEFAULT_PLAYBOOK_KEY,
        }
        for playbook in PLAYBOOKS.values()
    ]


def has_playbook(key: str | None) -> bool:
    """True when the key matches a registered playbook."""

    return bool(key) and key in PLAYBOOKS


def get_playbook(key: str | None) -> ReadingPlaybook:
    """Fetch a playbook, falling back to the generic policy."""

    if key and key in PLAYBOOKS:
        return PLAYBOOKS[key]
    return PLAYBOOKS[DEFAULT_PLAYBOOK_KEY]


def _normalize(parts: Iterable[str | None]) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def choose_playbook(
    *,
    project_type_hypothesis: str,
    candidate_object_families: Iterable[str],
    pack_type_hypothesis: str | None = None,
    discipline_hypothesis: str | None = None,
    override: str | None = None,
) -> tuple[ReadingPlaybook, str, str]:
    """Pick one active playbook for the run.

    Current behavior selects exactly one playbook per run.

    Selection order:
    1. explicit user override
    2. Stage 1 hypothesis matching
    3. generic fallback

    The returned tuple is (playbook, source, rationale) so the UI and later
    stages can explain why the choice happened.
    """

    if has_playbook(override):
        playbook = get_playbook(override)
        return playbook, "user_override", f"User explicitly selected the {playbook.label} playbook."

    haystack = _normalize([project_type_hypothesis, pack_type_hypothesis, discipline_hypothesis, *candidate_object_families])

    if "warehouse" in haystack and any(token in haystack for token in ("tilt", "panel", "precast")):
        playbook = PLAYBOOKS["warehouse_tilt_panel"]
        return playbook, "stage1_inference", "Stage 1 hypotheses indicate a warehouse pack with tilt or panel-driven wall systems."
    if "warehouse" in haystack and any(token in haystack for token in ("portal", "rafter", "purlin", "frame")):
        playbook = PLAYBOOKS["warehouse_portal_frame"]
        return playbook, "stage1_inference", "Stage 1 hypotheses indicate a warehouse pack centered on portal or framing systems."
    if any(token in haystack for token in ("steel", "girt", "purlin", "base plate", "industrial")):
        playbook = PLAYBOOKS["steel_frame_industrial"]
        return playbook, "stage1_inference", "Stage 1 hypotheses indicate a steel-framed industrial structural pack."

    playbook = PLAYBOOKS[DEFAULT_PLAYBOOK_KEY]
    return playbook, "fallback", "No specialized playbook matched the Stage 1 hypotheses, so the generic structural policy was used."


def prioritize_pages(playbook: ReadingPlaybook, page_atlas: Iterable[PageAtlasEntry], limit: int = 8) -> list[str]:
    """Rank the most important pages for the selected playbook.

    This is a biasing function, not a hard filter. Lower-ranked pages can still
    be read later; this just helps Stage 1 and Stage 2 put the likely anchor
    sheets near the front of the queue.
    """

    scored: list[tuple[int, int, str]] = []
    for entry in page_atlas:
        haystack = _normalize([entry.page_role, entry.title_hint, entry.sheet_number_hint, entry.summary, *entry.object_families])
        score = entry.importance_rank
        if entry.page_role == "plan":
            score += 25
        elif entry.page_role == "elevation":
            score += 18
        elif entry.page_role == "section":
            score += 14
        elif entry.page_role == "schedule":
            score += 12
        elif entry.page_role == "detail":
            score += 8
        for keyword in playbook.priority_keywords:
            if keyword in haystack:
                score += 12
        scored.append((score, entry.page_number, entry.page_id))

    ranked = sorted(scored, key=lambda item: (-item[0], item[1], item[2]))
    page_ids: list[str] = []
    for _, _, page_id in ranked:
        if page_id not in page_ids:
            page_ids.append(page_id)
        if len(page_ids) >= limit:
            break
    return page_ids


def build_stage2_guidance(playbook: ReadingPlaybook, prioritized_page_ids: Iterable[str]) -> str:
    """Turn the active playbook into plain-English guidance for Stage 2."""

    page_ids = [page_id for page_id in prioritized_page_ids if page_id]
    lines = [
        f"Active playbook: {playbook.label} ({playbook.key}).",
        playbook.description,
        "Use these playbook priorities when selecting pages and task types:",
        *[f"- {item}" for item in playbook.stage2_biases],
        "Coverage targets to protect:",
        *[f"- {target.label}: {target.description}" for target in playbook.coverage_targets],
    ]
    if page_ids:
        lines.append(f"Playbook-prioritized page ids: {', '.join(page_ids)}.")
    return "\n".join(lines)


def prompt_category(prompt_family: str) -> str:
    """Map a task's prompt_family string to a broad Stage 3 reading mode.

    Important: these labels describe the kind of page/task being read, not the
    element being found. For example, a portal-frame task will usually still be
    read as a plan, elevation, or detail task.

    Add a new category only when the reading behavior truly needs a different
    instruction set. If the existing category is fine and you only need stronger
    portal/warehouse emphasis, edit the playbook.stage3_notes instead.
    """

    lowered = (prompt_family or "").lower()
    if any(token in lowered for token in ("index", "titleblock", "title_block", "sheet_index")):
        return "title_index"
    if "cross_reference" in lowered or "callout" in lowered:
        return "cross_reference"
    if any(token in lowered for token in ("stairs", "stair", "landing", "guard")):
        return "stairs"
    if any(token in lowered for token in ("schedule", "table")):
        return "schedule"
    if any(token in lowered for token in ("section", "vertical_sections")):
        return "section"
    if "elevation" in lowered:
        return "elevation"
    if any(token in lowered for token in ("detail", "connection", "footing", "slab_edge", "rebar")):
        return "detail"
    if any(token in lowered for token in ("plan", "layout", "grid", "foundation", "framing")):
        return "plan"
    return "generic"


def build_stage3_instructions(playbook: ReadingPlaybook, prompt_family: str, task_type: str) -> str:
    """Compose the final Stage 3 instruction block for one task.

    Stage 3 instructions are assembled from:
    1. a stable structural-reading base
    2. the active playbook's global priorities
    3. the prompt category's generic notes
    4. the active playbook's extra notes for that category
    """

    category = prompt_category(prompt_family)
    lines = [
        "You are the Stage 3 targeted reader for structural drawing interpretation.",
        "Use the page image as the primary source, use text excerpt as support, and do not promote uncertain facts.",
        f"Active playbook: {playbook.label} ({playbook.key}).",
        f"Current task type: {task_type}.",
        "Global playbook priorities:",
        *[f"- {item}" for item in playbook.focus_items],
        "Task-specific instructions:",
        *[f"- {item}" for item in BASE_STAGE3_NOTES.get(category, BASE_STAGE3_NOTES["generic"])],
    ]
    for note in playbook.stage3_notes.get(category, ()):
        lines.append(f"- {note}")
    return "\n".join(lines)


def evaluate_coverage(
    playbook: ReadingPlaybook,
    stage1: Stage1Reconnaissance,
    observations: Iterable[Observation],
) -> tuple[list[str], list[str]]:
    """Estimate whether the run covered the active playbook's key concepts.

    This function scans Stage 1 hypotheses, page summaries, unresolved notes,
    and Stage 3 observations for the playbook's coverage keywords.

    Treat the result as a completeness guardrail, not a correctness score:
    - hits mean the concept was mentioned somewhere in the run output
    - misses mean the concept did not surface clearly enough yet

    If a target is consistently missed for a valid pack, either the prompts are
    weak, the reading plan skipped the right pages, or the target keywords need
    to be broadened.
    """

    corpus_parts: list[str] = [
        stage1.pack_type_hypothesis,
        stage1.discipline_hypothesis,
        stage1.project_type_hypothesis,
        *stage1.candidate_object_families,
        *stage1.unresolved_questions,
    ]
    for page in stage1.page_atlas:
        corpus_parts.extend([page.page_role, page.title_hint or "", page.summary, *page.object_families])
    for observation in observations:
        corpus_parts.extend(
            [
                observation.observation_type,
                observation.object_family or "",
                observation.relationship_family or "",
                observation.summary or "",
            ]
        )
    corpus = _normalize(corpus_parts)

    hits: list[str] = []
    misses: list[str] = []
    for target in playbook.coverage_targets:
        if any(keyword in corpus for keyword in target.keywords):
            hits.append(target.label)
        elif target.required:
            misses.append(target.label)
    return hits, misses