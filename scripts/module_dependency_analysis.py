#!/usr/bin/env python3
"""Generate module dependency graph and Markdown report."""

from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

FROM_IMPORT_RE = re.compile(r"^\s*from\s+app\.(modules|core)\.([A-Za-z0-9_]+)\b")
PLAIN_IMPORT_RE = re.compile(r"^\s*import\s+app\.(modules|core)\.([A-Za-z0-9_]+)\b")


def list_modules(modules_root: Path) -> tuple[str, ...]:
    names = sorted(
        d.name for d in modules_root.iterdir() if d.is_dir() and not d.name.startswith("__")
    )
    return tuple(names)


def _module_parts_from_path(modules_root: Path, py_file: Path) -> list[str]:
    rel = py_file.relative_to(modules_root).with_suffix("")
    parts = ["app", "modules", *rel.parts]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return parts


def _extract_target_module(module_path: str, modules: set[str]) -> str | None:
    if module_path.startswith("apps.backend.app.modules."):
        parts = module_path.split(".")
        if len(parts) >= 3 and parts[2] in modules:
            return parts[2]
        return None
    if module_path.startswith("apps.backend.app.core"):
        return "core"
    return None


def scan_dependencies(
    modules_root: Path,
) -> tuple[dict[str, Counter[str]], dict[str, list[str]], int, int]:
    modules = set(list_modules(modules_root))
    edges: dict[str, Counter[str]] = {name: Counter() for name in modules}
    evidence: dict[str, list[str]] = defaultdict(list)
    files_scanned = 0

    for source_module in sorted(modules):
        source_dir = modules_root / source_module
        for py_file in source_dir.rglob("*.py"):
            rel = py_file.relative_to(modules_root)
            if "__pycache__" in rel.parts or "tests" in rel.parts:
                continue
            try:
                text = py_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            files_scanned += 1
            lines = text.splitlines()
            module_parts = _module_parts_from_path(modules_root, py_file)

            def record_edge(target: str, lineno: int) -> None:
                if not target or target == source_module:
                    return
                if target != "core" and target not in modules:
                    return
                edges[source_module][target] += 1
                edge_key = f"{source_module}->{target}"
                if len(evidence[edge_key]) < 5:
                    line_text = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
                    evidence[edge_key].append(f"{rel}:{lineno} {line_text}")

            try:
                tree = ast.parse(text)
            except SyntaxError:
                for lineno, line in enumerate(lines, start=1):
                    target_module = None
                    if line.lstrip().startswith("from "):
                        match = FROM_IMPORT_RE.match(line)
                        if match:
                            target_module = "core" if match.group(1) == "core" else match.group(2)
                    elif line.lstrip().startswith("import "):
                        match = PLAIN_IMPORT_RE.match(line)
                        if match:
                            target_module = "core" if match.group(1) == "core" else match.group(2)
                    if target_module:
                        record_edge(target_module, lineno)
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        target = _extract_target_module(alias.name, modules)
                        if target:
                            record_edge(target, node.lineno)
                elif isinstance(node, ast.ImportFrom):
                    if node.level > 0:
                        base_parts = (
                            module_parts[: -node.level] if node.level <= len(module_parts) else []
                        )
                        if node.module:
                            base_parts = base_parts + node.module.split(".")
                        if node.module is None:
                            for alias in node.names:
                                candidate = ".".join(base_parts + [alias.name])
                                target = _extract_target_module(candidate, modules)
                                if target:
                                    record_edge(target, node.lineno)
                        else:
                            candidate = ".".join(base_parts)
                            target = _extract_target_module(candidate, modules)
                            if target:
                                record_edge(target, node.lineno)
                    else:
                        if node.module is None:
                            continue
                        target = _extract_target_module(node.module, modules)
                        if target:
                            record_edge(target, node.lineno)

    return edges, evidence, files_scanned, len(modules)


def detect_cycles(edges: dict[str, Counter[str]]) -> list[list[str]]:
    """Tarjan SCC to detect circular dependencies."""
    graph = {node: list(targets.keys()) for node, targets in edges.items()}
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    sccs: list[list[str]] = []

    def strong_connect(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                strong_connect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])

        if lowlinks[node] == indices[node]:
            component: list[str] = []
            while True:
                current = stack.pop()
                on_stack.remove(current)
                component.append(current)
                if current == node:
                    break
            if len(component) > 1:
                sccs.append(sorted(component))

    for node in sorted(graph):
        if node not in indices:
            strong_connect(node)

    sccs.sort(key=lambda item: (len(item), item), reverse=True)
    return sccs


