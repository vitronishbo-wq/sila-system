from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
import os
from dotenv import load_dotenv
load_dotenv()

# Importar Project Root para sys.path
import os
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
# PYTHONPATH should be configured via setup_dev_env.sh; do not modify sys.path here.
# Importar APENAS o Base com metadata
from app.db.base import Base

# Try to get DATABASE_URL from settings or environment
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    try:
        from app.core.settings import settings
        db_url = settings.DATABASE_URL
        # Convert async URL to sync for Alembic
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    except Exception as e:
        print(f"WARNING: Could not load settings: {e}")
        # Fallback: try to build URL from environment variables
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "5432")
        db_user = os.getenv("DB_USER", "sila_user")
        db_password = os.getenv("DB_PASSWORD", "Trumanmarcelo_1983")
        db_name = os.getenv("DB_NAME", "sila_system")
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
else:
    # Convert async URL to sync for Alembic if needed
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version_core"
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with a database connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_core"
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
