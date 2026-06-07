#!/usr/bin/env python3
"""Generate AI architecture graph from module ARCHITECTURE.md files."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from apps.backend.app.core.module_registry import iter_modules  # noqa: E402
from architecture.generate_architecture_index import dump_yaml  # noqa: E402


def relpath(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def parse_sectioned_lists(doc_text: str) -> dict[str, list[str]]:
    section_map = {
        "## Key Entities": "entities",
        "## Use Cases": "use_cases",
        "## Public API": "api",
        "## Dependencies": "depends_on",
    }
    parsed: dict[str, list[str]] = {value: [] for value in section_map.values()}
    current: str | None = None

    for raw in doc_text.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line in section_map:
            current = section_map[line]
            continue
        if line.startswith("## "):
            current = None
            continue
        if current and line.startswith("- "):
            item = line[2:].strip()
            if item and "Nenhum" not in item and "Sem dependencias" not in item:
                parsed[current].append(item)

    for key, values in parsed.items():
        parsed[key] = sorted({value for value in values if value})
    return parsed


def load_module_doc(module_dir: Path) -> tuple[dict[str, list[str]], bool]:
    doc_file = module_dir / "ARCHITECTURE.md"
    if not doc_file.exists():
        return {"entities": [], "use_cases": [], "api": [], "depends_on": []}, False
    try:
        text = doc_file.read_text(encoding="utf-8")
    except OSError:
        return {"entities": [], "use_cases": [], "api": [], "depends_on": []}, False
    return parse_sectioned_lists(text), True


def has_layered_architecture(module_dir: Path) -> bool:
    required = ("domain", "application", "infrastructure", "api")
    return all((module_dir / part).exists() for part in required)


def build_graph_payload(
    system_name: str, modules_root: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    module_map: dict[str, Any] = {}
    edges: list[dict[str, str]] = []
    missing_docs: list[str] = []

    specs = {spec.name: spec for spec in iter_modules(enabled_only=False)}
    module_names = sorted(
        d.name for d in modules_root.iterdir() if d.is_dir() and not d.name.startswith("__")
    )

    for module_name in module_names:
        module_dir = modules_root / module_name
        spec = specs.get(module_name)
        parsed, present = load_module_doc(module_dir)
        if not present:
            missing_docs.append(module_name)

        depends_on = [
            dep for dep in parsed["depends_on"] if dep in module_names and dep != module_name
        ]
        for dep in depends_on:
            edges.append({"source": module_name, "target": dep})

        module_map[module_name] = {
            "path": relpath(module_dir),
            "domain_group": spec.domain if spec else "unknown",
            "layered_architecture": has_layered_architecture(module_dir),
            "entities": parsed["entities"],
            "use_cases": parsed["use_cases"],
            "api": parsed["api"],
            "depends_on": depends_on,
        }

    yaml_payload = {
        "system": system_name,
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "modules": module_map,
    }
    json_payload = {
        "system": system_name,
        "generated_at": datetime.now(UTC).isoformat(),
        "modules": module_map,
        "edges": edges,
        "missing_architecture_docs": missing_docs,
    }
    return yaml_payload, json_payload


def render_visual_report(json_payload: dict[str, Any], output_path: Path) -> str:
    modules = json_payload.get("modules", {})
    edges = json_payload.get("edges", [])
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")

    with_entities = sum(1 for node in modules.values() if node.get("entities"))
    with_use_cases = sum(1 for node in modules.values() if node.get("use_cases"))
    with_api = sum(1 for node in modules.values() if node.get("api"))
    layered = sum(1 for node in modules.values() if node.get("layered_architecture"))

    lines: list[str] = []
    lines.append("# AI Architecture Graph Visual Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Output: `{output_path.as_posix()}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules in graph: **{len(modules)}**")
    lines.append(f"- Dependency edges: **{len(edges)}**")
    lines.append(f"- Layered architecture compliant: **{layered}**")
    lines.append(f"- Modules with entities: **{with_entities}**")
    lines.append(f"- Modules with use cases: **{with_use_cases}**")
    lines.append(f"- Modules with API routes listed: **{with_api}**")
    lines.append("")
    lines.append("## Edge Table")
    lines.append("")
    lines.append("| Source | Target |")
    lines.append("| --- | --- |")
    for edge in edges[:200]:
        lines.append(f"| `{edge['source']}` | `{edge['target']}` |")
    lines.append("")
    lines.append("## Mermaid Graph (Top 80 Edges)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for edge in edges[:80]:
        lines.append(f"  {edge['source']} --> {edge['target']}")
    if not edges:
        lines.append('  A["No edges"]')
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AI architecture graph.")
    parser.add_argument("--system", default="sila-system", help="System identifier.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root path.",
    )
    parser.add_argument(
        "--yaml-output",
        default="docs/AI_ARCHITECTURE_GRAPH.yaml",
        help="YAML graph output path.",
    )
    parser.add_argument(
        "--json-output",
        default="reports/ai_architecture_graph.json",
        help="JSON graph output path for tooling/guardrails.",
    )
    parser.add_argument(
        "--visual-report-output",
        default="reports/ai_architecture_graph_visual_report.md",
        help="Visual report output path.",
    )
    args = parser.parse_args()

    modules_root = (REPO_ROOT / args.modules_root).resolve()
    yaml_output = (REPO_ROOT / args.yaml_output).resolve()
    json_output = (REPO_ROOT / args.json_output).resolve()
    visual_output = (REPO_ROOT / args.visual_report_output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    yaml_payload, json_payload = build_graph_payload(args.system, modules_root)

    yaml_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    visual_output.parent.mkdir(parents=True, exist_ok=True)

    yaml_output.write_text(dump_yaml(yaml_payload).rstrip() + "\n", encoding="utf-8")
    json_output.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    visual_output.write_text(render_visual_report(json_payload, visual_output), encoding="utf-8")

    print(f"Generated: {yaml_output}")
    print(f"Generated: {json_output}")
    print(f"Generated: {visual_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
