#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
DEFAULT_LEGACY_ROOT = DEFAULT_BACKEND_ROOT / "modules"
DEFAULT_TARGET_ROOT = DEFAULT_BACKEND_ROOT / "app" / "domain"

DEFAULT_MAPPING: dict[str, str] = {
    "education": "academic",
    "educacao": "academic",
    "finance": "finance",
    "financas": "finance",
    "civil_identity": "identity",
    "identidade_civil": "identity",
    "notifications": "notifications",
}

DEFAULT_EXCLUDES = [
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
]


@dataclass
class MigrationResult:
    source: Path
    target: Path
    copied_files: int = 0
    skipped_files: int = 0
    overwritten_files: int = 0
    conflicts: int = 0
    source_missing: bool = False
    source_removed: bool = False


def parse_mapping(raw_pairs: list[str]) -> dict[str, str]:
    mapping = dict(DEFAULT_MAPPING)
    for pair in raw_pairs:
        if ":" not in pair:
            raise ValueError(f"Invalid --map value '{pair}'. Expected old:new.")
        old_name, new_name = pair.split(":", 1)
        old_name = old_name.strip()
        new_name = new_name.strip()
        if not old_name or not new_name:
            raise ValueError(f"Invalid --map value '{pair}'. Empty side detected.")
        mapping[old_name] = new_name
    return mapping


def should_exclude(path: Path, patterns: list[str]) -> bool:
    for part in path.parts:
        for pattern in patterns:
            if fnmatch.fnmatch(part, pattern):
                return True
    return False


def copy_module(
    *,
    source_module_dir: Path,
    target_domain_dir: Path,
    excludes: list[str],
    overwrite: bool,
    dry_run: bool,
) -> MigrationResult:
    result = MigrationResult(source=source_module_dir, target=target_domain_dir)
    if not source_module_dir.exists():
        result.source_missing = True
        return result

    source_files = sorted(p for p in source_module_dir.rglob("*") if p.is_file())
    for src_file in source_files:
        rel_path = src_file.relative_to(source_module_dir)
        if should_exclude(rel_path, excludes):
            result.skipped_files += 1
            continue

        dst_file = target_domain_dir / rel_path
        if dst_file.exists() and not overwrite:
            result.conflicts += 1
            continue

        if dst_file.exists() and overwrite:
            result.overwritten_files += 1
        else:
            result.copied_files += 1

        if dry_run:
            continue

        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)

    return result


def remove_source(path: Path, *, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    shutil.rmtree(path, ignore_errors=True)
    return True


def cleanup_empty_dirs(root: Path, *, dry_run: bool) -> int:
    removed = 0
    if not root.exists():
        return removed

    # Remove children first.
    for directory in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        try:
            if any(directory.iterdir()):
                continue
            removed += 1
            if not dry_run:
                directory.rmdir()
        except OSError:
            continue
    return removed


def print_summary(results: list[MigrationResult], *, removed_empty_dirs: int, dry_run: bool) -> None:
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"[MODE] {mode}")
    print("[SUMMARY] Legacy module migration")

    total_copied = 0
    total_overwritten = 0
    total_skipped = 0
    total_conflicts = 0

    for res in results:
        source_name = res.source.name
        target_name = res.target.name
        if res.source_missing:
            print(f" - {source_name} -> {target_name}: source missing")
            continue

        total_copied += res.copied_files
        total_overwritten += res.overwritten_files
        total_skipped += res.skipped_files
        total_conflicts += res.conflicts

        removed_label = "yes" if res.source_removed else "no"
        print(
            f" - {source_name} -> {target_name}: "
            f"copied={res.copied_files}, overwritten={res.overwritten_files}, "
            f"skipped={res.skipped_files}, conflicts={res.conflicts}, source_removed={removed_label}"
        )

    print(
        "[TOTAL] "
        f"copied={total_copied}, overwritten={total_overwritten}, "
        f"skipped={total_skipped}, conflicts={total_conflicts}, "
        f"empty_dirs_removed={removed_empty_dirs}"
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Migrate legacy modules into app/domain namespaces.",
    )
    parser.add_argument(
        "--legacy-root",
        type=Path,
        default=DEFAULT_LEGACY_ROOT,
        help=f"Legacy modules root (default: {DEFAULT_LEGACY_ROOT})",
    )
    parser.add_argument(
        "--target-root",
        type=Path,
        default=DEFAULT_TARGET_ROOT,
        help=f"Target domain root (default: {DEFAULT_TARGET_ROOT})",
    )
    parser.add_argument(
        "--map",
        action="append",
        default=[],
        metavar="OLD:NEW",
        help="Add or override mapping pair (repeatable).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Exclude path pattern (repeatable).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination files on conflict.",
    )
    parser.add_argument(
        "--prune-source",
        action="store_true",
        help="Remove migrated source module directories.",
    )
    parser.add_argument(
        "--cleanup-empty-dirs",
        action="store_true",
        help="Remove empty directories under legacy root after migration.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    mapping = parse_mapping(args.map)
    excludes = list(dict.fromkeys([*DEFAULT_EXCLUDES, *args.exclude]))

    results: list[MigrationResult] = []
    for old_name, new_name in mapping.items():
        source = args.legacy_root / old_name
        target = args.target_root / new_name
        result = copy_module(
            source_module_dir=source,
            target_domain_dir=target,
            excludes=excludes,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
        if args.prune_source and not result.source_missing:
            result.source_removed = remove_source(source, dry_run=args.dry_run)
        results.append(result)

    removed_empty_dirs = 0
    if args.cleanup_empty_dirs:
        removed_empty_dirs = cleanup_empty_dirs(args.legacy_root, dry_run=args.dry_run)

    print_summary(results, removed_empty_dirs=removed_empty_dirs, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
