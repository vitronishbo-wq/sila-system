#!/usr/bin/env python3
"""🛰️ SILA Path Consistency Check

Garante que referências legadas a `backend/` e `frontend/` não reapareçam
fora das zonas explicitamente permitidas, reforçando a topologia `apps/`.

Uso:
    python tools/consistency/check_paths.py
"""

import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent.parent

ALLOWED_SUBSTRINGS = [
    "apps/backend",
    "apps/frontend",
]

LEGACY_TOKENS = [
    "backend/",
    "frontend/",
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

INCLUDE_EXT = {
    ".py",
    ".sh",
    ".yml",
    ".yaml",
    ".md",
    ".json",
    ".toml",
}


def should_scan(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return False
    if not path.is_file():
        return False
    if path.suffix in INCLUDE_EXT or path.name in {"Makefile"}:
        return True
    return False


def main() -> None:
    violations: List[str] = []

    for path in ROOT.rglob("*"):
        if not should_scan(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in LEGACY_TOKENS:
            if token not in text:
                continue
            # Ignorar casos obviamente já migrados para apps/
            if any(app_token in text for app_token in ALLOWED_SUBSTRINGS):
                continue
            rel = path.relative_to(ROOT)
            violations.append(f"{rel}: contém token legado '{token}'")

    if not violations:
        print("✅ Nenhuma referência de path legado encontrada.")
        raise SystemExit(0)

    print("❌ Inconsistências de paths detectadas:")
    for v in violations:
        print(f" - {v}")

    print(
        "\n💡 Ação recomendada: executar 'python tools/refactor/update_paths.py --dry-run' para inspecionar possíveis correções."
    )
    raise SystemExit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
