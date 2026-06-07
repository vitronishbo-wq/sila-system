#!/usr/bin/env python
"""
Fix imports that still point to removed per-module files.

Currently handles:
- DomainException imports from domain_exception.py
- BaseRepository imports from base_repository.py

Default is dry-run. Use --apply to write changes.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

DOMAIN_IMPORT_RE = re.compile(r"^\s*from\s+[\w\.]*domain_exception\s+import\s+(?P<imports>.+)$")
BASE_IMPORT_RE = re.compile(r"^\s*from\s+[\w\.]*base_repository\s+import\s+(?P<imports>.+)$")

DOMAIN_REPLACEMENT = "from apps.backend.core.exceptions.domain_exception import DomainException"
BASE_REPLACEMENT = "from apps.backend.core.repositories.base_repository import BaseRepository"


def _needs_review(import_list: str, expected: str) -> bool:
    parts = [p.strip() for p in import_list.split(",")]
    return not (len(parts) == 1 and parts[0] == expected)


def process_file(path: Path, apply_changes: bool) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    warnings: list[str] = []
    new_lines: list[str] = []

    for line in lines:
        domain_match = DOMAIN_IMPORT_RE.match(line)
        if domain_match and "DomainException" in domain_match.group("imports"):
            if _needs_review(domain_match.group("imports"), "DomainException"):
                warnings.append(
                    f"{path}: non-standard DomainException import list: "
                    f"{domain_match.group('imports')}"
                )
            new_lines.append(DOMAIN_REPLACEMENT)
            changed = True
            continue

        base_match = BASE_IMPORT_RE.match(line)
        if base_match and "BaseRepository" in base_match.group("imports"):
            if _needs_review(base_match.group("imports"), "BaseRepository"):
                warnings.append(
                    f"{path}: non-standard BaseRepository import list: "
                    f"{base_match.group('imports')}"
                )
            new_lines.append(BASE_REPLACEMENT)
            changed = True
            continue

        new_lines.append(line)

    if changed and apply_changes:
        path.write_text(
            "\n".join(new_lines) + ("\n" if text.endswith("\n") else ""),
            encoding="utf-8",
        )

    return changed, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix imports that reference removed per-module files."
    )
    parser.add_argument(
        "--root",
        default="apps/backend",
        help="Root path to scan (default: apps/backend)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files (default: dry-run)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Root path not found: {root}")
        return 1

    changed_files: list[str] = []
    warnings: list[str] = []

    for path in root.rglob("*.py"):
        changed, warn = process_file(path, args.apply)
        if changed:
            changed_files.append(str(path))
        warnings.extend(warn)

    print(f"changed_files: {len(changed_files)}")
    for p in changed_files:
        print(p)

    if warnings:
        print(f"warnings: {len(warnings)}")
        for w in warnings:
            print(w)

    if not args.apply:
        print("dry_run: no files were modified")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
