"""Alembic chain guard: enforce single head revision."""

from __future__ import annotations

import ast
from pathlib import Path


ALEMBIC_VERSIONS = Path(__file__).resolve().parents[1] / "alembic" / "versions"


def _literal_eval(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def _collect_revisions() -> tuple[set[str], set[str]]:
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

    return revisions, down_revisions


def test_alembic_has_single_head():
    revisions, down_revisions = _collect_revisions()
    heads = sorted(revisions - down_revisions)
    assert len(heads) == 1, f"Expected one alembic head, found {len(heads)}: {heads}"
    assert heads[0] == "20260314_052_transportes_logistica_audit_columns"
