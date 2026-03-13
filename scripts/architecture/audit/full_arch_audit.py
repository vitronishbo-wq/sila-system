#!/usr/bin/env python3
"""End-to-end architecture audit with per-module compliance scoring."""

from __future__ import annotations

import argparse
import ast
import json
from collections import defaultdict
from pathlib import Path


def _discover_modules(modules_root: Path) -> list[Path]:
    modules: list[Path] = []
    for manifest in modules_root.rglob("module.yaml"):
        module = manifest.parent
        rel = module.relative_to(modules_root)
        if len(rel.parts) < 2:
            continue
        modules.append(module)
    return sorted(set(modules), key=lambda p: p.as_posix())


def _module_name(modules_root: Path, module_dir: Path) -> str:
    return ".".join(module_dir.relative_to(modules_root).parts)


def _module_name_from_import(import_name: str) -> str | None:
    # app.modules.<macro>.<module>...
    parts = import_name.split(".")
    if len(parts) < 4:
        return None
    if parts[0] != "app" or parts[1] != "modules":
        return None
    return f"{parts[2]}.{parts[3]}"


def _module_name_from_file(modules_root: Path, py_file: Path) -> str | None:
    rel = py_file.relative_to(modules_root)
    if len(rel.parts) < 3:
        return None
    return f"{rel.parts[0]}.{rel.parts[1]}"


def run_audit(modules_root: Path) -> dict:
    modules = _discover_modules(modules_root)
    module_names = {_module_name(modules_root, m) for m in modules}

    violations: dict[str, list[str]] = {
        "circular_import_risk": [],
        "domain_importing_infra": [],
        "domain_importing_session": [],
        "missing_health": [],
        "missing_router": [],
        "parse_errors": [],
    }
    edges: dict[str, set[str]] = defaultdict(set)
    per_module: dict[str, dict] = {}

    for module in modules:
        name = _module_name(modules_root, module)
        has_domain = (module / "domain").is_dir()
        has_application = (module / "application").is_dir()
        has_infrastructure = (module / "infrastructure").is_dir()
        has_router = (module / "api/router.py").is_file()
        has_health = (module / "api/health.py").is_file()

        if not has_router:
            violations["missing_router"].append(module.as_posix())
        if not has_health:
            violations["missing_health"].append(module.as_posix())

        base_score = sum([has_domain, has_application, has_infrastructure, has_router, has_health]) * 20
        per_module[name] = {
            "path": module.as_posix(),
            "has_domain": has_domain,
            "has_application": has_application,
            "has_infrastructure": has_infrastructure,
            "has_router": has_router,
            "has_health": has_health,
            "base_score": base_score,
            "deduction": 0,
            "score": base_score,
            "issues": [],
        }

    for py_file in modules_root.rglob("*.py"):
        src_module = _module_name_from_file(modules_root, py_file)
        if src_module is None or src_module not in module_names:
            continue

        in_domain_layer = "domain" in py_file.parts
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=py_file.as_posix())
        except (SyntaxError, UnicodeDecodeError) as err:
            msg = f"{py_file.as_posix()} :: {err}"
            violations["parse_errors"].append(msg)
            per_module[src_module]["issues"].append("parse_error")
            continue

        for node in ast.walk(tree):
            imported_modules: list[str] = []
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_modules.append(node.module)
            elif isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)

            for imported in imported_modules:
                dst_module = _module_name_from_import(imported)
                if dst_module and dst_module in module_names and dst_module != src_module:
                    edges[src_module].add(dst_module)

                if in_domain_layer and imported.startswith("app.platform"):
                    violations["domain_importing_infra"].append(py_file.as_posix())
                    per_module[src_module]["issues"].append("domain_importing_platform")

                # Only flag real infrastructure layer imports, not names like
                # "infrastructure_sector" that are valid macro-domain names.
                if in_domain_layer and "infrastructure" in imported.split("."):
                    violations["domain_importing_infra"].append(py_file.as_posix())
                    per_module[src_module]["issues"].append("domain_importing_infrastructure")

                if in_domain_layer and imported == "sqlalchemy.orm":
                    if isinstance(node, ast.ImportFrom) and any(
                        alias.name == "Session" for alias in node.names
                    ):
                        violations["domain_importing_session"].append(py_file.as_posix())
                        per_module[src_module]["issues"].append("domain_importing_session")

    # Simple bidirectional circular risk.
    for src, deps in edges.items():
        for dst in deps:
            if src in edges.get(dst, set()):
                msg = f"{src} <-> {dst}"
                violations["circular_import_risk"].append(msg)
                per_module[src]["issues"].append("circular_import_risk")
                per_module[dst]["issues"].append("circular_import_risk")

    # Normalize and finalize scores.
    for module_data in per_module.values():
        issue_set = sorted(set(module_data["issues"]))
        module_data["issues"] = issue_set
        deduction = 0
        if "parse_error" in issue_set:
            deduction += 20
        if (
            "domain_importing_platform" in issue_set
            or "domain_importing_infrastructure" in issue_set
            or "domain_importing_session" in issue_set
        ):
            deduction += 30
        if "circular_import_risk" in issue_set:
            deduction += 20
        module_data["deduction"] = deduction
        module_data["score"] = max(0, module_data["base_score"] - module_data["deduction"])

    for key in violations:
        violations[key] = sorted(set(violations[key]))

    critical = sorted(
        ((name, data) for name, data in per_module.items() if data["score"] < 40),
        key=lambda item: (item[1]["score"], item[0]),
    )

    return {
        "modules_root": modules_root.as_posix(),
        "totals": {
            "modules": len(per_module),
            "circular_import_risk": len(violations["circular_import_risk"]),
            "domain_importing_infra": len(violations["domain_importing_infra"]),
            "domain_importing_session": len(violations["domain_importing_session"]),
            "missing_health": len(violations["missing_health"]),
            "missing_router": len(violations["missing_router"]),
            "parse_errors": len(violations["parse_errors"]),
            "critical_lt_40": len(critical),
        },
        "violations": violations,
        "per_module": dict(sorted(per_module.items())),
        "critical": [{"module": name, **data} for name, data in critical],
    }


