# Plan To 3D Milestone 1

This folder contains the first implementation cut for milestone 1 of the repository execution plan.

It is structured as one application with:

- `backend/`: FastAPI API, filesystem artifact store, SQLite index, staged pipeline through Stage 5B
- `frontend/`: Vite + React review and developer workspace shell

## OpenAI key

Do not paste your API key into chat.

Create a local `.env` file in this folder from `.env.example` and set:

```text
OPENAI_API_KEY=your_key_here
PLAN3D_MODEL_MODE=openai
PLAN3D_STAGE1_MODEL=gpt-5.5
PLAN3D_STAGE2_MODEL=gpt-5.5
PLAN3D_STAGE3_MODEL=gpt-5.5
```

`PLAN3D_MODEL_MODE=openai` enables real Responses API calls for Stage 1 reconnaissance, Stage 2 planning, and Stage 3 targeted reading.

If you need a deterministic local fallback, temporarily switch back to:

```text
PLAN3D_MODEL_MODE=mock
```

## Backend

```powershell
Set-Location "backend"
python -m pip install -e .[dev]
python -m plan_to_3d.main
```

The API runs on `http://localhost:8000` by default and serves generated artifact files from `/artifacts/...`.

When starting a run you can now optionally set a reading playbook override such as `warehouse_portal_frame`, `warehouse_tilt_panel`, or `steel_frame_industrial`. If no override is supplied, Stage 1 chooses a default playbook from the pack hypotheses.

The frontend run form exposes the same playbook selector, and the backend also returns the available playbooks from `/api/config`.

## Frontend

```powershell
Set-Location "frontend"
npm.cmd install
npm.cmd run dev
```

The frontend expects the backend at `http://localhost:8000`.
