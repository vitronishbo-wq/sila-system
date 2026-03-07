#!/usr/bin/env python3
"""Architecture health audit for backend modules."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


ILLEGAL_IMPORT_PATTERN = re.compile(r"from app\.modules\.([a-zA-Z0-9_]+)")


def count_lines(file_path: Path) -> int:
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)


def scan_file_for_imports(file_path: Path, current_module: str, report: dict[str, list[str]]) -> None:
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    matches = ILLEGAL_IMPORT_PATTERN.findall(content)
    for target in matches:
        if target != current_module:
            report["illegal_imports"].append(f"{file_path} -> imports module '{target}'")


def scan_module(module_path: Path, module_name: str, max_file_lines: int, report: dict[str, list[str]]) -> None:
    report["modules"].append(module_name)

    router = module_path / "api" / "router.py"
    tests = module_path / "tests"
    domain = module_path / "domain"

    if not router.exists():
        report["missing_router"].append(module_name)
    if not tests.exists():
        report["missing_tests"].append(module_name)
    if not domain.exists():
        report["missing_domain"].append(module_name)

    for root, dirs, files in os.walk(module_path):
        root_path = Path(root)

        for d in dirs:
            if "{" in d or "}" in d:
                report["weird_dirs"].append(str(root_path / d))

        for file_name in files:
            file_path = root_path / file_name
            if not file_name.endswith(".py"):
                continue

            lowered = file_name.lower()
            if "generate" in lowered or "setup" in lowered:
                report["module_scripts"].append(str(file_path))

            lines = count_lines(file_path)
            if lines > max_file_lines:
                report["large_files"].append(f"{file_path} ({lines} lines)")

            scan_file_for_imports(file_path, module_name, report)


def print_section(title: str, items: list[str]) -> None:
    print(title)
    if not items:
        print(" - none")
        return
    for item in items:
        print(f" - {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run architecture audit across modules.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root path",
    )
    parser.add_argument(
        "--max-file-lines",
        type=int,
        default=400,
        help="Flag Python files above this number of lines",
    )
    parser.add_argument(
        "--output-json",
        default="reports/architecture_audit_report.json",
        help="JSON output path",
    )
    args = parser.parse_args()

    base_path = Path(args.modules_root)
    if not base_path.exists():
        print(f"Modules directory not found: {base_path}")
        return 2

    report: dict[str, list[str]] = {
        "modules": [],
        "missing_router": [],
        "missing_tests": [],
        "missing_domain": [],
        "api_style_nonstandard": [],
        "illegal_imports": [],
        "large_files": [],
        "module_scripts": [],
        "weird_dirs": [],
    }

    modules = sorted([p for p in base_path.iterdir() if p.is_dir() and p.name != "__pycache__"])
    for module in modules:
        scan_module(module, module.name, args.max_file_lines, report)

        api_dir = module / "api"
        has_style_a = (
            (api_dir / "router.py").exists()
            and (api_dir / "endpoints").exists()
            and (api_dir / "schemas").exists()
            and (api_dir / "deps.py").exists()
        )
        has_style_b = (module / "presentation" / "router.py").exists()
        has_style_c = (api_dir.exists() and (api_dir / "router.py").exists() and not (api_dir / "endpoints").exists())
        if not has_style_a:
            style = "unknown"
            if has_style_b:
                style = "presentation"
            elif has_style_c:
                style = "flat_api"
            elif (api_dir / "router.py").exists():
                style = "partial_api"
            report["api_style_nonstandard"].append(f"{module.name}: {style}")

    print("====================================")
    print("ARCHITECTURE AUDIT REPORT")
    print("====================================")
    print(f"Total Modules: {len(report['modules'])}")
    print_section("\nModules missing router:", report["missing_router"])
    print_section("\nModules missing tests:", report["missing_tests"])
    print_section("\nModules missing domain:", report["missing_domain"])
    print_section("\nModules with non-standard API style:", report["api_style_nonstandard"])
    print_section("\nIllegal imports between modules:", report["illegal_imports"])
    print_section("\nLarge files (> max-file-lines):", report["large_files"])
    print_section("\nScripts inside modules:", report["module_scripts"])
    print_section("\nWeird directories:", report["weird_dirs"])
    print("\nAudit completed.")

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"JSON report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
