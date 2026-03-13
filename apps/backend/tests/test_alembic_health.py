"""Alembic health guard: ensure upgrade updates alembic_version consistently."""

from __future__ import annotations

import ast
import asyncio
import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


BACKEND_DIR = Path(__file__).resolve().parents[1]
ALEMBIC_INI = BACKEND_DIR / "alembic.ini"
ALEMBIC_VERSIONS = BACKEND_DIR / "alembic" / "versions"
MIGRATION_SENTINEL_TABLES = (
    "pescas_industriais_unidades",
    "pescas_industriais_produtos_processados",
    "pescas_industriais_lotes_producao",
    "pescas_industriais_inspecoes",
    "cultura_artistas",
    "cultura_bens_culturais",
    "cultura_eventos_culturais",
    "cultura_grupos_artisticos",
    "cultura_patrimonios_imateriais",
    "desporto_atletas",
    "desporto_competicoes",
    "desporto_clubes",
    "desporto_jogos",
)


def _literal_eval(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def _expected_head_revision() -> str:
    revisions: set[str] = set()
    down_revisions: set[str] = set()

    for file_path in ALEMBIC_VERSIONS.glob("*.py"):
        module = ast.parse(file_path.read_text(encoding="utf-8", errors="ignore"))
        file_revision = None
        file_down = None
        for node in module.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                value = _literal_eval(node.value)
                if name == "revision" and isinstance(value, str):
                    file_revision = value
                elif name == "down_revision":
                    file_down = value

        if file_revision:
            revisions.add(file_revision)
        if isinstance(file_down, str):
            down_revisions.add(file_down)
        elif isinstance(file_down, tuple):
            down_revisions.update(item for item in file_down if isinstance(item, str))

    heads = sorted(revisions - down_revisions)
    assert len(heads) == 1, f"Expected one alembic head, found {len(heads)}: {heads}"
    return heads[0]


def _run_alembic(*args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ALEMBIC_INI), *args],
        cwd=BACKEND_DIR,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


async def _read_alembic_state(db_url: str) -> tuple[list[str], dict[str, bool]]:
    engine = create_async_engine(db_url, echo=False)
    try:
        async with engine.connect() as conn:
            versions = [
                row[0]
                for row in (
                    await conn.execute(text("SELECT version_num FROM alembic_version ORDER BY version_num"))
                ).fetchall()
            ]
            sentinels = {}
            for table_name in MIGRATION_SENTINEL_TABLES:
                exists = (await conn.execute(text("SELECT to_regclass(:table_name)"), {"table_name": table_name})).scalar()
                sentinels[table_name] = bool(exists)
            return versions, sentinels
    finally:
        await engine.dispose()


@pytest.mark.integration
def test_alembic_upgrade_updates_version_table() -> None:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        pytest.skip("DATABASE_URL not set; skipping alembic health test")
    if "+asyncpg" not in db_url:
        pytest.skip("DATABASE_URL must use postgresql+asyncpg for alembic health test")

    expected_head = _expected_head_revision()
    env = os.environ.copy()
    env["DATABASE_URL"] = db_url

    _run_alembic("upgrade", "head", env=env)
    current = _run_alembic("current", env=env)
    versions, sentinel_tables = asyncio.run(_read_alembic_state(db_url))

    assert expected_head in current.stdout, (
        "alembic current is not at expected head after upgrade. "
        f"expected={expected_head} output={current.stdout.strip()}"
    )
    assert versions == [expected_head], (
        "alembic_version out of sync after upgrade. "
        f"expected={[expected_head]} actual={versions}"
    )

    any_sentinel_exists = any(sentinel_tables.values())
    if any_sentinel_exists and versions != [expected_head]:
        pytest.fail(
            "Detected DDL sentinel tables with stale alembic_version. "
            f"tables={sentinel_tables} versions={versions} expected_head={expected_head}"
        )
