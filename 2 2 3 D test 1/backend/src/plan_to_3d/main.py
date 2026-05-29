from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .models import CreateProjectRequest, CreateRunRequest, ReviewActionRequest
from .playbooks import list_playbook_summaries
from .services import AppService
from .storage import ArtifactStore, Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    database = Database(settings.database_path)
    artifacts = ArtifactStore(settings)
    app.state.services = AppService(settings, database, artifacts)
    app.mount("/artifacts", StaticFiles(directory=artifacts.root), name="artifacts")
    yield


app = FastAPI(title="Plan To 3D Milestone 1", lifespan=lifespan)
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def service(request: Request) -> AppService:
    return request.app.state.services


@app.get("/api/health")
def health() -> dict[str, object]:
    current = get_settings()
    return {
        "status": "ok",
        "model_mode": current.model_mode,
        "openai_configured": current.openai_configured,
    }


@app.get("/api/config")
def config() -> dict[str, object]:
    current = get_settings()
    return {
        "frontend_origin": current.frontend_origin,
        "model_mode": current.model_mode,
        "openai_configured": current.openai_configured,
        "available_playbooks": list_playbook_summaries(),
    }


@app.get("/api/projects")
def list_projects(request: Request):
    return service(request).list_projects()


@app.post("/api/projects")
def create_project(payload: CreateProjectRequest, request: Request):
    return service(request).create_project(payload.name, payload.description)


@app.get("/api/projects/{project_id}")
def get_project(project_id: str, request: Request):
    return service(request).get_project_detail(project_id)


@app.post("/api/projects/{project_id}/documents")
async def upload_documents(project_id: str, request: Request, files: list[UploadFile] = File(...)):
    return await service(request).upload_documents(project_id, files)


@app.post("/api/projects/{project_id}/runs")
async def create_run(project_id: str, payload: CreateRunRequest, request: Request):
    return await service(request).create_run(project_id, payload)


@app.get("/api/projects/{project_id}/runs")
def list_runs(project_id: str, request: Request):
    return service(request).get_project_detail(project_id).runs


@app.get("/api/runs/{run_id}")
def get_run(run_id: str, request: Request):
    return service(request).get_run_snapshot(run_id)


@app.post("/api/runs/{run_id}/review-actions")
def record_review_action(run_id: str, payload: ReviewActionRequest, request: Request):
    return service(request).record_review_action(run_id, payload)


@app.get("/api/runs/{run_id}/stream")
async def stream_run(run_id: str, request: Request):
    async def event_source():
        last_signature = ""
        while True:
            if await request.is_disconnected():
                break
            snapshot = service(request).get_run_snapshot(run_id)
            signature = json.dumps(
                {
                    "status": snapshot.run.status,
                    "current_stage": snapshot.run.current_stage,
                    "events": len(snapshot.stage_events),
                    "decision_status": snapshot.run.decision_status,
                },
                sort_keys=True,
            )
            if signature != last_signature:
                last_signature = signature
                yield f"data: {snapshot.model_dump_json()}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_source(), media_type="text/event-stream")


def run() -> None:
    uvicorn.run("plan_to_3d.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    run()