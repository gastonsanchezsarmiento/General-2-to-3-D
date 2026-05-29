from __future__ import annotations

import base64
import json
import mimetypes
import time
from pathlib import Path
from typing import Any

from openai import OpenAI

from .config import Settings
from .models import (
    ArtifactRef,
    EvidenceRef,
    Observation,
    PageAtlasEntry,
    PageRecord,
    ReadPlan,
    ReadTask,
    Stage1Reconnaissance,
    Stage3TaskResult,
)
from .playbooks import build_stage2_guidance, build_stage3_instructions, choose_playbook, get_playbook, prioritize_pages
from .storage import make_id, now_iso


ROLE_PRIORITY = {
    "plan": 0,
    "elevation": 1,
    "section": 2,
    "schedule": 3,
    "detail": 4,
    "notes": 5,
    "drawing": 6,
    "title_index": 7,
}


def _closed_object(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


STAGE1_PAGE_SCHEMA = _closed_object(
    {
        "page_id": {"type": "string"},
        "page_role": {"type": "string", "enum": ["plan", "elevation", "section", "schedule", "detail", "notes", "title_index", "drawing"]},
        "role_confidence": {"type": "string", "enum": ["high", "medium", "low", "contested", "unknown"]},
        "importance_rank": {"type": "integer", "minimum": 1, "maximum": 100},
        "title_hint": {"type": "string"},
        "sheet_number_hint": {"type": "string"},
        "object_families": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
        "needs_follow_up": {"type": "boolean"},
        "unresolved_questions": {"type": "array", "items": {"type": "string"}},
    },
    [
        "page_id",
        "page_role",
        "role_confidence",
        "importance_rank",
        "title_hint",
        "sheet_number_hint",
        "object_families",
        "summary",
        "needs_follow_up",
        "unresolved_questions",
    ],
)

STAGE1_SYNTHESIS_SCHEMA = _closed_object(
    {
        "pack_type_hypothesis": {"type": "string"},
        "discipline_hypothesis": {"type": "string"},
        "project_type_hypothesis": {"type": "string"},
        "candidate_object_families": {"type": "array", "items": {"type": "string"}},
        "anchor_page_ids": {"type": "array", "items": {"type": "string"}},
        "schedule_page_ids": {"type": "array", "items": {"type": "string"}},
        "detail_page_ids": {"type": "array", "items": {"type": "string"}},
        "recommended_next_pages": {"type": "array", "items": {"type": "string"}},
        "unresolved_questions": {"type": "array", "items": {"type": "string"}},
    },
    [
        "pack_type_hypothesis",
        "discipline_hypothesis",
        "project_type_hypothesis",
        "candidate_object_families",
        "anchor_page_ids",
        "schedule_page_ids",
        "detail_page_ids",
        "recommended_next_pages",
        "unresolved_questions",
    ],
)

STAGE2_SCHEMA = _closed_object(
    {
        "working_project_hypothesis": {"type": "string"},
        "collection_goals": {"type": "array", "items": {"type": "string"}},
        "tasks": {
            "type": "array",
            "items": _closed_object(
                {
                    "task_type": {"type": "string"},
                    "target_page_ids": {"type": "array", "items": {"type": "string"}},
                    "prompt_family": {"type": "string"},
                    "support_eligible": {"type": "boolean"},
                    "escalation_rule": {"type": "string"},
                    "priority_rank": {"type": "integer", "minimum": 1, "maximum": 100},
                    "reason": {"type": "string"},
                },
                [
                    "task_type",
                    "target_page_ids",
                    "prompt_family",
                    "support_eligible",
                    "escalation_rule",
                    "priority_rank",
                    "reason",
                ],
            ),
        },
        "unresolved_ids": {"type": "array", "items": {"type": "string"}},
    },
    ["working_project_hypothesis", "collection_goals", "tasks", "unresolved_ids"],
)

STAGE3_OBSERVATION_SCHEMA = _closed_object(
    {
        "observation_type": {"type": "string"},
        "object_family": {"type": "string"},
        "relationship_family": {"type": "string"},
        "page_id": {"type": "string"},
        "summary": {"type": "string"},
        "confidence_tier": {"type": "string", "enum": ["high", "medium", "low", "contested", "unknown"]},
        "epistemic_status": {
            "type": "string",
            "enum": ["direct", "derived", "inferred_schematic", "inferred_approximate", "unresolved"],
        },
        "signals": {"type": "array", "items": {"type": "string"}},
        "dimension_candidates": {"type": "array", "items": {"type": "string"}},
        "observed_labels": {"type": "array", "items": {"type": "string"}},
    },
    [
        "observation_type",
        "object_family",
        "relationship_family",
        "page_id",
        "summary",
        "confidence_tier",
        "epistemic_status",
        "signals",
        "dimension_candidates",
        "observed_labels",
    ],
)

STAGE3_SCHEMA = _closed_object(
    {
        "summary": {"type": "string"},
        "direct_observations": {"type": "array", "items": STAGE3_OBSERVATION_SCHEMA},
        "inferred_observations": {"type": "array", "items": STAGE3_OBSERVATION_SCHEMA},
        "unresolved_questions": {"type": "array", "items": {"type": "string"}},
        "support_recommended": {"type": "boolean"},
    },
    ["summary", "direct_observations", "inferred_observations", "unresolved_questions", "support_recommended"],
)


def _clean_string(value: str) -> str | None:
    cleaned = value.strip()
    return cleaned or None


def _parse_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    return json.loads(cleaned)


def _data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _artifact_path(app_root: Path, artifact_path: str | None) -> Path | None:
    if not artifact_path:
        return None
    return app_root / "data" / "artifacts" / artifact_path


def _dump_optional(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, (dict, list, str, int, float, bool)):
        return value
    return str(value)


class OpenAIStageClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when PLAN3D_MODEL_MODE=openai")
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def stage1_reconnaissance(
        self,
        run_id: str,
        pages: list[PageRecord],
        playbook_override: str | None = None,
    ) -> tuple[Stage1Reconnaissance, list[dict[str, Any]]]:
        journals: list[dict[str, Any]] = []
        page_results: list[dict[str, Any]] = []

        for page in pages:
            preview_path = _artifact_path(self.settings.app_root, page.preview_artifact.path if page.preview_artifact else None)
            if preview_path is None or not preview_path.exists():
                continue

            payload, journal = self._call_structured(
                prompt_family="stage1_page_reconnaissance",
                model=self.settings.stage1_model,
                reasoning_effort="medium",
                schema_name="stage1_page_classification",
                schema=STAGE1_PAGE_SCHEMA,
                instructions=(
                    "You are the Stage 1 reconnaissance reader for structural drawing packs. "
                    "The sent drawings are in low resolution. " 
                    "Classify the page broadly, identify likely sheet role and object families, and preserve a bit of uncertainty. "
                    "Use the image as the primary source and the provided metadata only as support."
                ),
                content=[
                    {
                        "type": "input_text",
                        "text": (
                            f"Run ID: {run_id}\n"
                            f"Page ID: {page.page_id}\n"
                            f"Page number: {page.page_number}\n"
                            f"Sheet hint: {page.sheet_number_hint or ''}\n"
                            f"Title hint: {page.title_hint or ''}\n"
                            f"Text excerpt: {str(page.extensions.get('text_excerpt', ''))}\n"
                            "Return a structured page classification for milestone-1 planning."
                        ),
                    },
                    {"type": "input_image", "image_url": _data_url(preview_path), "detail": "high"},
                ],
                metadata={"run_id": run_id, "page_id": page.page_id},
            )
            page_results.append(payload)
            journals.append(journal)

        synthesis_payload, synthesis_journal = self._call_structured(
            prompt_family="stage1_pack_synthesis",
            model=self.settings.stage1_model,
            reasoning_effort="medium",
            schema_name="stage1_pack_synthesis",
            schema=STAGE1_SYNTHESIS_SCHEMA,
            instructions=(
                "You are the Stage 1 whole-pack synthesizer. Use the page classifications to infer the broad pack type, "
                "high-value pages, and unresolved questions. Favor plan-grounded reading order and preserve uncertainty."
            ),
            content=[
                {
                    "type": "input_text",
                    "text": (
                        f"Run ID: {run_id}\n"
                        f"Requested playbook override: {playbook_override or 'automatic'}\n"
                        "Page classifications:\n"
                        f"{json.dumps(page_results, indent=2)}"
                    ),
                }
            ],
            metadata={"run_id": run_id, "pages": len(page_results)},
        )
        journals.append(synthesis_journal)

        atlas = [
            PageAtlasEntry(
                page_id=result.get("page_id") or page.page_id,
                page_number=page.page_number,
                page_role=result["page_role"],
                role_confidence=result["role_confidence"],
                importance_rank=result["importance_rank"],
                title_hint=_clean_string(result.get("title_hint", "")) or page.title_hint,
                sheet_number_hint=_clean_string(result.get("sheet_number_hint", "")) or page.sheet_number_hint,
                object_families=result.get("object_families", []) or ["structural_context"],
                summary=result["summary"],
                preview_artifact=page.preview_artifact,
            )
            for page, result in zip(pages, page_results, strict=False)
        ]
        atlas.sort(key=lambda item: item.importance_rank, reverse=True)

        playbook, playbook_source, playbook_rationale = choose_playbook(
            project_type_hypothesis=synthesis_payload["project_type_hypothesis"],
            candidate_object_families=synthesis_payload.get("candidate_object_families", []),
            pack_type_hypothesis=synthesis_payload["pack_type_hypothesis"],
            discipline_hypothesis=synthesis_payload["discipline_hypothesis"],
            override=playbook_override,
        )
        playbook_focus_page_ids = prioritize_pages(playbook, atlas)
        recommended_next_pages = list(dict.fromkeys([*playbook_focus_page_ids, *synthesis_payload.get("recommended_next_pages", [])]))

        reconnaissance = Stage1Reconnaissance(
            run_id=run_id,
            pack_type_hypothesis=synthesis_payload["pack_type_hypothesis"],
            discipline_hypothesis=synthesis_payload["discipline_hypothesis"],
            project_type_hypothesis=synthesis_payload["project_type_hypothesis"],
            candidate_object_families=synthesis_payload.get("candidate_object_families", []),
            page_atlas=atlas,
            anchor_page_ids=synthesis_payload.get("anchor_page_ids", []),
            schedule_page_ids=synthesis_payload.get("schedule_page_ids", []),
            detail_page_ids=synthesis_payload.get("detail_page_ids", []),
            unresolved_questions=synthesis_payload.get("unresolved_questions", []),
            recommended_next_pages=recommended_next_pages,
            selected_playbook=playbook.key,
            playbook_source=playbook_source,
            playbook_rationale=playbook_rationale,
            playbook_focus=list(playbook.focus_items),
            playbook_focus_page_ids=playbook_focus_page_ids,
        )
        return reconnaissance, journals

    def stage2_read_plan(
        self,
        run_id: str,
        stage1: Stage1Reconnaissance,
        review_feedback: dict[str, Any] | None = None,
    ) -> tuple[ReadPlan, list[dict[str, Any]]]:
        playbook = get_playbook(stage1.selected_playbook)
        feedback_instructions = []
        if review_feedback and review_feedback.get("action_count"):
            feedback_instructions.append(
                "Respect human review feedback from the prior milestone loop. Prioritize requested reread pages, de-prioritize discarded pages or card targets, and create focused tasks when the reviewer is asking for numeric dimension confirmation."
            )
        payload, journal = self._call_structured(
            prompt_family="stage2_read_plan",
            model=self.settings.stage2_model,
            reasoning_effort="medium",
            schema_name="stage2_read_plan",
            schema=STAGE2_SCHEMA,
            instructions="\n".join(
                [
                    "You are the Stage 2 orchestrator planner. Convert Stage 1 reconnaissance into a typed reading plan.",
                    "Choose plan-anchor sheets first, then elevations, sections, schedules, details, and notes.",
                    *feedback_instructions,
                    build_stage2_guidance(playbook, stage1.playbook_focus_page_ids),
                ]
            ),
            content=[
                {
                    "type": "input_text",
                    "text": (
                        f"Run ID: {run_id}\n"
                        f"Project hypothesis: {stage1.project_type_hypothesis}\n"
                        f"Active playbook: {stage1.selected_playbook or playbook.key}\n"
                        f"Playbook source: {stage1.playbook_source or 'unspecified'}\n"
                        f"Playbook rationale: {stage1.playbook_rationale or ''}\n"
                        f"Playbook focus items: {json.dumps(stage1.playbook_focus)}\n"
                        f"Playbook priority page ids: {json.dumps(stage1.playbook_focus_page_ids)}\n"
                        f"Candidate families: {', '.join(stage1.candidate_object_families)}\n"
                        f"Page atlas: {json.dumps([entry.model_dump(mode='json') for entry in stage1.page_atlas], indent=2)}\n"
                        f"Unresolved: {json.dumps(stage1.unresolved_questions)}\n"
                        f"Human review feedback: {json.dumps(review_feedback or {}, indent=2)}"
                    ),
                }
            ],
            metadata={"run_id": run_id, "pages": len(stage1.page_atlas), "feedback_actions": int((review_feedback or {}).get("action_count", 0))},
            max_output_tokens=max(1600, min(6400, 200 * max(1, len(stage1.page_atlas)))),
        )

        tasks = [
            ReadTask(
                task_id=make_id("task"),
                task_type=item["task_type"],
                target_page_ids=item.get("target_page_ids", []),
                prompt_family=item["prompt_family"],
                expected_output_schema_id="core/observation",
                support_eligible=item["support_eligible"],
                escalation_rule=item["escalation_rule"],
                extensions={"priority_rank": item["priority_rank"], "reason": item["reason"]},
            )
            for item in sorted(payload.get("tasks", []), key=lambda entry: entry.get("priority_rank", 100))
        ]

        read_plan = ReadPlan(
            plan_id=make_id("plan"),
            run_id=run_id,
            working_project_hypothesis=payload["working_project_hypothesis"],
            collection_goals=payload.get("collection_goals", []),
            tasks=tasks,
            unresolved_ids=payload.get("unresolved_ids", []),
            playbook_key=playbook.key,
            playbook_guidance=list(playbook.stage2_biases),
            priority_page_ids=stage1.playbook_focus_page_ids,
        )
        return read_plan, [journal]

    def stage3_task(
        self,
        run_id: str,
        task: ReadTask,
        pages: list[PageRecord],
        playbook_key: str | None = None,
    ) -> tuple[Stage3TaskResult, list[Observation], list[dict[str, Any]]]:
        playbook = get_playbook(playbook_key)
        content: list[dict[str, Any]] = [
            {
                "type": "input_text",
                "text": (
                    f"Run ID: {run_id}\n"
                    f"Task ID: {task.task_id}\n"
                    f"Task type: {task.task_type}\n"
                    f"Prompt family: {task.prompt_family}\n"
                    f"Support eligible: {task.support_eligible}\n"
                    f"Escalation rule: {task.escalation_rule or ''}\n"
                    "Read the supplied engineering drawing page(s) and return evidence-linked observations for milestone-1 packaging. "
                    "Keep directly seen facts separate from inferred schematic understanding."
                ),
            }
        ]

        page_map = {page.page_id: page for page in pages}
        for page_id in task.target_page_ids:
            page = page_map[page_id]
            preview_path = _artifact_path(self.settings.app_root, page.preview_artifact.path if page.preview_artifact else None)
            master_path = _artifact_path(self.settings.app_root, page.master_artifact.path if page.master_artifact else None)
            content.append(
                {
                    "type": "input_text",
                    "text": (
                        f"Page ID: {page.page_id}\n"
                        f"Page number: {page.page_number}\n"
                        f"Sheet hint: {page.sheet_number_hint or ''}\n"
                        f"Title hint: {page.title_hint or ''}\n"
                        f"Text excerpt: {str(page.extensions.get('text_excerpt', ''))}\n"
                    ),
                }
            )
            if preview_path and preview_path.exists():
                content.append({"type": "input_image", "image_url": _data_url(preview_path), "detail": "low"})
            if master_path and master_path.exists() and master_path.stat().st_size < 5_000_000:
                content.append({"type": "input_image", "image_url": _data_url(master_path), "detail": "high"})

        payload, journal = self._call_structured(
            prompt_family=task.prompt_family,
            model=self.settings.stage3_model,
            reasoning_effort="high",
            schema_name="stage3_task_result",
            schema=STAGE3_SCHEMA,
            instructions=build_stage3_instructions(playbook, task.prompt_family, task.task_type),
            content=content,
            metadata={"run_id": run_id, "task_id": task.task_id, "pages": len(task.target_page_ids), "playbook": playbook.key},
            max_output_tokens=2200,
        )

        observations: list[Observation] = []
        direct_observations = self._build_observations(run_id, task, page_map, payload.get("direct_observations", []), default_status="direct")
        inferred_observations = self._build_observations(
            run_id,
            task,
            page_map,
            payload.get("inferred_observations", []),
            default_status="inferred_schematic",
        )
        observations.extend(direct_observations)
        observations.extend(inferred_observations)

        task_result = Stage3TaskResult(
            run_id=run_id,
            task_id=task.task_id,
            page_ids=task.target_page_ids,
            prompt_family=task.prompt_family,
            summary=payload["summary"],
            direct_observations=direct_observations,
            inferred_observations=inferred_observations,
            unresolved_questions=payload.get("unresolved_questions", []),
            support_recommended=payload.get("support_recommended", False),
        )
        return task_result, observations, [journal]

    def _build_observations(
        self,
        run_id: str,
        task: ReadTask,
        page_map: dict[str, PageRecord],
        items: list[dict[str, Any]],
        default_status: str,
    ) -> list[Observation]:
        observations: list[Observation] = []
        for item in items:
            page_id = item.get("page_id") or task.target_page_ids[0]
            page = page_map.get(page_id) or page_map[task.target_page_ids[0]]
            artifact = page.master_artifact or page.preview_artifact or ArtifactRef(artifact_id=page.page_id, artifact_type="page")
            evidence = EvidenceRef(
                evidence_id=make_id("evidence"),
                source_type="vision",
                source_artifact=artifact,
                source_file_id=page.source_document_id,
                page_id=page.page_id,
                confidence_tier=item.get("confidence_tier", "medium"),
                note="OpenAI Responses vision read over Stage 0 assets.",
            )
            observations.append(
                Observation(
                    observation_id=make_id("obs"),
                    run_id=run_id,
                    task_id=task.task_id,
                    observation_type=item["observation_type"],
                    object_family=_clean_string(item.get("object_family", "")),
                    relationship_family=_clean_string(item.get("relationship_family", "")),
                    page_id=page.page_id,
                    summary=item["summary"],
                    observed_values={
                        "signals": item.get("signals", []),
                        "dimension_candidates": item.get("dimension_candidates", []),
                        "observed_labels": item.get("observed_labels", []),
                    },
                    supporting_evidence=[evidence],
                    epistemic_status=item.get("epistemic_status", default_status),
                    confidence_tier=item.get("confidence_tier", "medium"),
                )
            )
        return observations

    def _call_structured(
        self,
        *,
        prompt_family: str,
        model: str,
        reasoning_effort: str,
        schema_name: str,
        schema: dict[str, Any],
        instructions: str,
        content: list[dict[str, Any]],
        metadata: dict[str, Any],
        max_output_tokens: int = 1600,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        started = time.perf_counter()
        current_max_output_tokens = max_output_tokens
        attempts = 0
        last_response = None

        while attempts < 3:
            attempts += 1
            response = self.client.responses.create(
                model=model,
                reasoning={"effort": reasoning_effort},
                instructions=instructions,
                input=[{"role": "user", "content": content}],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": schema_name,
                        "schema": schema,
                        "strict": True,
                    },
                    "verbosity": "low",
                },
                max_output_tokens=current_max_output_tokens,
                metadata={key: str(value) for key, value in metadata.items()},
                store=False,
            )
            last_response = response

            incomplete = getattr(response, "incomplete_details", None)
            incomplete_reason = getattr(incomplete, "reason", None)
            if getattr(response, "status", None) == "incomplete" and incomplete_reason == "max_output_tokens":
                next_max_output_tokens = min(current_max_output_tokens * 2, 6400)
                if next_max_output_tokens > current_max_output_tokens:
                    current_max_output_tokens = next_max_output_tokens
                    continue
                raise RuntimeError(
                    "OpenAI structured response hit the max_output_tokens ceiling "
                    f"for {prompt_family} at {current_max_output_tokens} tokens."
                )

            try:
                payload = _parse_json(response.output_text)
                break
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Failed to parse structured OpenAI response for {prompt_family}: {exc}"
                ) from exc
        else:
            incomplete = getattr(last_response, "incomplete_details", None) if last_response is not None else None
            incomplete_reason = getattr(incomplete, "reason", None)
            raise RuntimeError(
                "OpenAI structured response remained incomplete "
                f"for {prompt_family} after {attempts} attempts (reason={incomplete_reason}, max_output_tokens={current_max_output_tokens})."
            )

        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        journal = {
            "journal_id": make_id("journal"),
            "run_id": metadata.get("run_id"),
            "prompt_family": prompt_family,
            "mode": "openai",
            "model": model,
            "response_id": getattr(response, "id", None),
            "created_at": now_iso(),
            "latency_ms": duration_ms,
            "usage": _dump_optional(getattr(response, "usage", None)),
            "metadata": metadata,
            "attempts": attempts,
            "response_status": getattr(response, "status", None),
            "max_output_tokens": current_max_output_tokens,
            "output_preview": response.output_text[:500],
        }
        return payload, journal
