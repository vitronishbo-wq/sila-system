#!/usr/bin/env python3
"""Check seeds for hardcoded users below national level.

Scans common seed/script folders and reports any occurrences of emails
or role names that indicate hardcoded provincial/municipal users.

Usage:
    python3 scripts/ci/check_no_hardcoded_users.py

Exit code: 0 if OK, 2 if violations found.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[2]

# Files/directories to scan (relative to repo root)
# Scan only canonical seed entry points to enforce bootstrap policy.
SCAN_PATHS = [
    "apps/backend/seeds/run_master_seed.py",
    "apps/backend/scripts/seed_all_users.py",
    "apps/backend/scripts/init-db.sql",
]

# Allowed admin emails (seed canonical super-admins)
ALLOWED_ADMIN_EMAILS = {
    "admin@sila.gov.ao",
    "admin@sila.system",
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@sila\.(gov\.ao|system)")

OFFENDING_ROLE_KEYWORDS = [
    "ADMIN_PROVINCIAL",
    "ADMIN_MUNICIPAL",
    "ADMIN_COMMUNAL",
    "PROVINCIAL",
    "MUNICIPAL",
    "COMMUNAL",
]


def scan_files() -> List[Tuple[Path, int, str]]:
    offenses: List[Tuple[Path, int, str]] = []

    for rel in SCAN_PATHS:
        path = ROOT / rel
        if not path.exists():
            continue
        if path.is_file():
            files = [path]
        else:
            files = [p for p in path.rglob("*.py")] + [p for p in path.rglob("*.sql")] + [p for p in path.rglob("*.md")]

        for f in files:
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for m in EMAIL_RE.finditer(text):
                email = m.group(0)
                if email not in ALLOWED_ADMIN_EMAILS:
                    # Determine line number
                    upto = text[: m.start()].count("\n") + 1
                    offenses.append((f, upto, f"Hardcoded email: {email}"))
            # Role keyword checks (only in seed files)
            for kw in OFFENDING_ROLE_KEYWORDS:
                if kw in text:
                    # Skip if keyword appears in allowed admin context
                    # (e.g., ADMIN_CENTRAL is fine)
                    if kw == "PROVINCIAL" or kw == "MUNICIPAL" or kw == "COMMUNAL":
                        # These words may appear in territory definitions; check nearby 'email' occurrences
                        # We'll flag lines where the keyword appears next to an email-like token
                        for i, line in enumerate(text.splitlines(), start=1):
                            if kw in line and EMAIL_RE.search(line):
                                offenses.append((f, i, f"Role/level keyword with email: {kw} (line)"))
                    else:
                        for i, line in enumerate(text.splitlines(), start=1):
                            if kw in line:
                                offenses.append((f, i, f"Role keyword present: {kw}"))
    return offenses


def main() -> int:
    offenses = scan_files()
    if not offenses:
        print("OK: No hardcoded users found in seeds/scripts (allowed admin only)")
        return 0

    print("ERROR: Found hardcoded user occurrences:\n")
    for f, line, msg in offenses:
        print(f" - {f.relative_to(ROOT)}:{line} -> {msg}")
    print("\nPlease remove hardcoded users below national level or add them only to DEV_CREDENTIALS.md for development.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