def write_report(audit: dict, report_output: Path) -> None:
    report_output.parent.mkdir(parents=True, exist_ok=True)
    with report_output.open("w", encoding="utf-8") as f:
        f.write("# SILA ARCHITECTURE AUDIT (E2E)\n\n")
        f.write("## Summary\n")
        for key, value in audit["totals"].items():
            f.write(f"- {key}: {value}\n")
        f.write("\n")

        f.write("## Compliance By Module\n")
        f.write("| Module | Score | Domain | Application | Infrastructure | Router | Health | Issues |\n")
        f.write("|---|---:|:---:|:---:|:---:|:---:|:---:|---|\n")
        for name, data in sorted(audit["per_module"].items(), key=lambda item: (item[1]["score"], item[0])):
            issues = ", ".join(data["issues"]) if data["issues"] else "none"
            f.write(
                f"| {name} | {data['score']} | "
                f"{'Y' if data['has_domain'] else 'N'} | {'Y' if data['has_application'] else 'N'} | "
                f"{'Y' if data['has_infrastructure'] else 'N'} | {'Y' if data['has_router'] else 'N'} | "
                f"{'Y' if data['has_health'] else 'N'} | {issues} |\n"
            )
        f.write("\n")

        f.write("## Critical (<40)\n")
        if not audit["critical"]:
            f.write("- none\n\n")
        else:
            for item in audit["critical"]:
                f.write(f"- {item['module']} ({item['score']})\n")
            f.write("\n")

        f.write("## Violations\n")
        for key, values in audit["violations"].items():
            f.write(f"### {key}\n")
            if not values:
                f.write("- none\n\n")
                continue
            for value in values:
                f.write(f"- {value}\n")
            f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate full architecture audit report.")
    parser.add_argument("--modules-root", default="apps/backend/app/modules")
    parser.add_argument("--report-output", default="reports/architecture_audit.md")
    parser.add_argument("--json-output", default="reports/architecture_audit.json")
    args = parser.parse_args()

    modules_root = Path(args.modules_root)
    report_output = Path(args.report_output)
    json_output = Path(args.json_output)

    audit = run_audit(modules_root)
    write_report(audit, report_output)

    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Audit generated -> {report_output.as_posix()}")
    print(f"JSON generated -> {json_output.as_posix()}")


if __name__ == "__main__":
    main()
