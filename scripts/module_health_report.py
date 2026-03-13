#!/usr/bin/env python3
"""Generate module health report for SILA modules."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ModuleHealth:
    name: str
    py_files: int
    has_domain: bool
    has_application: bool
    has_infrastructure: bool
    has_api: bool
    has_tests: bool
    inbound: int
    outbound: int

    @property
    def score(self) -> int:
        structural = sum(
            [
                self.has_domain,
                self.has_application,
                self.has_infrastructure,
                self.has_api,
                self.has_tests,
            ]
        )
        return structural + (1 if self.py_files >= 5 else 0)

    @property
    def grade(self) -> str:
        if self.score >= 6:
            return "A"
        if self.score >= 4:
            return "B"
        return "C"


def load_dependency_counters(path: Path) -> tuple[Counter, Counter]:
    inbound: Counter = Counter()
    outbound: Counter = Counter()
    if not path.exists():
        return inbound, outbound

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return inbound, outbound

    for edge in payload.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")
        weight = int(edge.get("weight", 0))
        if source:
            outbound[source] += weight
        if target:
            inbound[target] += weight
    return inbound, outbound


def collect_health(modules_root: Path, tests_root: Path, dep_json: Path) -> list[ModuleHealth]:
    inbound, outbound = load_dependency_counters(dep_json)
    items: list[ModuleHealth] = []

    for module_dir in sorted(d for d in modules_root.iterdir() if d.is_dir() and not d.name.startswith("__")):
        py_files = len(list(module_dir.rglob("*.py")))
        test_dir_local = module_dir / "tests"
        test_dir_global = tests_root / module_dir.name
        has_tests = test_dir_local.exists() or test_dir_global.exists()

        items.append(
            ModuleHealth(
                name=module_dir.name,
                py_files=py_files,
                has_domain=(module_dir / "domain").exists(),
                has_application=(module_dir / "application").exists(),
                has_infrastructure=(module_dir / "infrastructure").exists(),
                has_api=(module_dir / "api").exists() or (module_dir / "presentation").exists(),
                has_tests=has_tests,
                inbound=int(inbound[module_dir.name]),
                outbound=int(outbound[module_dir.name]),
            )
        )

    items.sort(key=lambda item: (item.grade, item.score, item.py_files), reverse=True)
    return items


def render_report(items: list[ModuleHealth]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    grade_counter = Counter(item.grade for item in items)

    lines: list[str] = []
    lines.append("# Module Health Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append("- Scope: `apps/backend/app/modules`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules: **{len(items)}**")
    lines.append(f"- Grade A: **{grade_counter['A']}**")
    lines.append(f"- Grade B: **{grade_counter['B']}**")
    lines.append(f"- Grade C: **{grade_counter['C']}**")
    lines.append("")
    lines.append("## Health Matrix")
    lines.append("")
    lines.append("| Module | Grade | Score | Py files | Domain | Application | Infrastructure | API/Presentation | Tests | Inbound deps | Outbound deps |")
    lines.append("| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | ---: |")

    for item in items:
        lines.append(
            f"| `{item.name}` | {item.grade} | {item.score} | {item.py_files} | "
            f"{'Y' if item.has_domain else 'N'} | {'Y' if item.has_application else 'N'} | "
            f"{'Y' if item.has_infrastructure else 'N'} | {'Y' if item.has_api else 'N'} | "
            f"{'Y' if item.has_tests else 'N'} | {item.inbound} | {item.outbound} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Score uses structural completeness + basic module size signal.")
    lines.append("- Inbound/Outbound deps are derived from `module_dependency_graph.json` when available.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate module health report.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root.",
    )
    parser.add_argument(
        "--tests-root",
        default="apps/backend/tests/modules",
        help="Path to module tests root.",
    )
    parser.add_argument(
        "--dependency-json",
        default="reports/module_dependency_graph.json",
        help="Dependency graph json path.",
    )
    parser.add_argument(
        "--output",
        default="reports/module_health_report.md",
        help="Output markdown path.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root).resolve()
    tests_root = Path(args.tests_root).resolve()
    dep_json = Path(args.dependency_json).resolve()
    output = Path(args.output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    items = collect_health(modules_root, tests_root, dep_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(items), encoding="utf-8")
    print(f"Generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
