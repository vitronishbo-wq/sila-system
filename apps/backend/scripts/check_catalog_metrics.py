#!/usr/bin/env python3
"""Print catalog integrity metrics from the target database."""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.core.settings import settings  # noqa: E402


def _sync_url() -> str:
    url = settings.DATABASE_URL
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


def main() -> None:
    engine = create_engine(_sync_url(), future=True)
    with engine.connect() as conn:
        metrics = {
            "modules": conn.execute(text("select count(1) from modules")).scalar(),
            "services": conn.execute(text("select count(1) from services")).scalar(),
            "unique_codes": conn.execute(
                text("select count(distinct code) from services")
            ).scalar(),
            "missing_workflow": conn.execute(
                text(
                    "select count(1) from services "
                    "where workflow_definition_key is null or workflow_definition_key = ''"
                )
            ).scalar(),
            "missing_sla": conn.execute(
                text(
                    "select count(1) from services where estimated_days is null or estimated_days < 1"
                )
            ).scalar(),
            "orphan_services": conn.execute(
                text(
                    "select count(1) "
                    "from services s left join modules m on m.id = s.module_id "
                    "where s.module_id is null or m.id is null"
                )
            ).scalar(),
        }

    engine.dispose()
    print(metrics)


if __name__ == "__main__":
    main()
