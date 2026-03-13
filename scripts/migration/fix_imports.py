#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCOPE = REPO_ROOT / "apps" / "backend"
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}

DEFAULT_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bfrom\s+modules\.education\b"), "from app.domain.academic"),
    (re.compile(r"\bimport\s+modules\.education\b"), "import app.domain.academic"),
    (re.compile(r"\bfrom\s+modules\.educacao\b"), "from app.domain.academic"),
    (re.compile(r"\bimport\s+modules\.educacao\b"), "import app.domain.academic"),
    (re.compile(r"\bfrom\s+modules\.finance\b"), "from app.domain.finance"),
    (re.compile(r"\bimport\s+modules\.finance\b"), "import app.domain.finance"),
    (re.compile(r"\bfrom\s+modules\.financas\b"), "from app.domain.finance"),
    (re.compile(r"\bimport\s+modules\.financas\b"), "import app.domain.finance"),
    (re.compile(r"\bfrom\s+modules\.civil_identity\b"), "from app.domain.identity"),
    (re.compile(r"\bimport\s+modules\.civil_identity\b"), "import app.domain.identity"),
    (re.compile(r"\bfrom\s+modules\.identidade_civil\b"), "from app.domain.identity"),
    (re.compile(r"\bimport\s+modules\.identidade_civil\b"), "import app.domain.identity"),
    (re.compile(r"\bfrom\s+app\.citizen\.core\.models\b"), "from apps.backend.app.modules.identity.core.models"),
    (re.compile(r"\bimport\s+app\.citizen\.core\.models\b"), "import apps.backend.app.modules.identity.core.models"),
    (re.compile(r"\bfrom\s+app\.citizen\.service\b"), "from apps.backend.app.modules.identity.service"),
    (re.compile(r"\bimport\s+app\.citizen\.service\b"), "import apps.backend.app.modules.identity.service"),
    (re.compile(r"\bfrom\s+app\.citizen\.enums\b"), "from apps.backend.app.modules.identity.enums"),
    (re.compile(r"\bimport\s+app\.citizen\.enums\b"), "import apps.backend.app.modules.identity.enums"),
    (re.compile(r"\bfrom\s+app\.citizen\.exceptions\b"), "from apps.backend.app.modules.identity.exceptions"),
    (re.compile(r"\bimport\s+app\.citizen\.exceptions\b"), "import apps.backend.app.modules.identity.exceptions"),
    (re.compile(r"\bfrom\s+app\.citizen\.events\.models\b"), "from apps.backend.app.modules.identity.events.models"),
    (re.compile(r"\bimport\s+app\.citizen\.events\.models\b"), "import apps.backend.app.modules.identity.events.models"),
    (re.compile(r"\bfrom\s+app\.citizen\.projections\.projectors\b"), "from apps.backend.app.modules.identity.projections.projectors"),
    (re.compile(r"\bimport\s+app\.citizen\.projections\.projectors\b"), "import apps.backend.app.modules.identity.projections.projectors"),
]


@dataclass
class FileChange:
    path: Path
    replacements: int


def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in DEFAULT_EXCLUDE_DIRS:
            return True
        if part.startswith("app.backup."):
            return True
    return False


def transform_content(content: str) -> tuple[str, int]:
    total = 0
    updated = content
    for pattern, replacement in DEFAULT_REPLACEMENTS:
        updated, count = pattern.subn(replacement, updated)
        total += count
    return updated, total


def iter_python_files(scope: Path) -> list[Path]:
    if scope.is_file() and scope.suffix == ".py":
        return [scope]
    return sorted(
        path
        for path in scope.rglob("*.py")
        if path.is_file() and not is_excluded(path)
    )


def apply_fixes(*, scope: Path, dry_run: bool) -> tuple[list[FileChange], int]:
    changed_files: list[FileChange] = []
    total_replacements = 0

    for path in iter_python_files(scope):
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        updated, replacements = transform_content(original)
        if replacements == 0:
            continue

        changed_files.append(FileChange(path=path, replacements=replacements))
        total_replacements += replacements
        if not dry_run:
            path.write_text(updated, encoding="utf-8")

    return changed_files, total_replacements


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rewrite legacy module imports to domain namespaces.",
    )
    parser.add_argument(
        "--scope",
        type=Path,
        default=DEFAULT_SCOPE,
        help=f"Root folder or file to scan (default: {DEFAULT_SCOPE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show candidate changes without writing files.",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    changes, replacement_count = apply_fixes(scope=args.scope, dry_run=args.dry_run)

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"[MODE] {mode}")
    print(
        f"[SUMMARY] files_changed={len(changes)} replacements={replacement_count} scope={args.scope}"
    )
    for item in changes:
        relative = item.path.relative_to(REPO_ROOT) if item.path.is_relative_to(REPO_ROOT) else item.path
        print(f" - {relative} ({item.replacements} replacements)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
