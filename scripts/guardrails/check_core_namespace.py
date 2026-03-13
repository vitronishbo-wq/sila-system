#!/usr/bin/env python3
"""Guardrail: block legacy `core.*` imports outside allowed legacy zones."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FROM_RE = re.compile(r"^\s*from\s+core\.")
IMPORT_RE = re.compile(r"^\s*import\s+core\.")

DEFAULT_ROOT = Path("apps/backend")
DEFAULT_EXCLUDES = (
    "apps/backend/core/",
    "apps/backend/tests/",
    "__pycache__/",
    ".venv/",
    "node_modules/",
)


def should_skip(path: Path, root: Path, excludes: tuple[str, ...]) -> bool:
    normalized = str(path.as_posix())
    for item in excludes:
        if item in normalized:
            return True
    # Skip generated migration example docs under legacy core
    if normalized.endswith("MIGRATION_EXAMPLE.py"):
        return True
    return False


def scan(root: Path, excludes: tuple[str, ...]) -> list[tuple[Path, int, str]]:
    violations: list[tuple[Path, int, str]] = []
    for py_file in root.rglob("*.py"):
        if should_skip(py_file, root, excludes):
            continue
        try:
            text = py_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if FROM_RE.match(line) or IMPORT_RE.match(line):
                violations.append((py_file, lineno, stripped))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail when `core.*` imports are used outside approved legacy folders."
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help="Root path to scan.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional exclude substring (repeatable).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    excludes = tuple(DEFAULT_EXCLUDES) + tuple(args.exclude)

    if not root.exists():
        raise SystemExit(f"Root not found: {root}")

    violations = scan(root, excludes)
    if not violations:
        print("OK: no forbidden `core.*` imports found in guarded paths.")
        return 0

    print("Forbidden legacy imports detected (`core.*`):")
    for path, lineno, line in violations:
        rel = path.as_posix()
        print(f"- {rel}:{lineno} -> {line}")

    print("")
    print("Use canonical namespace imports (e.g. `app.core.*`).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
