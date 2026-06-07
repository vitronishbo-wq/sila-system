"""Scan repo for occurrences of well-known policy defaults and report candidates
for migration to `foundation.policies`.

This script is intentionally read-only and conservative: it reports candidate files
and lines but does not modify code. Use --apply in future iterations to perform
automated replacements after manual review.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[2]

POLICY_MARKERS = {
    "MAX_TRANSFER_DISTANCE": r"\b50\b",
    "MAX_PENDING_DEBT": r"\b0\b",
    "TRANSFER_WINDOWS": r"TRANSFER_WINDOWS",
    "GRADE_COMPATIBILITY": r"GRADE_COMPATIBILITY",
}


def scan_paths(paths: List[Path]) -> dict:
    findings = {}
    for p in paths:
        if not p.exists():
            continue
        for f in p.rglob("*.py"):
            try:
                txt = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for policy, pattern in POLICY_MARKERS.items():
                for m in re.finditer(pattern, txt):
                    findings.setdefault(policy, []).append({
                        "file": str(f.relative_to(ROOT)),
                        "line": txt.count("\n", 0, m.start()) + 1,
                        "snippet": txt[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")[:200],
                    })
    return findings


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--roots", nargs="*", default=["domain", "foundation", "apps"], help="Folders to scan (relative to repo root)")
    p.add_argument("--out", default="data/policy_scan_report.json")
    args = p.parse_args(argv)
    roots = [ROOT / r for r in args.roots]
    report = scan_paths(roots)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote report to {args.out}")


if __name__ == "__main__":
    main()
