#!/usr/bin/env python3
"""Guardrail: require AI architecture guide update for rector architecture changes."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GUIDE = "docs/AI_ARCHITECTURE_GUIDE.md"
DEFAULT_RECTOR_PATHS = (
    "apps/backend/app/core/module_registry.py",
    "apps/backend/app/api/router.py",
    "apps/backend/app/main.py",
    "scripts/run_guardrails.sh",
    "scripts/domain_overlap_analysis.py",
    "scripts/module_dependency_analysis.py",
    "scripts/architecture_map_report.py",
    "scripts/module_health_report.py",
    "scripts/migration_domain_inventory.py",
    "scripts/guardrails/check_core_namespace.py",
    "scripts/guardrails/check_module_registry_sync.py",
    "scripts/guardrails/check_architecture_guide_sync.py",
    "docs/architecture/module_federation_plan.md",
    "docs/architecture/migration_strategy.md",
)


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def changed_files_from_worktree() -> set[str]:
    changed: set[str] = set()
    commands = (
        ["diff", "--name-only", "--diff-filter=ACMRD"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMRD"],
        ["ls-files", "--others", "--exclude-standard"],
    )
    for command in commands:
        result = run_git(command)
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            if line.strip():
                changed.add(line.strip().replace("\\", "/"))
    return changed


def resolve_base_ref(explicit_base_ref: str | None) -> str | None:
    if explicit_base_ref:
        return explicit_base_ref

    guardrails_base = os.environ.get("GUARDRAILS_BASE_REF")
    if guardrails_base:
        return guardrails_base

    github_base = os.environ.get("GITHUB_BASE_REF")
    if github_base:
        return f"origin/{github_base}"

    return None


def changed_files_from_base(base_ref: str) -> set[str]:
    result = run_git(
        ["diff", "--name-only", "--diff-filter=ACMRD", f"{base_ref}...HEAD"]
    )
    if result.returncode != 0:
        return set()
    return {
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    }


def is_rector_path(path: str, rector_paths: tuple[str, ...]) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized == marker for marker in rector_paths)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fail when architecture rector files change without updating "
            "docs/AI_ARCHITECTURE_GUIDE.md in the same change set."
        )
    )
    parser.add_argument(
        "--guide-path",
        default=DEFAULT_GUIDE,
        help="Path to AI architecture guide file.",
    )
    parser.add_argument(
        "--base-ref",
        default=None,
        help=(
            "Optional git base ref for comparison (example: origin/main). "
            "If omitted, the current working tree is used."
        ),
    )
    parser.add_argument(
        "--rector-path",
        action="append",
        default=[],
        help="Additional rector path requiring guide update (repeatable).",
    )
    args = parser.parse_args()

    guide_path = args.guide_path.replace("\\", "/")
    rector_paths = tuple(DEFAULT_RECTOR_PATHS) + tuple(
        path.replace("\\", "/") for path in args.rector_path
    )

    base_ref = resolve_base_ref(args.base_ref)
    changed = changed_files_from_base(base_ref) if base_ref else changed_files_from_worktree()
    if base_ref and not changed:
        changed = changed_files_from_worktree()

    if not changed:
        print("OK: no changed files detected for architecture guide sync check.")
        return 0

    rector_hits = sorted(path for path in changed if is_rector_path(path, rector_paths))
    if not rector_hits:
        print("OK: no rector architecture changes detected.")
        return 0

    if guide_path in changed:
        print("OK: rector architecture changes detected and AI architecture guide was updated.")
        return 0

    print("Architecture rector changes detected without guide update:")
    for hit in rector_hits:
        print(f"- {hit}")
    print("")
    print(f"Required: update `{guide_path}` in the same change set.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
