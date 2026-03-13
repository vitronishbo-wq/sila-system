#!/usr/bin/env python3
"""Generate context map documentation from dependency graph artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_graph(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Dependency graph not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def render_context_map(graph: dict) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    edges = [
        (item.get("source"), item.get("target"), int(item.get("weight", 1)))
        for item in graph.get("edges", [])
        if item.get("source") and item.get("target") and item.get("source") != item.get("target")
    ]
    edges.sort(key=lambda row: row[2], reverse=True)
    modules = sorted({src for src, _, _ in edges} | {tgt for _, tgt, _ in edges})
    cycles = [cycle for cycle in graph.get("cycles", []) if isinstance(cycle, list)]

    lines: list[str] = []
    lines.append("# Context Map")
    lines.append("")
    lines.append(f"- Generated at: `{generated_at}`")
    lines.append(f"- Modules in map: **{len(modules)}**")
    lines.append(f"- Cross-context edges: **{len(edges)}**")
    lines.append(f"- Circular groups: **{len(cycles)}**")
    lines.append("")

    lines.append("## Relations")
    lines.append("")
    if not edges:
        lines.append("- No cross-context dependencies detected.")
    else:
        lines.append("| Source | Target | Weight |")
        lines.append("| --- | --- | ---: |")
        for source, target, weight in edges:
            lines.append(f"| `{source}` | `{target}` | {weight} |")
    lines.append("")

    lines.append("## Mermaid")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    if not edges:
        lines.append("  A[\"No edges\"]")
    else:
        for source, target, weight in edges:
            lines.append(f"  {source} -->|{weight}| {target}")
    lines.append("```")
    lines.append("")

    lines.append("## Circular Dependencies")
    lines.append("")
    if not cycles:
        lines.append("- None.")
    else:
        for cycle in cycles:
            lines.append("- " + " -> ".join(f"`{node}`" for node in cycle))
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate context_map.md from dependency graph.")
    parser.add_argument(
        "--graph-json",
        default="reports/module_dependency_graph.json",
        help="Dependency graph JSON source.",
    )
    parser.add_argument(
        "--output",
        default="docs/architecture/context_map.md",
        help="Output Markdown file.",
    )
    args = parser.parse_args()

    graph = load_graph(Path(args.graph_json))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_context_map(graph), encoding="utf-8")
    print(f"Generated: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
