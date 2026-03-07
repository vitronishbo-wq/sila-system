#!/usr/bin/env python3
"""Detect cross-module imports under apps/backend/app/modules."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FROM_RE = re.compile(r"^\s*from\s+app\.modules\.([a-zA-Z0-9_]+)\b")
IMPORT_RE = re.compile(r"^\s*import\s+app\.modules\.([a-zA-Z0-9_]+)\b")


def collect_modules(modules_root: Path) -> set[str]:
    return {
        p.name
        for p in modules_root.iterdir()
        if p.is_dir() and p.name != "__pycache__"
    }


def scan_module_file(py_file: Path, current_module: str, module_set: set[str]) -> list[str]:
    violations: list[str] = []
    try:
        text = py_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return violations

    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("#"):
            continue

        match = FROM_RE.search(line) or IMPORT_RE.search(line)
        if not match:
            continue

        imported_module = match.group(1)
        if imported_module in module_set and imported_module != current_module:
            violations.append(
                f"{py_file}:{i} imports app.modules.{imported_module}"
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check cross-module imports in backend modules.",
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root",
    )
    parser.add_argument(
        "--fail-on-violation",
        action="store_true",
        help="Exit with code 1 if violations are found.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root)
    if not modules_root.exists():
        print(f"Modules root not found: {modules_root}")
        return 2

    module_set = collect_modules(modules_root)
    violations: list[str] = []

    for module in sorted(module_set):
        module_path = modules_root / module
        for py_file in module_path.rglob("*.py"):
            violations.extend(scan_module_file(py_file, module, module_set))

    print(f"Scanned modules: {len(module_set)}")
    print(f"Cross-module imports detected: {len(violations)}")
    for item in violations:
        print(f" - {item}")

    if args.fail_on_violation and violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
