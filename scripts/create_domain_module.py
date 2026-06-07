#!/usr/bin/env python3
"""Scaffold a bounded module and auto-register it in AI_ARCHITECTURE_GRAPH.yaml."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

VALID_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


def ensure_structure(module_root: Path) -> None:
    dirs = [
        "api",
        "application/services",
        "application/ports",
        "domain/models",
        "domain/entities",
        "domain/value_objects",
        "infrastructure/repositories",
        "infrastructure/adapters",
    ]
    for item in dirs:
        path = module_root / item
        path.mkdir(parents=True, exist_ok=True)

    for item in ["", "api", "application", "domain", "infrastructure"]:
        init_path = module_root / item / "__init__.py" if item else module_root / "__init__.py"
        init_path.touch(exist_ok=True)

    architecture_doc = module_root / "ARCHITECTURE.md"
    if not architecture_doc.exists():
        architecture_doc.write_text(
            "\n".join(
                [
                    f"# {module_root.name} Architecture",
                    "",
                    "- Bounded context module scaffolded by `scripts/create_domain_module.py`.",
                    "- Fill responsibilities, contracts, and integration boundaries here.",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def register_in_graph(graph_path: Path, macro_domain: str, module_name: str) -> None:
    payload = yaml.safe_load(graph_path.read_text(encoding="utf-8")) if graph_path.exists() else {}
    if not isinstance(payload, dict):
        payload = {}

    modules = payload.setdefault("modules", {})
    if not isinstance(modules, dict):
        modules = {}
        payload["modules"] = modules

    entry = modules.get(macro_domain)
    if not isinstance(entry, dict):
        entry = {
            "path": f"apps/backend/app/modules/{macro_domain}",
            "domain_group": macro_domain,
            "layered_architecture": True,
            "entities": [],
            "use_cases": [],
            "api": [],
            "depends_on": [],
        }
        modules[macro_domain] = entry

    submodules = entry.setdefault("submodules", [])
    if not isinstance(submodules, list):
        submodules = []
        entry["submodules"] = submodules
    if module_name not in submodules:
        submodules.append(module_name)
        submodules.sort()

    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8"
    )


def normalize_value(value: str | None, prompt: str) -> str:
    if value:
        candidate = value.strip().lower()
    else:
        candidate = input(prompt).strip().lower()
    if not VALID_NAME.fullmatch(candidate):
        raise SystemExit(
            f"Invalid name '{candidate}'. Use snake_case starting with a letter (e.g. pesca_artesanal)."
        )
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a domain module scaffold.")
    parser.add_argument("--module-name", help="New module name (snake_case).")
    parser.add_argument(
        "--macro-domain", help="Macro domain folder under apps/backend/app/modules."
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root path.",
    )
    parser.add_argument(
        "--graph-yaml",
        default="docs/AI_ARCHITECTURE_GRAPH.yaml",
        help="Architecture graph file to auto-register module.",
    )
    args = parser.parse_args()

    module_name = normalize_value(args.module_name, "Module name (snake_case): ")
    macro_domain = normalize_value(args.macro_domain, "Macro-domain (snake_case): ")

    modules_root = Path(args.modules_root).resolve()
    macro_root = modules_root / macro_domain
    module_root = macro_root / module_name
    ensure_structure(module_root)

    graph_yaml = Path(args.graph_yaml).resolve()
    register_in_graph(graph_yaml, macro_domain=macro_domain, module_name=module_name)

    print(f"Created module scaffold: {module_root}")
    print(f"Updated architecture graph: {graph_yaml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
