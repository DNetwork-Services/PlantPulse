from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# This file lives at: backend/app/core/config.py
# parents[0] = core, [1] = app, [2] = backend, [3] = repo root.
# Anchoring to __file__'s real location (not the current working
# directory) means this works identically whether you run alembic
# from backend/, from the repo root, or from anywhere else.
BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """
    Centralized, typed config. Reads from environment variables —
    populated via .env locally, via ECS task definition / Secrets
    Manager in AWS later. Same code, different source per environment.
    """
    database_url: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()