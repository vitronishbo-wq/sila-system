#!/usr/bin/env python3
"""Scan Python imports for module-level circular dependencies."""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from pathlib import Path


def _module_from_file(modules_root: Path, py_file: Path) -> str | None:
    rel = py_file.relative_to(modules_root)
    if len(rel.parts) < 3:
        return None
    return f"{rel.parts[0]}.{rel.parts[1]}"


def _module_from_import(import_name: str) -> str | None:
    parts = import_name.split(".")
    if len(parts) < 4:
        return None
    if parts[0] != "app" or parts[1] != "modules":
        return None
    return f"{parts[2]}.{parts[3]}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect circular dependencies across modules.")
    parser.add_argument("--modules-root", default="apps/backend/app/modules")
    parser.add_argument("--output", default="reports/circular_dependency_scan.md")
    args = parser.parse_args()

    modules_root = Path(args.modules_root)
    output = Path(args.output)

    edges: dict[str, set[str]] = defaultdict(set)
    modules: set[str] = set()

    for py_file in modules_root.rglob("*.py"):
        src = _module_from_file(modules_root, py_file)
        if not src:
            continue
        modules.add(src)
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=py_file.as_posix())
        except (SyntaxError, UnicodeDecodeError):
            continue

        for node in ast.walk(tree):
            imports: list[str] = []
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
            elif isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)

            for imported in imports:
                dst = _module_from_import(imported)
                if dst and dst != src:
                    edges[src].add(dst)

    pairs: set[tuple[str, str]] = set()
    for src, deps in edges.items():
        for dst in deps:
            if src in edges.get(dst, set()):
                pairs.add(tuple(sorted((src, dst))))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        f.write("# Circular Dependency Scan\n\n")
        f.write(f"- modules_observed: {len(modules)}\n")
        f.write(f"- circular_pairs: {len(pairs)}\n\n")
        f.write("## Circular Pairs\n")
        if not pairs:
            f.write("- none\n")
        else:
            for a, b in sorted(pairs):
                f.write(f"- {a} <-> {b}\n")

    print(f"Circular scan generated -> {output.as_posix()}")


if __name__ == "__main__":
    main()
