#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run(command: str, *, cwd: Path) -> None:
    print(f"[RUN] {command}", flush=True)
    subprocess.run(shlex.split(command), cwd=cwd, check=True)


def command_exists(command_name: str) -> bool:
    return shutil.which(command_name) is not None


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute enterprise consolidation pipeline for legacy migration.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Apply changes. Without this flag, migration scripts run in dry-run mode.",
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip `ruff check --fix`.",
    )
    parser.add_argument(
        "--skip-cleanup",
        action="store_true",
        help="Skip structural cleanup step.",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip `pytest`.",
    )
    parser.add_argument(
        "--run-alembic-reset",
        action="store_true",
        help="Run controlled alembic reset/revision/upgrade sequence.",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()

    cleanup_cmd = "python3 scripts/cleanup/remove_structural_debt.py"
    migrate_cmd = "python3 scripts/migration/auto_migrate_legacy.py"
    fix_imports_cmd = "python3 scripts/migration/fix_imports.py"

    if not args.execute:
        cleanup_cmd += " --dry-run"
        migrate_cmd += " --dry-run"
        fix_imports_cmd += " --dry-run"

    if not args.skip_cleanup:
        run(cleanup_cmd, cwd=REPO_ROOT)

    run(migrate_cmd, cwd=REPO_ROOT)
    run(fix_imports_cmd, cwd=REPO_ROOT)

    if args.run_alembic_reset:
        run("alembic downgrade base", cwd=REPO_ROOT)
        run('alembic revision --autogenerate -m "enterprise consolidation"', cwd=REPO_ROOT)
        run("alembic upgrade head", cwd=REPO_ROOT)

    if not args.skip_lint:
        if command_exists("ruff"):
            run("ruff check . --fix", cwd=REPO_ROOT)
        else:
            print("[SKIP] ruff not found in PATH")

    if not args.skip_tests:
        if command_exists("pytest"):
            run("pytest", cwd=REPO_ROOT)
        else:
            print("[SKIP] pytest not found in PATH")

    mode = "APPLY" if args.execute else "DRY-RUN"
    print(f"[ENTERPRISE CONSOLIDATION COMPLETE] mode={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
