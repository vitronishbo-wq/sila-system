#!/usr/bin/env python3
"""Guardrail: enforce module registry consistency against modules on disk."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.module_registry import (  # noqa: E402
    find_bootstrap_misalignment,
    find_unregistered_modules,
    iter_modules,
)


def find_missing_enabled_modules(modules_root: Path) -> tuple[str, ...]:
    discovered = {
        folder.name
        for folder in modules_root.iterdir()
        if folder.is_dir() and not folder.name.startswith("__")
    }
    missing = sorted(
        spec.name
        for spec in iter_modules(enabled_only=True)
        if spec.name not in discovered
    )
    return tuple(missing)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail if explicit module registry diverges from modules on disk."
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root).resolve()
    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    unregistered = find_unregistered_modules(modules_root)
    missing_enabled = find_missing_enabled_modules(modules_root)
    misaligned_bootstrap = find_bootstrap_misalignment(modules_root)

    if not unregistered and not missing_enabled and not misaligned_bootstrap:
        print("OK: module registry is synchronized with modules on disk.")
        return 0

    print("Module registry synchronization issues detected:")
    if unregistered:
        print(
            "- Unregistered module folders (present on disk, missing in registry): "
            + ", ".join(unregistered)
        )
    if missing_enabled:
        print(
            "- Missing enabled modules (present in registry, missing on disk): "
            + ", ".join(missing_enabled)
        )
    if misaligned_bootstrap:
        print(
            "- Bootstrap misalignment (bootstrap-enabled module missing on disk): "
            + ", ".join(misaligned_bootstrap)
        )

    print("")
    print("Update `app/core/module_registry.py` and/or module folders before merging.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
