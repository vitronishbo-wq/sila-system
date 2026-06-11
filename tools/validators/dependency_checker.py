#!/usr/bin/env python3
"""Simple dependency checker that builds an import graph and detects cycles.

This is intentionally minimal and does not attempt to fully resolve packages;
it provides a quick way to find obvious circular import patterns.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List, Set


def find_imports(path: Path) -> Set[str]:
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(src)
    except Exception:
        return set()
    imports: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports


def build_graph(root: Path) -> Dict[str, Set[str]]:
    graph: Dict[str, Set[str]] = {}
    for p in root.rglob("*.py"):
        if "tools/validators" in str(p):
            # skip our own helpers
            continue
        module_name = p.with_suffix("").relative_to(root).as_posix().replace("/", ".")
        graph[module_name] = set()
        for imp in find_imports(p):
            graph[module_name].add(imp)
    return graph


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    visited: Set[str] = set()
    stack: List[str] = []
    cycles: List[List[str]] = []

    def dfs(node: str, path: List[str]) -> None:
        if node in path:
            cycles.append(path[path.index(node) :] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path = path + [node]
        for neigh in graph.get(node, set()):
            if neigh in graph:  # only follow nodes we have in the graph
                dfs(neigh, path)

    for n in graph:
        if n not in visited:
            dfs(n, [])
    return cycles


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", default=Path("."), type=Path)
    args = parser.parse_args()

    graph = build_graph(args.root)
    cycles = find_cycles(graph)
    if cycles:
        print("Dependency cycles detected:")
        for c in cycles:
            print(" -> ".join(c))
        raise SystemExit(2)
    print("No dependency cycles found (quick scan).")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import re
import subprocess


def pip_can_install(req: str) -> bool:
    proc = subprocess.run(
        ["pip", "install", "--dry-run", "--quiet", req],
        capture_output=True,
    )
    return proc.returncode == 0


def validate_requirement_line(line: str) -> dict:
    line = line.strip()

    if not line or line.startswith("#"):
        return {"line": line, "status": "skip"}

    pattern = r"^([a-zA-Z0-9_\-]+)([<>=!]=.+)?$"
    if not re.match(pattern, line):
        return {"line": line, "status": "invalid-format"}

    if not pip_can_install(line):
        return {"line": line, "status": "not-installable"}

    return {"line": line, "status": "ok"}
