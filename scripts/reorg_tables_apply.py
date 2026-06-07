#!/usr/bin/env python3
"""
reorg_tables_apply.py

Detecta __tablename__ em módulos e aplica uma normalização automática:
    new_table_name = <module_name>_<orig_table_name_cleaned>

Cria backups (.orig) e um relatório JSON (reorg_report.json).

USO:
    python3 reorg_tables_apply.py --modules apps/backend/modules --apply
    (ou sem --apply para só gerar relatório e mapping)
"""

import argparse
import json
import os
import re
from pathlib import Path

TAB_RE = re.compile(r'__tablename__\s*=\s*["\']([^"\']+)["\']')


def module_name_from_path(path: Path, modules_root: Path) -> str:
    try:
        rel = path.relative_to(modules_root)
        parts = rel.parts
        return parts[0] if parts else "unknown"
    except Exception:
        return "unknown"


def clean_table_name(name: str) -> str:
    s = name.strip().replace(" ", "_").lower()
    return re.sub(r"[^a-z0-9_]", "", s)


def suggest_new_name(module: str, orig: str) -> str:
    orig_c = clean_table_name(orig)
    if orig_c.startswith(f"{module}_"):
        return orig_c
    return f"{module}_{orig_c}"


def process_file(path: Path, modules_root: Path, apply: bool = False):
    text = path.read_text(encoding="utf-8")
    matches = list(TAB_RE.finditer(text))
    if not matches:
        return []

    module = module_name_from_path(path, modules_root)
    changes = []
    new_text = text
    for m in reversed(matches):
        orig = m.group(1)
        new = suggest_new_name(module, orig)
        start, end = m.span(1)
        new_text = new_text[:start] + new + new_text[end:]
        changes.append(
            {
                "file": str(path),
                "module": module,
                "orig": orig,
                "suggested": new,
            }
        )
    if apply and changes:
        orig_path = path.with_suffix(path.suffix + ".orig")
        if not orig_path.exists():
            path.rename(orig_path)
            orig_path.write_text(text, encoding="utf-8")
            path.write_text(new_text, encoding="utf-8")
        else:
            bak = path.with_suffix(path.suffix + f".bak_{int(os.times()[4])}")
            bak.write_text(text, encoding="utf-8")
            path.write_text(new_text, encoding="utf-8")
    return changes


def walk_and_process(modules_root: Path, apply: bool = False):
    report = []
    for py in modules_root.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        changes = process_file(py, modules_root, apply=apply)
        if changes:
            report.extend(changes)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", required=True, help="Path to modules dir")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    args = parser.parse_args()
    modules_root = Path(args.modules).resolve()
    if not modules_root.exists():
        print("Modules root does not exist:", modules_root)
        return

    print("Scanning modules at:", modules_root)
    report = walk_and_process(modules_root, apply=args.apply)
    out = {
        "modules_root": str(modules_root),
        "applied": bool(args.apply),
        "count": len(report),
        "entries": report,
    }
    out_path = Path.cwd() / "reorg_report.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report written to {out_path} — items: {len(report)}")
    if report:
        for r in report:
            print(f"{r['file']}: {r['orig']} -> {r['suggested']}")
    else:
        print("No __tablename__ patterns found.")


if __name__ == "__main__":
    main()
