#!/usr/bin/env python3
"""🔍 SILA Import Topology Guard

Valida que imports de alto nível não utilizam mais `backend.` ou `frontend.`
como raiz, favorecendo `apps.backend` e `apps.frontend`.

Uso:
    python tools/consistency/check_imports.py
"""

import ast
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent.parent

LEGACY_ROOTS = [
    "backend",
    "frontend",
]

EXCLUDE_DIRS = {
    ".git",
    ".backups",
    "backups",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".cache",
}


def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix != ".py":
        return False
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return False
    return True


def main() -> None:
    violations: List[str] = []

    for path in ROOT.rglob("*.py"):
        if not should_scan(path):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        rel = path.relative_to(ROOT)

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                for root in LEGACY_ROOTS:
                    if node.module == root or node.module.startswith(root + "."):
                        violations.append(
                            f"{rel}: from {node.module} import ... (usar apps.{root}...)"
                        )
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    for root in LEGACY_ROOTS:
                        if alias.name == root or alias.name.startswith(root + "."):
                            violations.append(
                                f"{rel}: import {alias.name} (usar apps.{root}...)"
                            )

    if not violations:
        print("✅ Nenhum import legacy de backend/frontend encontrado.")
        raise SystemExit(0)

    print("❌ Imports legados detectados:")
    for v in violations:
        print(f" - {v}")

    print("\n💡 Corrija os imports para apontarem para apps.backend ou apps.frontend.")
    raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
