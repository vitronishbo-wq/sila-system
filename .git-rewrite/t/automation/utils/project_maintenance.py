#!/usr/bin/env python3
"""
Project maintenance CLI (argparse-based)

Subcommands:
    - clean-files: remove cache/temporary files (__pycache__, *.pyc, build artifacts)
    - fix-schemas: placeholder scanner for Pydantic schema modules
    - check-db-urls: validate database URLs in common config locations

Note: This is a scaffold intended to consolidate useful, reusable logic.
        Keep actions idempotent and safe by default. Prefer --dry-run first.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


def get_project_root() -> Path:
    # scripts/project_maintenance.py → project root is parent of parent of this file
    return Path(__file__).resolve().parent.parent


def iter_paths(root: Path, globs: Iterable[str]) -> Iterable[Path]:
    for pattern in globs:
        yield from root.rglob(pattern)


def remove_paths(paths: Iterable[Path], dry_run: bool) -> Tuple[int, int]:
    removed_files = 0
    removed_dirs = 0
    for path in paths:
        try:
            if path.is_dir():
                if dry_run:
                    print(f"[dry-run] rm -rf {path}")
                else:
                    shutil.rmtree(path, ignore_errors=True)
                removed_dirs += 1
            elif path.exists():
                if dry_run:
                    print(f"[dry-run] rm -f {path}")
                else:
                    path.unlink(missing_ok=True)
                removed_files += 1
        except Exception as exc:
            print(f"⚠️ Failed to remove {path}: {exc}")
    return removed_files, removed_dirs


def cmd_clean_files(args: argparse.Namespace) -> int:
    project_root = get_project_root()
    roots = [project_root]
    if args.paths:
        roots = [Path(p).resolve() for p in args.paths]

    file_globs = ["*.pyc", "*.pyo", "*.DS_Store"]
    dir_globs = [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
        "*.egg-info",
    ]

    total_files = 0
    total_dirs = 0
    for root in roots:
        file_iter = iter_paths(root, file_globs)
        dir_iter = (
            d for pattern in dir_globs for d in root.rglob(pattern) if d.is_dir()
        )
        f_count, d_count = remove_paths(list(file_iter), args.dry_run)
        total_files += f_count
        # Remove directories after files to avoid errors
        f_count2, d_count2 = remove_paths(list(dir_iter), args.dry_run)
        total_files += f_count2
        total_dirs += d_count + d_count2

    print(
        f"✅ Clean complete. files={total_files} dirs={total_dirs} dry_run={args.dry_run}"
    )
    return 0


def cmd_fix_schemas(args: argparse.Namespace) -> int:
    """Placeholder: scan for likely Pydantic schema modules and report them.
    This is intentionally non-destructive; extend with real fixers as needed.
    """
    project_root = get_project_root()
    backend_app = project_root / "backend" / "app"
    candidates: List[Path] = []
    for pattern in ("**/schemas.py", "**/schema.py", "**/schemas/*.py"):
        candidates.extend(backend_app.rglob(pattern))

    if not candidates:
        print("ℹ️ No schema files found under backend/app.")
        return 0

    print("🔎 Schema candidates:")
    for c in sorted(candidates):
        rel = c.relative_to(project_root)
        try:
            text = c.read_text(encoding="utf-8", errors="ignore")
            uses_basemodel = bool(
                re.search(
                    r"from\s+pydantic\s+import\s+BaseModel|class\s+\w+\(BaseModel\)",
                    text,
                )
            )
            note = " (pydantic)" if uses_basemodel else ""
            print(f" - {rel}{note}")
        except Exception as exc:
            print(f" - {rel} (error reading: {exc})")

    if args.apply:
        print(
            "⚠️ No automatic fixes implemented in scaffold. Extend this command to apply changes."
        )
    return 0


VALID_SCHEMES = {
    "postgresql",
    "postgresql+asyncpg",
    "mysql",
    "mssql",
    "oracle",
}


def looks_like_db_url(value: str) -> bool:
    return "://" in value and any(value.startswith(s + "://") for s in VALID_SCHEMES)


def cmd_check_db_urls(_: argparse.Namespace) -> int:
    project_root = get_project_root()
    possible_files = [
        project_root / ".env",
        project_root / "backend" / ".env",
        project_root / "backend" / "app" / "core" / "config.py",
        project_root / "backend" / "app" / "core" / "settings.py",
    ]

    found_any = False
    for f in possible_files:
        if not f.exists() or not f.is_file():
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        found_any = True
        print(f"🔎 Checking: {f.relative_to(project_root)}")
        for line in content.splitlines():
            if "DATABASE_URL" in line or "ASYNC_DATABASE_URL" in line:
                value = line.split("=", 1)[-1].strip().strip('"').strip("'")
                if looks_like_db_url(value):
                    print(f"  ✅ {value}")
                else:
                    print(f"  ❌ Suspicious URL: {value}")

    if not found_any:
        print("ℹ️ No config files with DB URLs found in common locations.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-maintenance", description="Project maintenance utilities"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_clean = sub.add_parser("clean-files", help="Remove cache/temporary files")
    p_clean.add_argument(
        "--dry-run", action="store_true", help="Only print what would be removed"
    )
    p_clean.add_argument(
        "--paths",
        nargs="*",
        help="Optional root paths to clean (default: project root)",
    )
    p_clean.set_defaults(func=cmd_clean_files)

    p_schemas = sub.add_parser(
        "fix-schemas", help="Scan or fix Pydantic schemas (scaffold)"
    )
    p_schemas.add_argument(
        "--apply", action="store_true", help="Apply automatic fixes (not implemented)"
    )
    p_schemas.set_defaults(func=cmd_fix_schemas)

    p_db = sub.add_parser("check-db-urls", help="Check database URLs in configs")
    p_db.set_defaults(func=cmd_check_db_urls)

    return parser


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
