#!/usr/bin/env python3
"""AI scan scope filter for large monorepos.

Supports two policy styles in AI_FILE_SCOPE.yaml:
- `include` glob patterns (recommended)
- `scan_roots` directory roots (legacy compatibility)
"""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_SCOPE_FILE = ".ai/AI_FILE_SCOPE.yaml"


def _parse_list_lines(lines: list[str], key: str) -> list[str]:
    values: list[str] = []
    in_key = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            in_key = line[:-1] == key
            continue
        if in_key and line.lstrip().startswith("- "):
            values.append(line.split("- ", 1)[1].strip())
        elif in_key and not line.startswith(" "):
            in_key = False
    return values


def _parse_int(lines: list[str], key: str, default: int) -> int:
    for raw in lines:
        line = raw.strip()
        if line.startswith(f"{key}:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return default
    return default


def load_policy(scope_file: Path) -> dict[str, object]:
    text = scope_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    include = _parse_list_lines(lines, "include")
    exclude_dirs = _parse_list_lines(lines, "exclude_dirs")
    ignore_dirs = _parse_list_lines(lines, "ignore_dirs")
    return {
        "include": include,
        "scan_roots": _parse_list_lines(lines, "scan_roots"),
        "ignore_dirs": set(exclude_dirs or ignore_dirs),
        "max_file_size_kb": _parse_int(lines, "max_file_size_kb", 200),
        "max_lines": _parse_int(lines, "max_lines", 800),
    }


def should_scan_file(
    path: Path, ignore_dirs: set[str], max_file_size_kb: int, max_lines: int
) -> bool:
    if any(part in ignore_dirs for part in path.parts):
        return False
    if not path.is_file():
        return False

    try:
        size_kb = path.stat().st_size / 1024
        if size_kb > max_file_size_kb:
            return False
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for idx, _ in enumerate(fh, start=1):
                if idx > max_lines:
                    return False
    except OSError:
        return False

    return True


def _iter_candidates_from_include(repo_root: Path, include_patterns: list[str]):
    seen: set[Path] = set()
    for pattern in include_patterns:
        for match in repo_root.glob(pattern):
            if match.is_dir():
                for nested in match.rglob("*"):
                    if nested in seen:
                        continue
                    seen.add(nested)
                    yield nested
            else:
                if match in seen:
                    continue
                seen.add(match)
                yield match


def iter_scannable_paths(repo_root: Path, policy: dict[str, object]):
    include_patterns = policy.get("include", [])
    scan_roots = [repo_root / p for p in policy["scan_roots"]]
    ignore_dirs = policy["ignore_dirs"]
    max_file_size_kb = int(policy["max_file_size_kb"])
    max_lines = int(policy["max_lines"])

    if include_patterns:
        for path in _iter_candidates_from_include(repo_root, include_patterns):
            if should_scan_file(path, ignore_dirs, max_file_size_kb, max_lines):
                yield path
        return

    for root in scan_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if should_scan_file(path, ignore_dirs, max_file_size_kb, max_lines):
                yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter repo files for AI-safe scanning.")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--scope-file", default=DEFAULT_SCOPE_FILE, help="Path to AI scope yaml")
    parser.add_argument("--print-count", action="store_true", help="Print only count")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    scope_file = (repo_root / args.scope_file).resolve()
    if not scope_file.exists():
        print(f"Scope file not found: {scope_file}")
        return 2

    policy = load_policy(scope_file)
    files = sorted(iter_scannable_paths(repo_root, policy))

    if args.print_count:
        print(len(files))
        return 0

    for file_path in files:
        print(file_path.relative_to(repo_root))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
