from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .config import Settings
from .models import (
    ArtifactRef,
    CANONICAL_MODELS,
    HumanReviewAction,
    ProjectRecord,
    RunRecord,
    SourceDocumentRecord,
    StageEvent,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in name)
    return cleaned.strip("._") or "file"


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    project_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS source_documents (
                    source_document_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    stored_path TEXT NOT NULL,
                    checksum TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    page_count INTEGER,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    source_document_ids TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_stage TEXT,
                    current_stage_status TEXT,
                    decision_status TEXT,
                    playbook_override TEXT,
                    selected_playbook TEXT,
                    feedback_source_run_id TEXT,
                    relaunch_scope TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS stage_events (
                    event_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS review_actions (
                    action_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            self._ensure_column(connection, "runs", "playbook_override", "TEXT")
            self._ensure_column(connection, "runs", "selected_playbook", "TEXT")
            self._ensure_column(connection, "runs", "feedback_source_run_id", "TEXT")
            self._ensure_column(connection, "runs", "relaunch_scope", "TEXT")

    def _ensure_column(self, connection: sqlite3.Connection, table: str, column: str, column_type: str) -> None:
        columns = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")

    def create_project(self, name: str, description: str | None) -> ProjectRecord:
        project = ProjectRecord(
            project_id=make_id("project"),
            name=name,
            description=description,
            created_at=now_iso(),
        )
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO projects(project_id, name, description, created_at) VALUES (?, ?, ?, ?)",
                (project.project_id, project.name, project.description, project.created_at),
            )
        return project

    def list_projects(self) -> list[ProjectRecord]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
        return [ProjectRecord.model_validate(dict(row)) for row in rows]

    def get_project(self, project_id: str) -> ProjectRecord | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,)).fetchone()
        return ProjectRecord.model_validate(dict(row)) if row else None

    def add_source_document(
        self,
        project_id: str,
        original_filename: str,
        stored_path: str,
        checksum: str,
        file_size: int,
    ) -> SourceDocumentRecord:
        document = SourceDocumentRecord(
            source_document_id=make_id("source"),
            project_id=project_id,
            original_filename=original_filename,
            stored_path=stored_path,
            checksum=checksum,
            file_size=file_size,
            page_count=None,
            created_at=now_iso(),
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO source_documents(
                    source_document_id, project_id, original_filename, stored_path, checksum, file_size, page_count, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document.source_document_id,
                    document.project_id,
                    document.original_filename,
                    document.stored_path,
                    document.checksum,
                    document.file_size,
                    document.page_count,
                    document.created_at,
                ),
            )
        return document

    def update_source_document_page_count(self, source_document_id: str, page_count: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE source_documents SET page_count = ? WHERE source_document_id = ?",
                (page_count, source_document_id),
            )

    def list_source_documents(self, project_id: str) -> list[SourceDocumentRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM source_documents WHERE project_id = ? ORDER BY created_at DESC",
                (project_id,),
            ).fetchall()
        return [SourceDocumentRecord.model_validate(dict(row)) for row in rows]

    def create_run(
        self,
        project_id: str,
        source_document_ids: list[str],
        playbook_override: str | None = None,
        feedback_source_run_id: str | None = None,
        relaunch_scope: str | None = None,
    ) -> RunRecord:
        created_at = now_iso()
        run = RunRecord(
            run_id=make_id("run"),
            project_id=project_id,
            source_document_ids=source_document_ids,
            status="queued",
            current_stage="orchestrator",
            current_stage_status="queued",
            decision_status=None,
            playbook_override=playbook_override,
            selected_playbook=None,
            feedback_source_run_id=feedback_source_run_id,
            relaunch_scope=relaunch_scope,
            created_at=created_at,
            updated_at=created_at,
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO runs(
                    run_id, project_id, source_document_ids, status, current_stage, current_stage_status, decision_status, playbook_override, selected_playbook, feedback_source_run_id, relaunch_scope, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    run.project_id,
                    json.dumps(run.source_document_ids),
                    run.status,
                    run.current_stage,
                    run.current_stage_status,
                    run.decision_status,
                    run.playbook_override,
                    run.selected_playbook,
                    run.feedback_source_run_id,
                    run.relaunch_scope,
                    run.created_at,
                    run.updated_at,
                ),
            )
        return run

    def list_runs(self, project_id: str) -> list[RunRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM runs WHERE project_id = ? ORDER BY created_at DESC",
                (project_id,),
            ).fetchall()
        return [self._row_to_run(row) for row in rows]

    def get_run(self, run_id: str) -> RunRecord | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        return self._row_to_run(row) if row else None

    def update_run(self, run_id: str, **fields: Any) -> RunRecord:
        if not fields:
            run = self.get_run(run_id)
            if run is None:
                raise KeyError(run_id)
            return run

        fields["updated_at"] = now_iso()
        assignments = ", ".join(f"{column} = ?" for column in fields)
        values: list[Any] = []
        for value in fields.values():
            values.append(json.dumps(value) if isinstance(value, list) else value)
        values.append(run_id)

        with self._connect() as connection:
            connection.execute(f"UPDATE runs SET {assignments} WHERE run_id = ?", values)

        updated = self.get_run(run_id)
        if updated is None:
            raise KeyError(run_id)
        return updated

    def append_stage_event(self, run_id: str, stage: str, status: str, message: str, payload: dict[str, Any] | None = None) -> StageEvent:
        event = StageEvent(
            event_id=make_id("event"),
            run_id=run_id,
            stage=stage,
            status=status,
            message=message,
            created_at=now_iso(),
            payload=payload or {},
        )
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO stage_events(event_id, run_id, stage, status, message, created_at, payload) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    event.event_id,
                    event.run_id,
                    event.stage,
                    event.status,
                    event.message,
                    event.created_at,
                    json.dumps(event.payload),
                ),
            )
        return event

    def list_stage_events(self, run_id: str) -> list[StageEvent]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM stage_events WHERE run_id = ? ORDER BY created_at ASC",
                (run_id,),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def save_review_action(self, action: HumanReviewAction) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO review_actions(action_id, run_id, payload, created_at) VALUES (?, ?, ?, ?)",
                (action.action_id, action.run_id, action.model_dump_json(), action.created_at),
            )

    def list_review_actions(self, run_id: str) -> list[HumanReviewAction]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM review_actions WHERE run_id = ? ORDER BY created_at ASC",
                (run_id,),
            ).fetchall()
        return [HumanReviewAction.model_validate_json(row["payload"]) for row in rows]

    def _row_to_run(self, row: sqlite3.Row) -> RunRecord:
        payload = dict(row)
        payload["source_document_ids"] = json.loads(payload["source_document_ids"])
        return RunRecord.model_validate(payload)

    def _row_to_event(self, row: sqlite3.Row) -> StageEvent:
        payload = dict(row)
        payload["payload"] = json.loads(payload["payload"])
        return StageEvent.model_validate(payload)


