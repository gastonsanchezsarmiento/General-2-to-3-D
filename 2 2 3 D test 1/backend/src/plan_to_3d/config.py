from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class Settings:
    app_root: Path
    repo_root: Path
    schema_root: Path
    data_root: Path
    database_path: Path
    frontend_origin: str
    openai_api_key: str | None
    model_mode: str
    stage1_model: str
    stage2_model: str
    stage3_model: str

    @property
    def openai_configured(self) -> bool:
        return bool(self.openai_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    app_root = Path(__file__).resolve().parents[3]
    repo_root = app_root.parent
    env_values = _load_env_file(app_root / ".env")

    def resolve(name: str, default: str | None = None) -> str | None:
        return os.getenv(name) or env_values.get(name) or default

    data_root = app_root / "data"
    data_root.mkdir(parents=True, exist_ok=True)

    return Settings(
        app_root=app_root,
        repo_root=repo_root,
        schema_root=repo_root / "Schemas",
        data_root=data_root,
        database_path=data_root / "plan_to_3d.db",
        frontend_origin=resolve("PLAN3D_FRONTEND_ORIGIN", "http://localhost:5173") or "http://localhost:5173",
        openai_api_key=resolve("OPENAI_API_KEY"),
        model_mode=(resolve("PLAN3D_MODEL_MODE", "mock") or "mock").lower(),
        stage1_model=resolve("PLAN3D_STAGE1_MODEL", "gpt-5.5") or "gpt-5.5",
        stage2_model=resolve("PLAN3D_STAGE2_MODEL", "gpt-5.5") or "gpt-5.5",
        stage3_model=resolve("PLAN3D_STAGE3_MODEL", "gpt-5.5") or "gpt-5.5",
    )

