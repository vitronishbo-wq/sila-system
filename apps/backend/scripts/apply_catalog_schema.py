#!/usr/bin/env python3
"""Apply catalog schema through Alembic (single migration chain)."""

from __future__ import annotations

from pathlib import Path
import sys

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.core.settings import settings


LEGACY_BRANCH_HEADS = ("add_import_batch_id_to_territory", "20231027001")


def _sync_url() -> str:
    if settings.DATABASE_URL.startswith("postgresql+asyncpg://"):
        return settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)
    return settings.DATABASE_URL


def _prepare_brownfield_alembic_state() -> None:
    """For existing databases without Alembic history, stamp legacy branch heads.

    This prevents replaying old migrations that would try to recreate existing objects.
    """
    engine = create_engine(_sync_url(), future=True)
    try:
        with engine.begin() as conn:
            table_exists = conn.execute(text("select to_regclass('public.alembic_version')")).scalar()
            if not table_exists:
                conn.execute(text("create table alembic_version (version_num varchar(64) not null)"))

            # Brownfield heuristic: schema already has operational data tables.
            has_existing_schema = bool(
                conn.execute(
                    text(
                        "select 1 from information_schema.tables "
                        "where table_schema='public' and table_name in "
                        "('users','citizen_fuc','modules','services','operational_orders') limit 1"
                    )
                ).fetchone()
            )

            if has_existing_schema:
                # Normalize to known branch heads to avoid overlap errors
                # (e.g. ancestor + descendant simultaneously in alembic_version).
                conn.execute(text("delete from alembic_version"))
                for revision in LEGACY_BRANCH_HEADS:
                    conn.execute(
                        text("insert into alembic_version (version_num) values (:revision)"),
                        {"revision": revision},
                    )
    finally:
        engine.dispose()


def apply() -> None:
    _prepare_brownfield_alembic_state()
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    command.upgrade(config, "head")
    print("Alembic upgrade head completed (catalog schema included).")


if __name__ == "__main__":
    apply()