def render_report(
    edges: dict[str, Counter[str]],
    evidence: dict[str, list[str]],
    files_scanned: int,
    modules_scanned: int,
) -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    sorted(edges.keys())
    inbound = Counter()
    edge_rows: list[tuple[str, str, int]] = []

    for source, targets in edges.items():
        for target, weight in targets.items():
            inbound[target] += weight
            edge_rows.append((source, target, weight))

    edge_rows.sort(key=lambda item: item[2], reverse=True)
    cycles = detect_cycles(edges)

    lines: list[str] = []
    lines.append("# Module Dependencies Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append("- Scope: `apps/backend/app/modules`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules scanned: **{modules_scanned}**")
    lines.append(f"- Python files parsed: **{files_scanned}**")
    lines.append(f"- Dependency edges (distinct): **{len(edge_rows)}**")
    lines.append(f"- Circular dependency groups: **{len(cycles)}**")
    lines.append("")

    lines.append("## Top Dependency Edges")
    lines.append("")
    if edge_rows:
        lines.append("| Source | Target | Import count |")
        lines.append("| --- | --- | ---: |")
        for source, target, weight in edge_rows[:50]:
            lines.append(f"| `{source}` | `{target}` | {weight} |")
    else:
        lines.append("- No cross-module imports detected.")
    lines.append("")

    lines.append("## Hotspots")
    lines.append("")
    out_hotspots = sorted(
        ((name, sum(targets.values()), len(targets)) for name, targets in edges.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    in_hotspots = inbound.most_common(30)

    lines.append("### Outbound")
    lines.append("")
    lines.append("| Module | Outbound imports | Distinct targets |")
    lines.append("| --- | ---: | ---: |")
    for name, count, distinct in out_hotspots[:30]:
        lines.append(f"| `{name}` | {count} | {distinct} |")
    lines.append("")

    lines.append("### Inbound")
    lines.append("")
    lines.append("| Module | Inbound imports |")
    lines.append("| --- | ---: |")
    for name, count in in_hotspots:
        lines.append(f"| `{name}` | {count} |")
    lines.append("")

    lines.append("## Circular Dependencies")
    lines.append("")
    if cycles:
        for cycle in cycles:
            lines.append(f"- {' -> '.join(f'`{node}`' for node in cycle)}")
    else:
        lines.append("- No circular dependency groups detected.")
    lines.append("")

    lines.append("## Dependency Graph (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for source, target, weight in edge_rows[:120]:
        lines.append(f"  {source} -->|{weight}| {target}")
    lines.append("```")
    lines.append("")

    lines.append("## Evidence Samples")
    lines.append("")
    for source, target, _weight in edge_rows[:30]:
        key = f"{source}->{target}"
        if key not in evidence:
            continue
        lines.append(f"### `{source}` -> `{target}`")
        lines.append("")
        for sample in evidence[key]:
            lines.append(f"- `{sample}`")
        lines.append("")

    return "\n".join(lines)


def to_json_payload(
    edges: dict[str, Counter[str]], files_scanned: int, modules_scanned: int
) -> dict:
    sorted(edges.keys())
    edge_list = []
    for source, targets in edges.items():
        for target, weight in targets.items():
            edge_list.append({"source": source, "target": target, "weight": weight})
    edge_list.sort(key=lambda item: item["weight"], reverse=True)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "modules_scanned": modules_scanned,
        "files_scanned": files_scanned,
        "edges": edge_list,
        "cycles": detect_cycles(edges),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate module dependency reports.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root.",
    )
    parser.add_argument(
        "--output-md",
        default="reports/module_dependencies.md",
        help="Path to markdown report output.",
    )
    parser.add_argument(
        "--output-json",
        default="reports/module_dependency_graph.json",
        help="Path to dependency graph JSON output.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root).resolve()
    output_md = Path(args.output_md).resolve()
    output_json = Path(args.output_json).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    edges, evidence, files_scanned, modules_scanned = scan_dependencies(modules_root)

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        render_report(edges, evidence, files_scanned, modules_scanned),
        encoding="utf-8",
    )
    output_json.write_text(
        json.dumps(
            to_json_payload(edges, files_scanned, modules_scanned),
            indent=2,
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )

    print(f"Generated: {output_md}")
    print(f"Generated: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
