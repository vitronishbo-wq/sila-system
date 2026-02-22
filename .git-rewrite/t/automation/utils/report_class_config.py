#!/usr/bin/env python3
"""
Scan repository for `class Config` blocks and report Pydantic-related usages.

Excludes common virtualenv and git dirs. Prints a detailed report with file,
line number, the Config block, and flags indicating if it contains
pydantic-style entries like `orm_mode`.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path("/opt/sila-system")
SKIP_DIRS = {"venv", ".venv", "node_modules", ".git", "__pycache__"}
RE_CONFIG_BLOCK = re.compile(
    r"(^[ \t]*)class\s+Config\s*:\s*\n((?:^[ \t]+.*\n)+)", re.MULTILINE
)
FLAGS = [
    "orm_mode",
    "from_attributes",
    "allow_population_by_field_name",
    "alias_generator",
    "validate_assignment",
    "extra",
    "use_enum_values",
]


def should_skip(path: Path) -> bool:
    parts = set(p.name for p in path.resolve().parts)
    return bool(parts & SKIP_DIRS)


def scan_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    results = []
    for m in RE_CONFIG_BLOCK.finditer(text):
        indent = m.group(1)
        body = m.group(2)
        # compute line number
        start_pos = m.start(0)
        lineno = text.count("\n", 0, start_pos) + 1
        body_lines = body.splitlines()
        flags_found = [f for f in FLAGS if any(f in ln for ln in body_lines)]
        results.append(
            {
                "lineno": lineno,
                "indent": indent,
                "body": body,
                "flags": flags_found,
                "snippet": "\n".join(body_lines[:10]),
            }
        )
    return results


def main():
    report = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune skip dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            fpath = Path(dirpath) / fn
            rel = fpath.relative_to(ROOT)
            items = scan_file(fpath)
            if items:
                report.append((str(rel), items))

    if not report:
        print("No class Config blocks found.")
        return

    total = sum(len(items) for _, items in report)
    print(f"Found {total} `class Config` block(s) in {len(report)} file(s)")
    print("-" * 80)
    for rel, items in report:
        print(f"File: {rel}")
        for it in items:
            print(f'  Line: {it["lineno"]}  Flags: {it["flags"]}')
            print("  --- Config block snippet:")
            for ln in it["body"].splitlines():
                print("   ", ln)
            # Suggestion
            if "orm_mode" in it["flags"]:
                print(
                    "  Suggestion: replace with `model_config = ConfigDict(orm_mode=True)` and ensure `from pydantic import ConfigDict` is imported"
                )
            elif it["flags"]:
                print(
                    "  Suggestion: review other Config attributes and map to ConfigDict where appropriate"
                )
            else:
                print(
                    "  Suggestion: review this Config block; may not be pydantic-related or may require manual migration"
                )
            print()
        print("-" * 80)


if __name__ == "__main__":
    main()
