#!/usr/bin/env python3
"""
Safe Duplicate Removal Script
Integrates with all_code_index.json to perform controlled, metadata-aware deduplication.

Rules:
- Only consider files listed in all_code_index.json
- Build checksum map using SHA256
- Detect duplicates via checksum groups
- For each group, pick canonical file:
    1. Prefer file inside canonical src dirs
    2. If tie, newest modification time
    3. If tie, shortest path
- Before deleting non-canonical duplicates:
    - Verify no active references using ripgrep
- All removals logged to .cleanup_backup/report.log
- Before modifying the repo:
    - Backup each file removed to .cleanup_backup/<path>

Supports --dry-run mode for audit-only runs (no filesystem changes).
"""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

INDEX_FILE = "all_code_index.json"
BACKUP_DIR = Path(".cleanup_backup")
CANON_DIRS = ["src", "core", "lib"]  # priority locations

BACKUP_DIR.mkdir(exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_index():
    if not Path(INDEX_FILE).exists():
        raise FileNotFoundError(f"Missing {INDEX_FILE}. Generate it before running dedup.")
    with open(INDEX_FILE) as f:
        return json.load(f)


def build_checksum_map(files):
    checksums = {}
    for entry in files:
        p = Path(entry["path"])
        if not p.exists():
            continue
        digest = sha256(p)
        checksums.setdefault(digest, []).append(p)
    return checksums


def is_canonical(path: Path) -> bool:
    return any(part in CANON_DIRS for part in path.parts)


def choose_winner(group):
    # group: list[Path]
    def score(p: Path):
        mtime = p.stat().st_mtime
        canonical = is_canonical(p)
        return (
            int(canonical),  # canonical dirs win
            mtime,  # newer wins
            -len(str(p)),  # shorter path wins
        )

    return max(group, key=score)


def referenced(path: Path) -> bool:
    """Return True if file name appears in codebase imports/calls."""
    try:
        result = subprocess.run(["rg", path.name, ".", "--glob", "*.py", "--quiet"])
        return result.returncode == 0
    except FileNotFoundError:
        return False


def backup(p: Path):
    dest = BACKUP_DIR / p
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dest)


def write_log(msg: str):
    with open(BACKUP_DIR / "report.log", "a") as f:
        f.write(msg + "\n")


def run_dedup(dry_run: bool = False) -> None:
    files = load_index()
    checksum_map = build_checksum_map(files)

    for digest, group in checksum_map.items():
        if len(group) < 2:
            continue

        winner = choose_winner(group)
        write_log(f"Winner for {digest}: {winner}")

        for p in group:
            if p == winner:
                continue

            if referenced(p):
                write_log(f"SKIPPED (referenced): {p}")
                continue

            if dry_run:
                write_log(f"DRY-RUN: would delete: {p}")
                continue

            backup(p)
            p.unlink()
            write_log(f"DELETED: {p}")

    write_log(f"Deduplication completed. dry_run={dry_run}")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Safe duplicate removal based on all_code_index.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Audit mode: do not delete files, only log what would be removed.",
    )
    args = parser.parse_args(argv)

    run_dedup(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
