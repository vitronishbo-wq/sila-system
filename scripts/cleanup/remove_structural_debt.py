#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BACKEND_ROOT = REPO_ROOT / "apps" / "backend"

DEFAULT_DUPLICATE_DIRS = [
    "modules/finance/financas",
    "modules/service_requests/service_requests",
    "modules/identity/identity",
]


def remove_path(path: Path, *, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)
    return True


def cleanup_pycache(root: Path, *, dry_run: bool) -> int:
    removed = 0
    for path in root.rglob("__pycache__"):
        if not path.is_dir():
            continue
        removed += 1
        if not dry_run:
            shutil.rmtree(path, ignore_errors=True)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove duplicate legacy folders and cache artifacts.",
    )
    parser.add_argument(
        "--backend-root",
        type=Path,
        default=DEFAULT_BACKEND_ROOT,
        help=f"Backend root directory (default: {DEFAULT_BACKEND_ROOT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup actions without deleting files.",
    )
    parser.add_argument(
        "--purge-alembic-versions",
        action="store_true",
        help="Delete all alembic version files under backend/alembic/versions.",
    )
    args = parser.parse_args()

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"[MODE] {mode}")

    deleted_duplicates = 0
    for rel_path in DEFAULT_DUPLICATE_DIRS:
        candidate = args.backend_root / rel_path
        deleted = remove_path(candidate, dry_run=args.dry_run)
        status = "removed" if deleted else "missing"
        if deleted:
            deleted_duplicates += 1
        print(f"[DUPLICATE] {candidate} -> {status}")

    removed_pycache = cleanup_pycache(args.backend_root, dry_run=args.dry_run)
    print(f"[CACHE] __pycache__ directories removed={removed_pycache}")

    removed_versions = 0
    if args.purge_alembic_versions:
        versions_dir = args.backend_root / "alembic" / "versions"
        for path in versions_dir.glob("*.py"):
            if remove_path(path, dry_run=args.dry_run):
                removed_versions += 1
        print(f"[ALEMBIC] version files removed={removed_versions}")

    print(
        f"[SUMMARY] duplicate_dirs={deleted_duplicates} "
        f"pycache_dirs={removed_pycache} alembic_versions={removed_versions}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
