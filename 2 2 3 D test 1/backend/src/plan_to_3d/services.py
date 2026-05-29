from __future__ import annotations

import asyncio
import re
import threading
from collections import Counter, defaultdict
from typing import Any, Iterable

import fitz
from fastapi import HTTPException, UploadFile

from .config import Settings
from .models import (
    ArtifactRef,
    CandidateObject,
    CandidateRelationship,
    ConflictRecord,
    CreateRunRequest,
    EvidenceRef,
    HumanReviewAction,
    Observation,
    PageAtlasEntry,
    PageRecord,
    PageSize,
    ProjectDetail,
    ProjectRecord,
    ReadPlan,
    ReadTask,
    ReviewActionRequest,
    RunManifest,
    RunRecord,
    RunSnapshot,
    SourceDocumentRecord,
    Stage1Reconnaissance,
    Stage3TaskResult,
    Stage4SupportArtifact,
    Stage5APackage,
    Stage5AReadiness,
    Stage5BBoard,
    Stage5BCard,
    UnresolvedRecord,
)
from .openai_pipeline import OpenAIStageClient
from .playbooks import evaluate_coverage, get_playbook, has_playbook
from .storage import ArtifactStore, Database, hash_bytes, make_id, now_iso


STAGE_ORDER = ["stage0", "stage1", "stage2", "stage3", "stage4", "stage5a", "stage5b"]
ROLE_PATTERNS: list[tuple[str, tuple[str, ...], int]] = [
    ("plan", ("plan", "framing", "footing", "slab", "roof plan"), 100),
    ("elevation", ("elevation", "north", "south", "east", "west"), 85),
    ("section", ("section", "cut"), 80),
    ("schedule", ("schedule", "legend", "member list"), 75),
    ("detail", ("detail", "connection", "typical"), 70),
    ("notes", ("notes", "general note", "specification"), 60),
    ("title_index", ("title", "drawing list", "index"), 50),
]
OBJECT_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("portal_frame", ("portal", "frame", "moment frame")),
    ("column", ("column", "stanchion")),
    ("beam", ("beam", "rafter", "girt", "purlin")),
    ("footing", ("footing", "pad footing", "foundation")),
    ("bracing", ("bracing", "brace", "tie rod")),
    ("grid", ("grid", "gridline", "bay")),
    ("level", ("level", "rl", "elevation")),
    ("roof", ("roof", "ridge", "eaves")),
    ("wall", ("wall", "panel", "cladding")),
]


def _first_lines(text: str, limit: int = 4) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()][:limit]


def _guess_sheet_number(text: str, filename: str) -> str | None:
    match = re.search(r"\b([A-Z]{1,3}[0-9]{1,3}(?:\.[0-9]+)?)\b", text or filename)
    return match.group(1) if match else None


def _guess_role(haystack: str) -> tuple[str, int]:
    lowered = haystack.lower()
    for role, keywords, rank in ROLE_PATTERNS:
        if any(keyword in lowered for keyword in keywords):
            return role, rank
    return "drawing", 40


def _extract_families(haystack: str) -> list[str]:
    lowered = haystack.lower()
    families = [family for family, keywords in OBJECT_PATTERNS if any(keyword in lowered for keyword in keywords)]
    return families or ["structural_context"]


def _infer_project_type(texts: Iterable[str]) -> str:
    lowered = " ".join(texts).lower()
    if "portal" in lowered or "warehouse" in lowered or "shed" in lowered:
        return "portal-frame structural pack"
    if "residential" in lowered or "dwelling" in lowered:
        return "residential structural pack"
    return "structural drawing pack"


def _confidence_from_rank(rank: int) -> str:
    if rank >= 90:
        return "high"
    if rank >= 70:
        return "medium"
    return "low"


def _dimension_candidates(text: str) -> list[str]:
    values = re.findall(r"\b\d{2,5}(?:\.\d+)?\s?(?:mm|m|kN|RL)\b", text, flags=re.IGNORECASE)
    seen: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized not in seen:
            seen.append(normalized)
    return seen[:8]


DIMENSION_FOCUS_PATTERN = re.compile(
    r"\b(dimension|dimensions|numeric|number|size|sizes|span|length|height|width|depth|thickness|diameter|mm|rl)\b",
    flags=re.IGNORECASE,
)


def _unique_strings(values: Iterable[str]) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return seen


def _coerce_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