class ArtifactStore:
    def __init__(self, settings: Settings) -> None:
        self.root = settings.data_root / "artifacts"
        self.root.mkdir(parents=True, exist_ok=True)

    def run_dir(self, project_id: str, run_id: str) -> Path:
        path = self.root / "projects" / project_id / "runs" / run_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def uploads_dir(self, project_id: str) -> Path:
        path = self.root / "projects" / project_id / "uploads"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_upload(self, project_id: str, source_document_id: str, filename: str, data: bytes) -> str:
        destination = self.uploads_dir(project_id) / f"{source_document_id}_{safe_name(filename)}"
        destination.write_bytes(data)
        return self.relative_path(destination)

    def make_run_file(self, project_id: str, run_id: str, stage: str, category: str, filename: str) -> tuple[Path, str]:
        destination = self.run_dir(project_id, run_id) / stage / category / safe_name(filename)
        destination.parent.mkdir(parents=True, exist_ok=True)
        return destination, self.relative_path(destination)

    def write_json_artifact(
        self,
        project_id: str,
        run_id: str,
        stage: str,
        name: str,
        payload: dict[str, Any],
        schema_id: str | None = None,
    ) -> ArtifactRef:
        model = CANONICAL_MODELS.get(schema_id or "")
        normalized = model.model_validate(payload).model_dump(mode="json") if model else payload
        destination, relative_path = self.make_run_file(project_id, run_id, stage, "json", f"{name}.json")
        destination.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
        return ArtifactRef(
            artifact_id=make_id("artifact"),
            artifact_type="json",
            schema_id=schema_id,
            schema_version=normalized.get("schema_version") if isinstance(normalized, dict) else None,
            run_id=run_id,
            path=relative_path,
        )

    def write_text_artifact(self, project_id: str, run_id: str, stage: str, name: str, content: str) -> ArtifactRef:
        destination, relative_path = self.make_run_file(project_id, run_id, stage, "text", f"{name}.md")
        destination.write_text(content, encoding="utf-8")
        return ArtifactRef(
            artifact_id=make_id("artifact"),
            artifact_type="markdown",
            run_id=run_id,
            path=relative_path,
        )

    def read_json(self, relative_path: str) -> dict[str, Any]:
        return json.loads((self.root / relative_path).read_text(encoding="utf-8"))

    def read_json_if_exists(self, relative_path: str | None) -> dict[str, Any] | None:
        if not relative_path:
            return None
        target = self.root / relative_path
        if not target.exists():
            return None
        return json.loads(target.read_text(encoding="utf-8"))

    def list_run_artifacts(self, project_id: str, run_id: str) -> list[dict[str, Any]]:
        run_root = self.run_dir(project_id, run_id)
        artifacts: list[dict[str, Any]] = []
        for file_path in sorted(run_root.rglob("*")):
            if not file_path.is_file():
                continue
            relative_path = self.relative_path(file_path)
            descriptor: dict[str, Any] = {
                "path": relative_path,
                "size": file_path.stat().st_size,
                "kind": file_path.suffix.lstrip("."),
            }
            if file_path.suffix == ".json":
                try:
                    payload = json.loads(file_path.read_text(encoding="utf-8"))
                    descriptor["schema_id"] = payload.get("schema_id")
                except json.JSONDecodeError:
                    descriptor["schema_id"] = None
            artifacts.append(descriptor)
        return artifacts

    def relative_path(self, file_path: Path) -> str:
        return file_path.relative_to(self.root).as_posix()

    def absolute_path(self, relative_path: str) -> Path:
        return self.root / relative_path
