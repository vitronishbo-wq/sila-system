#!/usr/bin/env python3
"""
scan_integrity.py
Static scanner for repository integrity.
Produces JSON report at ./reports/integrity_report.json

Usage:
    python3 scripts/scan_integrity.py --modules apps/backend/modules --out reports/integrity_report.json
"""
import argparse
import ast
import json
import os
from pathlib import Path
from collections import defaultdict, Counter

TAB_RE = "__tablename__"
IMPORT_STAR = "import *"


def find_files(root: Path):
    return [p for p in root.rglob("*.py") if "__pycache__" not in p.parts]


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def parse_ast(path: Path):
    text = read_text(path)
    try:
        return ast.parse(text)
    except Exception:
        return None


def collect_tablenames(files):
    out = []
    for f in files:
        text = read_text(f)
        if "__tablename__" in text:
            for line_no, line in enumerate(text.splitlines(), start=1):
                if "__tablename__" in line:
                    out.append({"file": str(f), "line": line_no, "text": line.strip()})
    return out


def collect_import_star(files):
    out = []
    for f in files:
        text = read_text(f)
        if "import *" in text:
            for line_no, line in enumerate(text.splitlines(), start=1):
                if "import *" in line:
                    out.append({"file": str(f), "line": line_no, "text": line.strip()})
    return out


def collect_model_validate_calls(files):
    out = []
    for f in files:
        text = read_text(f)
        if "model_validate(" in text:
            for idx, line in enumerate(text.splitlines(), start=1):
                if "model_validate(" in line:
                    out.append({"file": str(f), "line": idx, "text": line.strip()})
    return out


def collect_status_value_access(files):
    out = []
    for f in files:
        text = read_text(f)
        if ".status.value" in text or ".value" in text:
            for idx, line in enumerate(text.splitlines(), start=1):
                if ".status.value" in line or ".value" in line:
                    out.append({"file": str(f), "line": idx, "text": line.strip()})
    return out


def collect_raw_table_name_usages(files, tablenames):
    # searches for literal usages of known tablenames (heuristic)
    names = set([t["text"].split("=")[-1].strip().strip("'\"") for t in tablenames])
    out = []
    if not names:
        return out
    for f in files:
        text = read_text(f)
        for name in names:
            if name in text:
                for idx, line in enumerate(text.splitlines(), start=1):
                    if name in line:
                        out.append(
                            {
                                "file": str(f),
                                "line": idx,
                                "match": name,
                                "text": line.strip(),
                            }
                        )
    return out


def collect_defs(files):
    classes = defaultdict(list)
    funcs = defaultdict(list)
    for f in files:
        tree = parse_ast(f)
        if not tree:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes[node.name].append(str(f))
            elif isinstance(node, ast.FunctionDef):
                funcs[node.name].append(str(f))
    return classes, funcs


def build_import_graph(files, modules_root: Path):
    # simple graph: module -> set(imported modules)
    graph = defaultdict(set)
    for f in files:
        tree = parse_ast(f)
        if not tree:
            continue
        module_key = str(f.relative_to(modules_root))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    graph[module_key].add(n.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                graph[module_key].add(mod)
    # detect cycles up to length 4 (heuristic)
    cycles = []
    for a in graph:
        for b in graph[a]:
            if b in graph and a in graph[b]:
                cycles.append([a, b])
    return graph, cycles


def orphan_modules(files, graph, modules_root: Path):
    # modules with low indegree (heuristic)
    indeg = Counter()
    for k, targets in graph.items():
        for t in targets:
            indeg[t] += 1
    orphans = []
    for f in files:
        key = str(f.relative_to(modules_root))
        if indeg.get(key, 0) == 0:
            # ignore tests and examples
            if "tests" in key or "examples" in key:
                continue
            orphans.append(key)
    return orphans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", default="apps/backend/modules")
    parser.add_argument("--out", default="reports/integrity_report.json")
    args = parser.parse_args()

    modules_root = Path(args.modules).resolve()
    files = find_files(modules_root)

    print(f"Scanning {len(files)} python files under {modules_root}")

    tablenames = collect_tablenames(files)
    import_star = collect_import_star(files)
    model_validate_calls = collect_model_validate_calls(files)
    status_value = collect_status_value_access(files)
    classes, funcs = collect_defs(files)
    graph, cycles = build_import_graph(files, modules_root)
    orphans = orphan_modules(files, graph, modules_root)
    raw_usages = collect_raw_table_name_usages(files, tablenames)

    dup_classes = {k: v for k, v in classes.items() if len(v) > 1}
    dup_funcs = {k: v for k, v in funcs.items() if len(v) > 1}

    out = {
        "scan_root": str(modules_root),
        "total_files": len(files),
        "tablenames": tablenames,
        "import_star": import_star,
        "model_validate_calls": model_validate_calls,
        "status_value_access": status_value,
        "duplicate_classes": dup_classes,
        "duplicate_functions": dup_funcs,
        "import_graph_sample": {k: list(v) for k, v in list(graph.items())[:200]},
        "import_cycles": cycles,
        "orphan_modules": orphans,
        "raw_table_usages": raw_usages,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Written report to", out_path)


if __name__ == "__main__":
    main()