class RunExecutor:
    def __init__(self, settings: Settings, database: Database, artifacts: ArtifactStore) -> None:
        self.settings = settings
        self.database = database
        self.artifacts = artifacts
        self.openai_client = OpenAIStageClient(settings) if settings.model_mode == "openai" else None

    async def execute(self, run_id: str) -> None:
        await asyncio.to_thread(self._execute_sync, run_id)

    def _execute_sync(self, run_id: str) -> None:
        run = self.database.get_run(run_id)
        if run is None:
            return
        project = self.database.get_project(run.project_id)
        if project is None:
            return
        documents = [doc for doc in self.database.list_source_documents(project.project_id) if doc.source_document_id in run.source_document_ids]
        stage_status = {stage: "pending" for stage in STAGE_ORDER}
        routing_log: list[dict[str, Any]] = []
        model_journal: list[dict[str, Any]] = []
        milestone_decisions: list[dict[str, Any]] = []
        feedback_context = self._load_feedback_context(project, run)

        try:
            reused_baseline = self._try_reuse_relaunch_baseline(project, run)
            if reused_baseline is None:
                self.database.update_run(run.run_id, status="running", current_stage="stage0", current_stage_status="running")
                pages, run_manifest = self._stage0(project, run, documents, stage_status)
                stage_status["stage0"] = "completed"
                self._emit(run.run_id, "stage0", "completed", "Prepared source manifests and page renders.", {"pages": len(pages)})
                routing_log.append({"stage": "stage0", "status": "completed", "created_at": now_iso()})
                self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

                self.database.update_run(run.run_id, current_stage="stage1", current_stage_status="running")
                stage1, stage1_journal = self._stage1(project, run, pages)
                stage_status["stage1"] = "completed"
                model_journal.extend(stage1_journal)
                self._emit(run.run_id, "stage1", "completed", "Generated whole-pack reconnaissance.", {"anchors": len(stage1.anchor_page_ids)})
                routing_log.append({"stage": "stage1", "status": "completed", "created_at": now_iso()})
                self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)
            else:
                pages, stage1 = reused_baseline
                self.database.update_run(run.run_id, status="running", current_stage="stage0", current_stage_status="reused")
                stage_status["stage0"] = "reused"
                self._emit(
                    run.run_id,
                    "stage0",
                    "reused",
                    "Reused Stage 0 page manifests from the prior review loop.",
                    {"pages": len(pages), "source_run_id": run.feedback_source_run_id},
                )
                routing_log.append({"stage": "stage0", "status": "reused", "created_at": now_iso()})
                self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

                self.database.update_run(run.run_id, current_stage="stage1", current_stage_status="reused")
                stage_status["stage1"] = "reused"
                self._emit(
                    run.run_id,
                    "stage1",
                    "reused",
                    "Reused Stage 1 reconnaissance from the prior review loop.",
                    {"anchors": len(stage1.anchor_page_ids), "source_run_id": run.feedback_source_run_id},
                )
                routing_log.append({"stage": "stage1", "status": "reused", "created_at": now_iso()})
                self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

            self.database.update_run(run.run_id, current_stage="stage2", current_stage_status="running")
            read_plan, stage2_journal = self._stage2(project, run, stage1, feedback_context)
            stage_status["stage2"] = "completed"
            model_journal.extend(stage2_journal)
            self._emit(run.run_id, "stage2", "completed", "Built typed read plan.", {"tasks": len(read_plan.tasks)})
            routing_log.append({"stage": "stage2", "status": "completed", "created_at": now_iso()})
            self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

            self.database.update_run(run.run_id, current_stage="stage3", current_stage_status="running")
            task_results, all_observations, stage3_journal = self._stage3(project, run, pages, read_plan)
            stage_status["stage3"] = "completed"
            model_journal.extend(stage3_journal)
            self._emit(run.run_id, "stage3", "completed", "Produced targeted reading artifacts.", {"observations": len(all_observations)})
            routing_log.append({"stage": "stage3", "status": "completed", "created_at": now_iso()})
            self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

            self.database.update_run(run.run_id, current_stage="stage4", current_stage_status="running")
            support_results = self._stage4(project, run, pages, read_plan, task_results, feedback_context)
            stage_status["stage4"] = "completed" if support_results else "skipped"
            self._emit(
                run.run_id,
                "stage4",
                "completed" if support_results else "skipped",
                "Generated optional support extraction artifacts." if support_results else "No support extraction required.",
                {"artifacts": len(support_results)},
            )
            routing_log.append({"stage": "stage4", "status": stage_status["stage4"], "created_at": now_iso()})
            self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

            self.database.update_run(run.run_id, current_stage="stage5a", current_stage_status="running")
            package = self._stage5a(project, run, pages, stage1, read_plan, task_results, support_results, all_observations)
            stage_status["stage5a"] = "completed"
            model_journal.append(self._mock_model_call("stage5a_packaging", run.run_id, {"candidate_objects": len(package.candidate_objects)}))
            self._emit(run.run_id, "stage5a", "completed", "Published coherent observation package.", {"candidate_objects": len(package.candidate_objects)})
            routing_log.append({"stage": "stage5a", "status": "completed", "created_at": now_iso()})
            self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)

            self.database.update_run(run.run_id, current_stage="stage5b", current_stage_status="running")
            board = self._stage5b(project, run, pages, package)
            stage_status["stage5b"] = "completed"
            self._emit(run.run_id, "stage5b", "completed", "Built milestone review board.", {"cards": len(board.cards)})
            routing_log.append({"stage": "stage5b", "status": "completed", "created_at": now_iso()})
            self.database.update_run(
                run.run_id,
                status="awaiting_review",
                current_stage="stage5b",
                current_stage_status="completed",
            )
            self._write_orchestrator_artifacts(project.project_id, run.run_id, stage_status, routing_log, model_journal, milestone_decisions)
        except Exception as exc:
            self.database.update_run(run.run_id, status="failed", current_stage_status="failed")
            self._emit(run.run_id, "orchestrator", "failed", str(exc), {})
            raise

    def _stage1(self, project: ProjectRecord, run: RunRecord, pages: list[PageRecord]) -> tuple[Stage1Reconnaissance, list[dict[str, Any]]]:
        if self.openai_client is None:
            return self._stage1_heuristic(project, run, pages), [self._mock_model_call("stage1_reconnaissance", run.run_id, {"pages": len(pages)})]

        reconnaissance, journals = self.openai_client.stage1_reconnaissance(run.run_id, pages, run.playbook_override)
        self.database.update_run(run.run_id, selected_playbook=reconnaissance.selected_playbook)
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage1",
            "reconnaissance",
            reconnaissance.model_dump(mode="json"),
            schema_id="stage1/reconnaissance",
        )
        return reconnaissance, journals

    def _stage2(
        self,
        project: ProjectRecord,
        run: RunRecord,
        stage1: Stage1Reconnaissance,
        feedback_context: dict[str, Any] | None = None,
    ) -> tuple[ReadPlan, list[dict[str, Any]]]:
        if self.openai_client is None:
            return self._stage2_heuristic(project, run, stage1, feedback_context), [self._mock_model_call("stage2_read_plan", run.run_id, {"tasks": len(stage1.page_atlas)})]

        read_plan, journals = self.openai_client.stage2_read_plan(run.run_id, stage1, feedback_context)
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage2",
            "read-plan",
            read_plan.model_dump(mode="json"),
            schema_id="stage2/read-plan",
        )
        if feedback_context:
            self.artifacts.write_json_artifact(project.project_id, run.run_id, "stage2", "review-feedback", feedback_context)
        return read_plan, journals

    def _stage3(
        self,
        project: ProjectRecord,
        run: RunRecord,
        pages: list[PageRecord],
        read_plan: ReadPlan,
    ) -> tuple[list[Stage3TaskResult], list[Observation], list[dict[str, Any]]]:
        if self.openai_client is None:
            task_results, observations = self._stage3_heuristic(project, run, pages, read_plan)
            return task_results, observations, [
                self._mock_model_call(
                    "stage3_targeted_reading",
                    run.run_id,
                    {"tasks": len(read_plan.tasks), "observations": len(observations)},
                )
            ]

        page_map = {page.page_id: page for page in pages}
        task_results: list[Stage3TaskResult] = []
        all_observations: list[Observation] = []
        journals: list[dict[str, Any]] = []
        total_tasks = len(read_plan.tasks)

        for index, task in enumerate(read_plan.tasks, start=1):
            task_pages = [page_map[page_id] for page_id in task.target_page_ids if page_id in page_map]
            missing_page_ids = [page_id for page_id in task.target_page_ids if page_id not in page_map]
            if missing_page_ids:
                raise ValueError(f"Stage 3 task {task.task_id} references missing pages: {', '.join(missing_page_ids)}")

            self._emit(
                run.run_id,
                "stage3",
                "running",
                f"Reading task {index}/{total_tasks}: {task.task_type}.",
                {
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "completed_tasks": index - 1,
                    "total_tasks": total_tasks,
                    "page_ids": task.target_page_ids,
                },
            )

            task_result, observations, task_journals = self.openai_client.stage3_task(
                run.run_id,
                task,
                task_pages,
                read_plan.playbook_key,
            )
            task_results.append(task_result)
            all_observations.extend(observations)
            journals.extend(task_journals)

            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage3",
                f"task-result-{task.task_id}",
                task_result.model_dump(mode="json"),
                schema_id="stage3/task-result",
            )
            for observation in observations:
                self.artifacts.write_json_artifact(
                    project.project_id,
                    run.run_id,
                    "stage3",
                    f"observation-{observation.observation_id}",
                    observation.model_dump(mode="json"),
                    schema_id="core/observation",
                )

            self._emit(
                run.run_id,
                "stage3",
                "running",
                f"Completed task {index}/{total_tasks}: {task.task_type}.",
                {
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "completed_tasks": index,
                    "total_tasks": total_tasks,
                    "page_ids": task.target_page_ids,
                },
            )

        return task_results, all_observations, journals

    def _feedback_page_ids(self, action: HumanReviewAction, cards_by_id: dict[str, dict[str, Any]]) -> list[str]:
        page_ids: list[str] = []
        for key in ("selected_page_id", "page_id", "card_page_id"):
            page_id = _coerce_text(action.extensions.get(key))
            if page_id and page_id.startswith("page_"):
                page_ids.append(page_id)
        for target_id in action.target_ids:
            if target_id.startswith("page_"):
                page_ids.append(target_id)
            linked_card = cards_by_id.get(target_id)
            linked_page_id = linked_card.get("page_id") if linked_card else None
            if isinstance(linked_page_id, str) and linked_page_id.startswith("page_"):
                page_ids.append(linked_page_id)
        return _unique_strings(page_ids)

    def _load_feedback_context(self, project: ProjectRecord, run: RunRecord) -> dict[str, Any] | None:
        if not run.feedback_source_run_id:
            return None
        source_run = self.database.get_run(run.feedback_source_run_id)
        if source_run is None or source_run.project_id != project.project_id:
            return None

        actions = self.database.list_review_actions(source_run.run_id)
        board_payload = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{source_run.run_id}/stage5b/json/board.json") or {}
        cards_by_id = {
            card.get("card_id"): card
            for card in board_payload.get("cards", [])
            if isinstance(card, dict) and isinstance(card.get("card_id"), str)
        }

        reread_page_ids: list[str] = []
        discarded_page_ids: list[str] = []
        discarded_card_ids: list[str] = []
        notes: list[str] = []

        for action in actions:
            page_ids = self._feedback_page_ids(action, cards_by_id)
            if action.action_type == "request_reread":
                reread_page_ids.extend(page_ids)
            elif action.action_type == "discard_sheet":
                discarded_page_ids.extend(page_ids)
            elif action.action_type == "discard_card":
                discarded_page_ids.extend(page_ids)
                selected_card_id = _coerce_text(action.extensions.get("selected_card_id"))
                if selected_card_id:
                    discarded_card_ids.append(selected_card_id)
                discarded_card_ids.extend([target_id for target_id in action.target_ids if target_id.startswith("card_")])

            if action.note:
                notes.append(f"{action.action_type}: {action.note.strip()}")

        return {
            "source_run_id": source_run.run_id,
            "action_count": len(actions),
            "requested_reread_page_ids": _unique_strings(reread_page_ids),
            "discarded_page_ids": _unique_strings(discarded_page_ids),
            "discarded_card_ids": _unique_strings(discarded_card_ids),
            "notes": notes[:12],
            "requires_numeric_dimensions": any(DIMENSION_FOCUS_PATTERN.search(note) for note in notes),
        }

    def _try_reuse_relaunch_baseline(
        self,
        project: ProjectRecord,
        run: RunRecord,
    ) -> tuple[list[PageRecord], Stage1Reconnaissance] | None:
        if run.relaunch_scope != "stage2_to_stage5" or not run.feedback_source_run_id:
            return None

        source_run = self.database.get_run(run.feedback_source_run_id)
        if source_run is None or source_run.project_id != project.project_id:
            return None
        if source_run.source_document_ids != run.source_document_ids:
            return None

        page_index = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{source_run.run_id}/stage0/json/page-index.json")
        stage1_payload = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{source_run.run_id}/stage1/json/reconnaissance.json")
        run_manifest_payload = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{source_run.run_id}/stage0/json/run-manifest.json")
        if not page_index or not stage1_payload:
            return None

        pages = [PageRecord.model_validate(payload) for payload in page_index.get("pages", [])]
        stage1 = Stage1Reconnaissance.model_validate(stage1_payload)
        self.database.update_run(run.run_id, selected_playbook=stage1.selected_playbook)

        if run_manifest_payload:
            manifest_payload = dict(run_manifest_payload)
            manifest_payload["run_id"] = run.run_id
            manifest_payload["project_id"] = project.project_id
            manifest_payload["created_at"] = run.created_at
            manifest_payload["source_document_ids"] = run.source_document_ids
            manifest_payload["artifact_roots"] = {"run": f"projects/{project.project_id}/runs/{run.run_id}"}
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage0",
                "run-manifest",
                manifest_payload,
                schema_id="stage0/run-manifest",
            )

        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "page-index",
            {
                "schema_id": "stage0/page-index",
                "run_id": run.run_id,
                "pages": [page.model_dump(mode="json") for page in pages],
            },
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage1",
            "reconnaissance",
            stage1.model_dump(mode="json"),
            schema_id="stage1/reconnaissance",
        )
        return pages, stage1

    def _stage0(
        self,
        project: ProjectRecord,
        run: RunRecord,
        documents: list[SourceDocumentRecord],
        stage_status: dict[str, str],
    ) -> tuple[list[PageRecord], RunManifest]:
        page_records: list[PageRecord] = []
        image_index: list[dict[str, Any]] = []

        config_snapshot = self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "config-snapshot",
            {
                "schema_id": "stage0/config-snapshot",
                "run_id": run.run_id,
                "project_id": project.project_id,
                "model_mode": self.settings.model_mode,
                "openai_configured": self.settings.openai_configured,
            },
        )

        for document in documents:
            pdf_path = self.artifacts.absolute_path(document.stored_path)
            source = fitz.open(pdf_path)
            self.database.update_source_document_page_count(document.source_document_id, source.page_count)
            for page_index in range(source.page_count):
                page = source.load_page(page_index)
                page_id = make_id("page")
                preview_path, preview_rel = self.artifacts.make_run_file(project.project_id, run.run_id, "stage0", "previews", f"{page_id}.png")
                master_path, master_rel = self.artifacts.make_run_file(project.project_id, run.run_id, "stage0", "masters", f"{page_id}.png")

                preview_pixmap = page.get_pixmap(matrix=fitz.Matrix(200 / 72, 200 / 72), alpha=False)
                preview_pixmap.save(preview_path)
                master_pixmap = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), alpha=False)
                master_pixmap.save(master_path)

                text = page.get_text("text")
                title_hint = _first_lines(text, 1)[0] if _first_lines(text, 1) else None
                page_record = PageRecord(
                    page_id=page_id,
                    source_document_id=document.source_document_id,
                    page_number=page_index + 1,
                    preview_artifact=ArtifactRef(
                        artifact_id=f"{page_id}_preview",
                        artifact_type="preview_image",
                        run_id=run.run_id,
                        path=preview_rel,
                    ),
                    master_artifact=ArtifactRef(
                        artifact_id=f"{page_id}_master",
                        artifact_type="master_image",
                        run_id=run.run_id,
                        path=master_rel,
                    ),
                    page_size=PageSize(width=float(page.rect.width), height=float(page.rect.height)),
                    rotation_degrees=float(page.rotation),
                    sheet_number_hint=_guess_sheet_number(text, document.original_filename),
                    title_hint=title_hint,
                    text_layer_available=bool(text.strip()),
                    vector_content_available=bool(page.get_drawings()),
                    likely_scanned=not bool(text.strip()),
                    extensions={
                        "text_excerpt": " ".join(_first_lines(text, 6)),
                        "original_filename": document.original_filename,
                    },
                )
                page_records.append(page_record)
                image_index.append(
                    {
                        "page_id": page_id,
                        "preview_path": preview_rel,
                        "master_path": master_rel,
                        "preview_dimensions": {"width": preview_pixmap.width, "height": preview_pixmap.height},
                        "master_dimensions": {"width": master_pixmap.width, "height": master_pixmap.height},
                    }
                )
                self.artifacts.write_json_artifact(
                    project.project_id,
                    run.run_id,
                    "stage0",
                    f"page-record-{page_id}",
                    page_record.model_dump(mode="json"),
                    schema_id="stage0/page-record",
                )

        run_manifest = RunManifest(
            run_id=run.run_id,
            project_id=project.project_id,
            created_at=run.created_at,
            source_document_ids=[doc.source_document_id for doc in documents],
            stage_status=stage_status,
            artifact_roots={"run": f"projects/{project.project_id}/runs/{run.run_id}"},
            config_snapshot=config_snapshot,
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "run-manifest",
            run_manifest.model_dump(mode="json"),
            schema_id="stage0/run-manifest",
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "page-index",
            {
                "schema_id": "stage0/page-index",
                "run_id": run.run_id,
                "pages": [page.model_dump(mode="json") for page in page_records],
            },
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "source-documents",
            {
                "schema_id": "stage0/source-documents",
                "run_id": run.run_id,
                "documents": [document.model_dump(mode="json") for document in documents],
            },
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage0",
            "image-assets",
            {
                "schema_id": "stage0/image-assets",
                "run_id": run.run_id,
                "images": image_index,
            },
        )
        return page_records, run_manifest

    def _stage1_heuristic(self, project: ProjectRecord, run: RunRecord, pages: list[PageRecord]) -> Stage1Reconnaissance:
        atlas: list[PageAtlasEntry] = []
        text_samples: list[str] = []
        family_counter: Counter[str] = Counter()
        anchor_page_ids: list[str] = []
        schedule_page_ids: list[str] = []
        detail_page_ids: list[str] = []
        unresolved: list[str] = []

        for page in pages:
            excerpt = str(page.extensions.get("text_excerpt", ""))
            haystack = " ".join([str(page.title_hint or ""), str(page.sheet_number_hint or ""), excerpt])
            role, rank = _guess_role(haystack)
            families = _extract_families(haystack)
            family_counter.update(families)
            text_samples.append(haystack)
            atlas.append(
                PageAtlasEntry(
                    page_id=page.page_id,
                    page_number=page.page_number,
                    page_role=role,
                    role_confidence=_confidence_from_rank(rank),
                    importance_rank=rank,
                    title_hint=page.title_hint,
                    sheet_number_hint=page.sheet_number_hint,
                    object_families=families,
                    summary=f"Likely {role} sheet with evidence for {', '.join(families)}.",
                    preview_artifact=page.preview_artifact,
                )
            )
            if role == "plan":
                anchor_page_ids.append(page.page_id)
            if role == "schedule":
                schedule_page_ids.append(page.page_id)
            if role == "detail":
                detail_page_ids.append(page.page_id)
            if not page.title_hint and role in {"plan", "elevation", "section"}:
                unresolved.append(f"Page {page.page_number} needs clearer title block confirmation.")

        reconnaissance = Stage1Reconnaissance(
            run_id=run.run_id,
            pack_type_hypothesis="structural drawing pack",
            discipline_hypothesis="structural",
            project_type_hypothesis=_infer_project_type(text_samples),
            candidate_object_families=[family for family, _ in family_counter.most_common()],
            page_atlas=sorted(atlas, key=lambda entry: entry.importance_rank, reverse=True),
            anchor_page_ids=anchor_page_ids,
            schedule_page_ids=schedule_page_ids,
            detail_page_ids=detail_page_ids,
            unresolved_questions=unresolved or ["Confirm sheet role assignments during targeted reading."],
            recommended_next_pages=[entry.page_id for entry in sorted(atlas, key=lambda item: item.importance_rank, reverse=True)[:6]],
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage1",
            "reconnaissance",
            reconnaissance.model_dump(mode="json"),
            schema_id="stage1/reconnaissance",
        )
        return reconnaissance

    def _stage2_heuristic(
        self,
        project: ProjectRecord,
        run: RunRecord,
        stage1: Stage1Reconnaissance,
        feedback_context: dict[str, Any] | None = None,
    ) -> ReadPlan:
        role_priority = {"plan": 0, "elevation": 1, "section": 2, "schedule": 3, "detail": 4, "notes": 5, "drawing": 6, "title_index": 7}
        requested_reread_page_ids = set((feedback_context or {}).get("requested_reread_page_ids", []))
        discarded_page_ids = set((feedback_context or {}).get("discarded_page_ids", []))
        requires_numeric_dimensions = bool((feedback_context or {}).get("requires_numeric_dimensions"))
        page_atlas = [entry for entry in stage1.page_atlas if entry.page_id not in discarded_page_ids] or list(stage1.page_atlas)
        tasks: list[ReadTask] = []
        for entry in sorted(
            page_atlas,
            key=lambda item: (
                0 if item.page_id in requested_reread_page_ids else 1,
                role_priority.get(item.page_role, 9),
                -item.importance_rank,
            ),
        ):
            force_support = requires_numeric_dimensions and entry.page_id in requested_reread_page_ids
            tasks.append(
                ReadTask(
                    task_id=make_id("task"),
                    task_type=f"read_{entry.page_role}",
                    target_page_ids=[entry.page_id],
                    prompt_family=f"stage3_{entry.page_role}",
                    expected_output_schema_id="core/observation",
                    support_eligible=entry.page_role in {"schedule", "detail", "notes"} or force_support,
                    escalation_rule="Escalate to Stage 4 when text clarity or repeated marks remain unresolved.",
                    extensions={
                        "importance_rank": entry.importance_rank,
                        "summary": entry.summary,
                        "feedback_requested": entry.page_id in requested_reread_page_ids,
                    },
                )
            )
        read_plan = ReadPlan(
            plan_id=make_id("plan"),
            run_id=run.run_id,
            working_project_hypothesis=stage1.project_type_hypothesis,
            collection_goals=[
                "Establish plan-grounded spatial anchors.",
                "Capture primary structural object families.",
                "Preserve unresolved and conflict-heavy areas for review.",
                *(["Apply human review feedback from the prior milestone loop."] if feedback_context else []),
            ],
            tasks=tasks,
            priority_page_ids=list(requested_reread_page_ids) or list(stage1.playbook_focus_page_ids),
            extensions={"review_feedback": feedback_context or {}},
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage2",
            "read-plan",
            read_plan.model_dump(mode="json"),
            schema_id="stage2/read-plan",
        )
        if feedback_context:
            self.artifacts.write_json_artifact(project.project_id, run.run_id, "stage2", "review-feedback", feedback_context)
        return read_plan

    def _stage3_heuristic(
        self,
        project: ProjectRecord,
        run: RunRecord,
        pages: list[PageRecord],
        read_plan: ReadPlan,
    ) -> tuple[list[Stage3TaskResult], list[Observation]]:
        page_map = {page.page_id: page for page in pages}
        task_results: list[Stage3TaskResult] = []
        all_observations: list[Observation] = []

        for task in read_plan.tasks:
            direct: list[Observation] = []
            inferred: list[Observation] = []
            unresolved: list[str] = []
            for page_id in task.target_page_ids:
                page = page_map[page_id]
                excerpt = str(page.extensions.get("text_excerpt", ""))
                families = _extract_families(" ".join([task.task_type, excerpt]))
                evidence = EvidenceRef(
                    evidence_id=make_id("evidence"),
                    source_type="vision",
                    source_artifact=page.preview_artifact or ArtifactRef(artifact_id=page.page_id, artifact_type="page"),
                    source_file_id=page.source_document_id,
                    page_id=page.page_id,
                    confidence_tier="medium",
                    note="Derived from Stage 0 preview and page text excerpt.",
                )
                direct.append(
                    Observation(
                        observation_id=make_id("obs"),
                        run_id=run.run_id,
                        task_id=task.task_id,
                        observation_type=task.task_type,
                        object_family=families[0],
                        page_id=page.page_id,
                        summary=f"Observed signals for {families[0]} on page {page.page_number}.",
                        observed_values={
                            "sheet_number": page.sheet_number_hint,
                            "title_hint": page.title_hint,
                            "keywords": families,
                        },
                        supporting_evidence=[evidence],
                        epistemic_status="direct",
                        confidence_tier="medium",
                    )
                )
                for family in families[1:]:
                    inferred.append(
                        Observation(
                            observation_id=make_id("obs"),
                            run_id=run.run_id,
                            task_id=task.task_id,
                            observation_type=f"inferred_{family}",
                            object_family=family,
                            page_id=page.page_id,
                            summary=f"Secondary evidence suggests {family} relevance on page {page.page_number}.",
                            observed_values={"keywords": families},
                            supporting_evidence=[evidence],
                            epistemic_status="inferred_schematic",
                            confidence_tier="low",
                        )
                    )
                if not excerpt:
                    unresolved.append(f"Page {page.page_number} has limited text evidence and may need manual crop review.")

            task_result = Stage3TaskResult(
                run_id=run.run_id,
                task_id=task.task_id,
                page_ids=task.target_page_ids,
                prompt_family=task.prompt_family,
                summary=f"Completed {task.task_type} for {len(task.target_page_ids)} page(s).",
                direct_observations=direct,
                inferred_observations=inferred,
                unresolved_questions=unresolved,
                support_recommended=task.support_eligible and bool(unresolved),
            )
            task_results.append(task_result)
            all_observations.extend(direct)
            all_observations.extend(inferred)
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage3",
                f"task-result-{task.task_id}",
                task_result.model_dump(mode="json"),
                schema_id="stage3/task-result",
            )
            for observation in direct + inferred:
                self.artifacts.write_json_artifact(
                    project.project_id,
                    run.run_id,
                    "stage3",
                    f"observation-{observation.observation_id}",
                    observation.model_dump(mode="json"),
                    schema_id="core/observation",
                )
        return task_results, all_observations

    def _stage4(
        self,
        project: ProjectRecord,
        run: RunRecord,
        pages: list[PageRecord],
        read_plan: ReadPlan,
        task_results: list[Stage3TaskResult],
        feedback_context: dict[str, Any] | None = None,
    ) -> list[Stage4SupportArtifact]:
        page_map = {page.page_id: page for page in pages}
        results: list[Stage4SupportArtifact] = []
        by_task = {result.task_id: result for result in task_results}
        requested_reread_page_ids = set((feedback_context or {}).get("requested_reread_page_ids", []))
        discarded_page_ids = set((feedback_context or {}).get("discarded_page_ids", []))
        requires_numeric_dimensions = bool((feedback_context or {}).get("requires_numeric_dimensions"))
        feedback_notes = [note for note in (feedback_context or {}).get("notes", []) if isinstance(note, str)]
        for task in read_plan.tasks:
            result = by_task[task.task_id]
            if any(page_id in discarded_page_ids for page_id in task.target_page_ids):
                continue
            force_support = bool(requested_reread_page_ids.intersection(task.target_page_ids))
            if not task.support_eligible and not result.support_recommended and not force_support:
                continue
            snippets: list[str] = []
            dimensions: list[str] = []
            warnings: list[str] = []
            for page_id in task.target_page_ids:
                page = page_map[page_id]
                excerpt = str(page.extensions.get("text_excerpt", ""))
                if excerpt:
                    snippets.append(excerpt)
                    dimensions.extend(_dimension_candidates(excerpt))
                else:
                    warnings.append(f"No text layer available for page {page.page_number}.")
            if force_support and feedback_notes:
                warnings.append(feedback_notes[0])
            if not snippets and not dimensions and not force_support:
                continue
            artifact = Stage4SupportArtifact(
                run_id=run.run_id,
                task_id=task.task_id,
                extraction_objective="targeted-numeric-dimension-support" if force_support and requires_numeric_dimensions else "text-and-dimension-support",
                page_ids=task.target_page_ids,
                snippets=snippets[:4],
                dimension_candidates=dimensions[:8],
                warnings=warnings,
            )
            results.append(artifact)
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage4",
                f"support-{task.task_id}",
                artifact.model_dump(mode="json"),
                schema_id="stage4/support-artifact",
            )
        return results

    def _stage5a(
        self,
        project: ProjectRecord,
        run: RunRecord,
        pages: list[PageRecord],
        stage1: Stage1Reconnaissance,
        read_plan: ReadPlan,
        task_results: list[Stage3TaskResult],
        support_results: list[Stage4SupportArtifact],
        observations: list[Observation],
    ) -> Stage5APackage:
        playbook = get_playbook(read_plan.playbook_key or stage1.selected_playbook)
        coverage_hits, coverage_misses = evaluate_coverage(playbook, stage1, observations)
        grouped: dict[str, list[Observation]] = defaultdict(list)
        for observation in observations:
            grouped[observation.object_family or "structural_context"].append(observation)

        candidate_objects: list[CandidateObject] = []
        observation_to_candidate: dict[str, str] = {}
        for family, family_observations in grouped.items():
            candidate_id = make_id("candidate")
            confidence = "medium" if len(family_observations) > 1 else "low"
            candidate = CandidateObject(
                candidate_object_id=candidate_id,
                run_id=run.run_id,
                object_family=family,
                display_label=family.replace("_", " ").title(),
                supporting_observation_ids=[item.observation_id for item in family_observations],
                supporting_evidence=[evidence for item in family_observations for evidence in item.supporting_evidence][:6],
                confidence_tier=confidence,
                spatial_hints={"page_ids": list({item.page_id for item in family_observations if item.page_id})},
            )
            candidate_objects.append(candidate)
            for item in family_observations:
                observation_to_candidate[item.observation_id] = candidate_id
                item.linked_candidate_ids.append(candidate_id)
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage5a",
                f"candidate-object-{candidate.candidate_object_id}",
                candidate.model_dump(mode="json"),
                schema_id="core/candidate-object",
            )

        relationship_rules = [
            ("column", "footing", "supported_by"),
            ("beam", "column", "connected_to"),
            ("roof", "portal_frame", "supported_by"),
        ]
        family_to_candidate = {candidate.object_family: candidate for candidate in candidate_objects}
        relationships: list[CandidateRelationship] = []
        for source_family, target_family, relationship_family in relationship_rules:
            source = family_to_candidate.get(source_family)
            target = family_to_candidate.get(target_family)
            if not source or not target:
                continue
            relationship = CandidateRelationship(
                candidate_relationship_id=make_id("rel"),
                run_id=run.run_id,
                relationship_family=relationship_family,
                source_candidate_object_ids=[source.candidate_object_id],
                target_candidate_object_ids=[target.candidate_object_id],
                supporting_observation_ids=source.supporting_observation_ids[:1] + target.supporting_observation_ids[:1],
                supporting_evidence=(source.supporting_evidence + target.supporting_evidence)[:4],
                confidence_tier="medium",
            )
            relationships.append(relationship)
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage5a",
                f"candidate-relationship-{relationship.candidate_relationship_id}",
                relationship.model_dump(mode="json"),
                schema_id="core/candidate-relationship",
            )

        conflicts: list[ConflictRecord] = []
        if not stage1.anchor_page_ids:
            conflict = ConflictRecord(
                conflict_id=make_id("conflict"),
                run_id=run.run_id,
                conflict_type="missing_anchor_plan",
                severity="medium",
                related_ids=[run.run_id],
                summary="No high-confidence plan anchor sheet was identified during reconnaissance.",
                impact_scope="Spatial grounding may be incomplete.",
                resolution_status="open",
            )
            conflicts.append(conflict)

        unresolved: list[UnresolvedRecord] = []
        if not support_results:
            unresolved.append(
                UnresolvedRecord(
                    unresolved_id=make_id("unresolved"),
                    run_id=run.run_id,
                    unresolved_type="support_path_not_used",
                    target_ids=[run.run_id],
                    blocking_reason="Stage 4 did not contribute additional support artifacts.",
                    recommended_next_action="Inspect schedule-heavy and note-heavy sheets manually if milestone review is not sufficient.",
                    may_proceed=True,
                )
            )
        if coverage_misses:
            unresolved.append(
                UnresolvedRecord(
                    unresolved_id=make_id("unresolved"),
                    run_id=run.run_id,
                    unresolved_type="playbook_coverage_gap",
                    target_ids=[run.run_id],
                    blocking_reason=f"Active playbook coverage still missing: {', '.join(coverage_misses[:5])}.",
                    recommended_next_action="Request targeted rereads for the missing playbook targets before trusting downstream modeling decisions.",
                    may_proceed=True,
                )
            )
        for task_result in task_results:
            if not task_result.unresolved_questions:
                continue
            unresolved.append(
                UnresolvedRecord(
                    unresolved_id=make_id("unresolved"),
                    run_id=run.run_id,
                    unresolved_type="page_reread_recommended",
                    target_ids=task_result.page_ids,
                    blocking_reason=task_result.unresolved_questions[0],
                    recommended_next_action="Request targeted reread from the milestone board if the evidence is insufficient.",
                    may_proceed=True,
                )
            )

        for conflict in conflicts:
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage5a",
                f"conflict-{conflict.conflict_id}",
                conflict.model_dump(mode="json"),
                schema_id="core/conflict-record",
            )
        for item in unresolved:
            self.artifacts.write_json_artifact(
                project.project_id,
                run.run_id,
                "stage5a",
                f"unresolved-{item.unresolved_id}",
                item.model_dump(mode="json"),
                schema_id="core/unresolved-record",
            )

        readiness = Stage5AReadiness(
            ready_for_human_review=True,
            ready_for_stage6=False,
            coverage_summary=(
                f"Packaged {len(candidate_objects)} candidate object groups across {len(pages)} pages. "
                f"Playbook {playbook.label}: found {len(coverage_hits)} targets and missed {len(coverage_misses)}."
            ),
            blockers=[] if candidate_objects else ["No candidate objects were formed from Stage 3 observations."],
            warnings=[
                *[conflict.summary for conflict in conflicts],
                *([f"Playbook coverage gaps: {', '.join(coverage_misses[:5])}."] if coverage_misses else []),
            ],
            synthesize_now=[candidate.object_family for candidate in candidate_objects if candidate.confidence_tier in {"high", "medium"}],
            synthesize_later=[candidate.object_family for candidate in candidate_objects if candidate.confidence_tier in {"low", "contested", "unknown"}],
        )

        overall_description = (
            f"The run currently reads as a {stage1.project_type_hypothesis} with {len(stage1.page_atlas)} page(s), "
            f"using the {playbook.label} playbook and a primary focus on {', '.join(stage1.candidate_object_families[:4])}."
        )
        precise_understanding = [
            f"Active playbook: {playbook.label}.",
            f"Anchor pages: {len(stage1.anchor_page_ids)} identified.",
            f"Stage 3 produced {len(observations)} observation artifacts.",
            f"Stage 4 produced {len(support_results)} support artifact(s).",
            f"Playbook coverage hits: {', '.join(coverage_hits[:6]) or 'None yet'}.",
            f"Playbook coverage misses: {', '.join(coverage_misses[:6]) or 'None'}.",
            readiness.coverage_summary,
        ]
        package = Stage5APackage(
            run_id=run.run_id,
            package_id=make_id("package"),
            packaging_cycle_id=make_id("cycle"),
            packaging_profile="milestone1_structural_pack",
            readiness=readiness,
            overall_description=overall_description,
            precise_understanding=precise_understanding,
            candidate_objects=candidate_objects,
            candidate_relationships=relationships,
            conflicts=conflicts,
            unresolved=unresolved,
            observation_ids=[item.observation_id for item in observations],
            playbook_key=playbook.key,
            playbook_label=playbook.label,
            coverage_hits=coverage_hits,
            coverage_misses=coverage_misses,
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage5a",
            "package",
            package.model_dump(mode="json"),
            schema_id="stage5a/package",
        )
        self.artifacts.write_text_artifact(
            project.project_id,
            run.run_id,
            "stage5a",
            "overall-understanding",
            "\n".join(["# Stage 5A Understanding", "", overall_description, "", *[f"- {line}" for line in precise_understanding]]),
        )
        return package

    def _stage5b(self, project: ProjectRecord, run: RunRecord, pages: list[PageRecord], package: Stage5APackage) -> Stage5BBoard:
        preview_by_page = {page.page_id: page.preview_artifact for page in pages}
        cards: list[Stage5BCard] = []
        for candidate in package.candidate_objects[:8]:
            page_ids = candidate.spatial_hints.get("page_ids", [])
            page_id = page_ids[0] if page_ids else None
            cards.append(
                Stage5BCard(
                    card_id=make_id("card"),
                    card_type="candidate",
                    title=f"Likely {candidate.display_label or candidate.object_family.replace('_', ' ')}",
                    subtitle=f"Supported by {len(candidate.supporting_observation_ids)} observation(s).",
                    confidence_tier=candidate.confidence_tier,
                    image_asset=preview_by_page.get(page_id),
                    linked_ids=[candidate.candidate_object_id],
                    page_id=page_id,
                    reason="Candidate object group from Stage 5A.",
                )
            )
        for conflict in package.conflicts:
            cards.append(
                Stage5BCard(
                    card_id=make_id("card"),
                    card_type="conflict",
                    title=conflict.summary,
                    subtitle=conflict.impact_scope,
                    confidence_tier="contested",
                    linked_ids=[conflict.conflict_id],
                    reason="Conflict preserved for milestone review.",
                )
            )
        for item in package.unresolved[:5]:
            cards.append(
                Stage5BCard(
                    card_id=make_id("card"),
                    card_type="unresolved",
                    title=item.unresolved_type.replace("_", " ").title(),
                    subtitle=item.blocking_reason,
                    confidence_tier="low",
                    linked_ids=[item.unresolved_id, *item.target_ids],
                    page_id=item.target_ids[0] if item.target_ids else None,
                    image_asset=preview_by_page.get(item.target_ids[0]) if item.target_ids else None,
                    reason="Unresolved record surfaced for human steering.",
                )
            )
        board = Stage5BBoard(
            run_id=run.run_id,
            board_id=make_id("board"),
            summary=(
                "Milestone 1 interpretation board showing candidate objects, conflicts, and unresolved slices. "
                f"Active playbook: {package.playbook_label or 'Generic Structural Pack'}; "
                f"coverage hits {len(package.coverage_hits)} / misses {len(package.coverage_misses)}."
            ),
            cards=cards,
            feedback_targets=[
                {"action_type": "approve", "decision_scope": "checkpoint"},
                {"action_type": "reject", "decision_scope": "checkpoint"},
                {"action_type": "request_reread", "decision_scope": "region"},
                    {"action_type": "discard_card", "decision_scope": "slice"},
                    {"action_type": "discard_sheet", "decision_scope": "region"},
                {"action_type": "note", "decision_scope": "object"},
            ],
        )
        self.artifacts.write_json_artifact(
            project.project_id,
            run.run_id,
            "stage5b",
            "board",
            board.model_dump(mode="json"),
            schema_id="stage5b/board",
        )
        return board

    def _emit(self, run_id: str, stage: str, status: str, message: str, payload: dict[str, Any]) -> None:
        self.database.append_stage_event(run_id, stage, status, message, payload)

    def _mock_model_call(self, prompt_family: str, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "journal_id": make_id("journal"),
            "run_id": run_id,
            "prompt_family": prompt_family,
            "mode": self.settings.model_mode,
            "model": "gpt-5.5" if self.settings.openai_configured else "heuristic-fallback",
            "created_at": now_iso(),
            "payload": payload,
        }

    def _write_orchestrator_artifacts(
        self,
        project_id: str,
        run_id: str,
        stage_status: dict[str, str],
        routing_log: list[dict[str, Any]],
        model_journal: list[dict[str, Any]],
        milestone_decisions: list[dict[str, Any]],
    ) -> None:
        self.artifacts.write_json_artifact(
            project_id,
            run_id,
            "orchestrator",
            "stage-status",
            {"schema_id": "orchestrator/stage-status", "run_id": run_id, "stage_status": stage_status},
        )
        self.artifacts.write_json_artifact(
            project_id,
            run_id,
            "orchestrator",
            "routing-log",
            {"schema_id": "orchestrator/routing-log", "run_id": run_id, "entries": routing_log},
        )
        self.artifacts.write_json_artifact(
            project_id,
            run_id,
            "orchestrator",
            "model-call-journal",
            {"schema_id": "orchestrator/model-call-journal", "run_id": run_id, "entries": model_journal},
        )
        self.artifacts.write_json_artifact(
            project_id,
            run_id,
            "orchestrator",
            "milestone-decisions",
            {"schema_id": "orchestrator/milestone-decisions", "run_id": run_id, "entries": milestone_decisions},
        )


