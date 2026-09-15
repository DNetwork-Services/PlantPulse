from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- PlantPulse additions: make backend/app importable, load our settings ---
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.db.session import Base
# --- end additions ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- PlantPulse: override the URL now that `config` exists ---
config.set_main_option("sqlalchemy.url", settings.database_url)
# --- end ---

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata   # was: target_metadata = None