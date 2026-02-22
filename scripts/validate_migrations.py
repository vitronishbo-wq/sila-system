#!/usr/bin/env python3
"""Validate Alembic migrations: compare DB current revision with migration heads.

Usage: DATABASE_URL env var must be set. Exits with code 0 when up-to-date,
1 otherwise.
"""
import os
import sys
from sqlalchemy import create_engine
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext


def _get_db_url():
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("ERROR: DATABASE_URL not set", file=sys.stderr)
        sys.exit(2)
    # If async driver is provided, switch to sync for alembic runtime check
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


def main():
    # alembic_core lives under apps/backend in this repository layout
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "apps", "backend", "alembic_core", "alembic.ini")
    cfg_path = os.path.normpath(cfg_path)
    cfg = Config(cfg_path)
    script = ScriptDirectory.from_config(cfg)
    heads = script.get_heads()

    db_url = _get_db_url()
    engine = create_engine(db_url)
    with engine.connect() as conn:
        mc = MigrationContext.configure(conn)
        current = mc.get_current_revision()

    print("Migration heads:", heads)
    print("Current DB revision:", current)

    if current in heads:
        print("Migrations are up-to-date.")
        sys.exit(0)
    else:
        print("Migrations are NOT up-to-date.")
        sys.exit(1)


if __name__ == "__main__":
    main()