class AppService:
    def __init__(self, settings: Settings, database: Database, artifacts: ArtifactStore) -> None:
        self.settings = settings
        self.database = database
        self.artifacts = artifacts
        self.executor = RunExecutor(settings, database, artifacts)
        self.active_runs: dict[str, threading.Thread] = {}

    def list_projects(self) -> list[ProjectRecord]:
        return self.database.list_projects()

    def create_project(self, name: str, description: str | None) -> ProjectRecord:
        return self.database.create_project(name, description)

    def get_project_detail(self, project_id: str) -> ProjectDetail:
        project = self.database.get_project(project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectDetail(
            project=project,
            documents=self.database.list_source_documents(project_id),
            runs=self.database.list_runs(project_id),
        )

    async def upload_documents(self, project_id: str, files: list[UploadFile]) -> list[SourceDocumentRecord]:
        if self.database.get_project(project_id) is None:
            raise HTTPException(status_code=404, detail="Project not found")
        records: list[SourceDocumentRecord] = []
        for upload in files:
            data = await upload.read()
            if not data:
                continue
            source_id = make_id("source")
            relative_path = self.artifacts.save_upload(project_id, source_id, upload.filename or "upload.pdf", data)
            record = SourceDocumentRecord(
                source_document_id=source_id,
                project_id=project_id,
                original_filename=upload.filename or "upload.pdf",
                stored_path=relative_path,
                checksum=hash_bytes(data),
                file_size=len(data),
                page_count=None,
                created_at=now_iso(),
            )
            with self.database._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO source_documents(source_document_id, project_id, original_filename, stored_path, checksum, file_size, page_count, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.source_document_id,
                        record.project_id,
                        record.original_filename,
                        record.stored_path,
                        record.checksum,
                        record.file_size,
                        record.page_count,
                        record.created_at,
                    ),
                )
            records.append(record)
        return records

    async def create_run(self, project_id: str, request: CreateRunRequest) -> RunRecord:
        project = self.database.get_project(project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        documents = self.database.list_source_documents(project_id)
        if not documents:
            raise HTTPException(status_code=400, detail="Upload at least one PDF before starting a run")
        if request.playbook_override and not has_playbook(request.playbook_override):
            raise HTTPException(status_code=400, detail=f"Unknown playbook override: {request.playbook_override}")
        selected_ids = request.source_document_ids or [document.source_document_id for document in documents]
        if request.feedback_source_run_id:
            feedback_source = self.database.get_run(request.feedback_source_run_id)
            if feedback_source is None or feedback_source.project_id != project_id:
                raise HTTPException(status_code=400, detail="Feedback source run must belong to the same project")
            if request.relaunch_scope == "stage2_to_stage5" and feedback_source.source_document_ids != selected_ids:
                raise HTTPException(status_code=400, detail="Stage 2 to 5 relaunch must use the same source documents as the feedback source run")
        run = self.database.create_run(
            project_id,
            selected_ids,
            request.playbook_override,
            request.feedback_source_run_id,
            request.relaunch_scope,
        )
        queued_message = "Run created and waiting to start."
        queued_payload: dict[str, Any] = {}
        if request.feedback_source_run_id:
            queued_message = "Feedback relaunch created and waiting to start."
            queued_payload = {
                "feedback_source_run_id": request.feedback_source_run_id,
                "relaunch_scope": request.relaunch_scope or "full",
            }
        self.database.append_stage_event(run.run_id, "orchestrator", "queued", queued_message, queued_payload)
        worker = threading.Thread(target=self._run_in_background, args=(run.run_id,), daemon=True, name=f"plan3d-{run.run_id}")
        self.active_runs[run.run_id] = worker
        worker.start()
        return run

    def _run_in_background(self, run_id: str) -> None:
        try:
            self.executor._execute_sync(run_id)
        finally:
            self.active_runs.pop(run_id, None)

    def get_run_snapshot(self, run_id: str) -> RunSnapshot:
        run = self.database.get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="Run not found")
        project = self.database.get_project(run.project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        documents = [document for document in self.database.list_source_documents(project.project_id) if document.source_document_id in run.source_document_ids]
        page_index = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{run.run_id}/stage0/json/page-index.json")
        stage1 = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{run.run_id}/stage1/json/reconnaissance.json")
        stage2 = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{run.run_id}/stage2/json/read-plan.json")
        stage5a = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{run.run_id}/stage5a/json/package.json")
        stage5b = self.artifacts.read_json_if_exists(f"projects/{project.project_id}/runs/{run.run_id}/stage5b/json/board.json")
        stage3_payloads = [
            self.artifacts.read_json(descriptor["path"])
            for descriptor in self.artifacts.list_run_artifacts(project.project_id, run.run_id)
            if descriptor["path"].startswith(f"projects/{project.project_id}/runs/{run.run_id}/stage3/json/task-result-")
        ]
        stage4_payloads = [
            self.artifacts.read_json(descriptor["path"])
            for descriptor in self.artifacts.list_run_artifacts(project.project_id, run.run_id)
            if descriptor["path"].startswith(f"projects/{project.project_id}/runs/{run.run_id}/stage4/json/support-")
        ]

        return RunSnapshot(
            project=project,
            run=run,
            documents=documents,
            pages=[PageRecord.model_validate(payload) for payload in page_index.get("pages", [])] if page_index else [],
            stage_events=self.database.list_stage_events(run_id),
            review_actions=self.database.list_review_actions(run_id),
            stage1=Stage1Reconnaissance.model_validate(stage1) if stage1 else None,
            stage2=ReadPlan.model_validate(stage2) if stage2 else None,
            stage3=[Stage3TaskResult.model_validate(payload) for payload in stage3_payloads],
            stage4=[Stage4SupportArtifact.model_validate(payload) for payload in stage4_payloads],
            stage5a=Stage5APackage.model_validate(stage5a) if stage5a else None,
            stage5b=Stage5BBoard.model_validate(stage5b) if stage5b else None,
            artifacts=self.artifacts.list_run_artifacts(project.project_id, run.run_id),
            config={
                "model_mode": self.settings.model_mode,
                "openai_configured": self.settings.openai_configured,
            },
        )

    def record_review_action(self, run_id: str, request: ReviewActionRequest) -> HumanReviewAction:
        snapshot = self.get_run_snapshot(run_id)
        action = HumanReviewAction(
            action_id=make_id("review"),
            run_id=run_id,
            review_stage="stage5_milestone",
            action_type=request.action_type,
            decision_scope=request.decision_scope,
            target_ids=request.target_ids,
            created_at=now_iso(),
            note=request.note,
            extensions=request.extensions,
        )
        self.database.save_review_action(action)
        self.artifacts.write_json_artifact(
            snapshot.project.project_id,
            run_id,
            "review",
            f"action-{action.action_id}",
            action.model_dump(mode="json"),
            schema_id="review/human-review-action",
        )
        decision_status = {
            "approve": "approved",
            "reject": "needs_correction",
            "request_reread": "rerun_requested",
        }.get(action.action_type, snapshot.run.decision_status)
        if decision_status:
            self.database.update_run(run_id, decision_status=decision_status, status=decision_status)
        self.database.append_stage_event(run_id, "review", "recorded", f"Recorded review action: {action.action_type}.", {"action_id": action.action_id})
        return action
