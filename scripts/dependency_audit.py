#!/usr/bin/env python3
"""
FASE 5: Dependency Audit
Check for circular dependencies and import conflicts between modules
"""

import ast
from collections import defaultdict
from pathlib import Path


def print_box(title="", width=80, char="="):
    """Print a box with title."""
    if title:
        padding_left = (width - len(title) - 2) // 2
        padding_right = width - len(title) - 2 - padding_left
        print(f"{char * padding_left} {title} {char * padding_right}")
    else:
        print(char * width)


def print_progress_bar(passed, total, width=40):
    """Print a progress bar."""
    percentage = (passed * 100) // total if total > 0 else 0
    filled = (passed * width) // total
    empty = width - filled
    bar = "█" * filled + "░" * empty
    print(f"  [{bar}] {passed}/{total} ({percentage}%)")


def extract_imports(file_path):
    """Extract module imports from a Python file."""
    try:
        tree = ast.parse(file_path.read_text())
    except:
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def build_dependency_graph():
    """Build dependency graph for all modules."""
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    modules = sorted(
        [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
    )

    graph = defaultdict(set)

    for module in modules:
        module_files = list(module.glob("**/*.py"))
        module_imports = set()

        for py_file in module_files:
            imports = extract_imports(py_file)
            for imp in imports:
                # Check if it's an internal module import
                if imp == "app" or imp in [m.name for m in modules]:
                    if imp != "app":
                        module_imports.add(imp)

        graph[module.name] = module_imports

    return graph, modules


def detect_circular_deps(graph):
    """Detect circular dependencies using DFS."""
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
            elif neighbor in rec_stack:
                cycle = path + [neighbor]
                cycles.append(cycle)

        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [node])

    return cycles


def analyze_module_isolation():
    """Analyze module isolation (coupling check)."""
    graph, modules = build_dependency_graph()

    isolation_score = 0
    very_coupled = []

    for module_name, deps in graph.items():
        if len(deps) > 3:
            very_coupled.append((module_name, len(deps)))
        else:
            isolation_score += 1

    return isolation_score, very_coupled, len(modules), graph


def main():
    print_box("DEPENDENCY AUDIT - SILA SYSTEM", width=80)

    # Test 1: Module Isolation
    print("\nTEST 1: Module Isolation (Low Coupling)")
    print("-" * 80)

    isolation_score, very_coupled, total_modules, graph = analyze_module_isolation()
    print(f"Modules checked: {total_modules}")
    print_progress_bar(isolation_score, total_modules)

    if very_coupled:
        print("\nModules with high coupling (>3 dependencies):")
        for mod_name, count in sorted(very_coupled, key=lambda x: -x[1])[:5]:
            print(f"  - {mod_name}: {count} dependencies")

    # Test 2: Circular Dependencies
    print("\nTEST 2: Circular Dependency Detection")
    print("-" * 80)

    cycles = detect_circular_deps(graph)
    no_cycles = len(cycles) == 0

    if no_cycles:
        print(f"Modules checked: {total_modules}")
        print_progress_bar(total_modules, total_modules)
        print("\nStatus: ✓ NO CIRCULAR DEPENDENCIES DETECTED")
    else:
        print(f"Found {len(cycles)} potential cycles:")
        for cycle in cycles[:3]:
            print(f"  → {' → '.join(cycle)}")

    # Summary
    print_box("SUMMARY", width=80)

    summary_tests = [
        ("Module Isolation", isolation_score, total_modules),
        ("No Circular Deps", total_modules if no_cycles else 0, total_modules),
    ]

    total_passed = sum(p for _, p, _ in summary_tests)
    total_tests = sum(t for _, _, t in summary_tests)

    for test_name, passed, total in summary_tests:
        indicator = "[√]" if passed == total else "[×]"
        print(f"  {indicator} {test_name:<30} {passed:>3}/{total:>3}")

    percentage = (total_passed * 100) // total_tests if total_tests > 0 else 0
    print()
    print_box()
    print_progress_bar(total_passed, total_tests, width=50)
    print(f"\nOVERALL: {total_passed}/{total_tests} checks passed ({percentage}%)")
    print_box()


if __name__ == "__main__":
    main()
