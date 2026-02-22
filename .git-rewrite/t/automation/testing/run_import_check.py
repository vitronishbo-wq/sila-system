#!/usr/bin/env python3
"""Import-check runner for the backend.

Scans Python files for import patterns (`from app.models.*`, `import app.models.*`,
`from modules.*`, `import modules.*`) and attempts to import the referenced modules
inside a controlled environment (adds `backend` to sys.path). Writes a report with
exceptions to `scripts/import_report_<TIMESTAMP>.txt`.

Usage: python3 scripts/run_import_check.py
"""
from __future__ import annotations
import re
import sys
import os
import glob
import importlib
import traceback
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_DIR = os.path.join(ROOT, "scripts")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
REPORT_FILE = os.path.join(REPORT_DIR, f"import_report_{TIMESTAMP}.txt")


def gather_targets() -> list[str]:
    patterns = [
        r"from\s+app\.models\.([A-Za-z0-9_]+)",
        r"import\s+app\.models\.([A-Za-z0-9_]+)",
        r"from\s+modules\.([A-Za-z0-9_]+)",
        r"import\s+modules\.([A-Za-z0-9_]+)",
    ]
    targets = set()
    for py in glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True):
        # skip virtualenv and node_modules
        if (
            "/.venv/" in py
            or "/venv/" in py
            or "/node_modules/" in py
            or "/.git/" in py
        ):
            continue
        try:
            s = open(py, "r", encoding="utf-8").read()
        except Exception:
            continue
        for pat in patterns:
            for m in re.finditer(pat, s):
                targets.add(m.group(0))
                # add module base
                name = m.group(0)
                # extract module-like name
                mod_match = re.search(
                    r"(app\.models\.[A-Za-z0-9_]+|modules\.[A-Za-z0-9_]+)", name
                )
                if mod_match:
                    targets.add(mod_match.group(0))
    # Normalize to module names
    normalized = set()
    for t in targets:
        t = t.strip()
        m = re.search(r"(app\.models\.[A-Za-z0-9_]+|modules\.[A-Za-z0-9_]+)", t)
        if m:
            normalized.add(m.group(0))
    return sorted(normalized)


def try_import(module_name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module_name)
        return True, ""
    except Exception as e:
        tb = traceback.format_exc()
        return False, tb


def main():
    # Add backend to sys.path to simulate running the backend
    backend_path = os.path.join(ROOT, "backend")
    if os.path.isdir(backend_path):
        sys.path.insert(0, backend_path)

    targets = gather_targets()
    results = []
    for mod in targets:
        ok, err = try_import(mod)
        results.append((mod, ok, err))

    # write report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Import check report - {TIMESTAMP}\n")
        f.write(f"Root: {ROOT}\n")
        f.write(f"Backend path used: {backend_path}\n\n")
        total = len(results)
        failed = [r for r in results if not r[1]]
        f.write(f"Total targets checked: {total}\n")
        f.write(f"Failures: {len(failed)}\n\n")
        for mod, ok, err in results:
            f.write("----\n")
            f.write(f"Module: {mod}\n")
            f.write(f"OK: {ok}\n")
            if not ok:
                f.write("Traceback:\n")
                f.write(err)
                f.write("\n")

    print("\nImport-check finished. Report written to:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
