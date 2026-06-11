#!/usr/bin/env python3
"""
scripts/seed_dev_data.py

Create development data files from `docs/DEV_CREDENTIALS.md`.
This script enforces a single universal password for all generated users.

Usage:
  python3 scripts/seed_dev_data.py --dry-run
  python3 scripts/seed_dev_data.py           # write files
  python3 scripts/seed_dev_data.py --force   # overwrite existing files

WARNING: These files and the password are ONLY for development/homologation
and MUST NOT be used in production.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict

# Hardcoded universal password for development/homologation (intentional)
UNIVERSAL_PASSWORD = "Sila_1983"

DOC_PATH = Path("docs/DEV_CREDENTIALS.md")
OUT_DIR = Path("data/dev")


def parse_dev_credentials(md_path: Path) -> List[Dict]:
    users: List[Dict] = []
    if not md_path.exists():
        return users
    with md_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue
            username = parts[0]
            role = parts[1]
            # Only accept entries that look like emails
            if "@" not in username:
                continue
            users.append({
                "username": username,
                "email": username,
                "role": role,
                "password": UNIVERSAL_PASSWORD,
            })
    return users


def derive_institutions(users: List[Dict]) -> List[Dict]:
    inst_map: Dict[str, Dict] = {}
    for u in users:
        email = u["email"]
        local = email.split("@")[0]
        inst_id = local
        if inst_id not in inst_map:
            inst_map[inst_id] = {
                "id": inst_id,
                "name": inst_id.replace(".", " ").upper(),
                "domain": email.split("@", 1)[1],
                "contacts": [email],
            }
        else:
            if email not in inst_map[inst_id]["contacts"]:
                inst_map[inst_id]["contacts"].append(email)
    return list(inst_map.values())


def write_json(path: Path, data, force: bool = False, dry_run: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force and not dry_run:
        print(f"[SKIP] {path} exists (use --force to overwrite)")
        return False
    if dry_run:
        print(f"[DRY] Would write {path} (items={len(data) if hasattr(data, '__len__') else 'n/a'})")
        return True
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print(f"[CREATED] {path}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed development data (single universal password)")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; show actions")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--out-dir", default=str(OUT_DIR), help="Output directory")
    args = parser.parse_args()

    users = parse_dev_credentials(DOC_PATH)
    institutions = derive_institutions(users)

    outdir = Path(args.out_dir)
    creds = {
        "universal_password": UNIVERSAL_PASSWORD,
        "note": "ONLY FOR DEVELOPMENT/HOMOLOGATION. Never use in production.",
    }

    write_json(outdir / "users.json", users, force=args.force, dry_run=args.dry_run)
    write_json(outdir / "institutions.json", institutions, force=args.force, dry_run=args.dry_run)
    write_json(outdir / "credentials.json", creds, force=args.force, dry_run=args.dry_run)

    print(f"Summary: users={len(users)} institutions={len(institutions)} out={outdir}")


if __name__ == "__main__":
    main()
