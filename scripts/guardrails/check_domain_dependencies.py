#!/usr/bin/env python3
"""Policy-driven dependency guardrail for SILA architecture."""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


CORE_IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+app\.modules\.", re.MULTILINE)
MODULE_IMPORT_RE = re.compile(
    r"^\s*(?:from|import)\s+app\.modules\.(?P<target>[A-Za-z_][A-Za-z0-9_]*)"
    r"(?P<suffix>(?:\.[A-Za-z_][A-Za-z0-9_]*)*)",
    re.MULTILINE,
)
INTERNAL_TARGETS = {"core", "shared", "common"}


@dataclass(frozen=True)
class Policy:
    allow_circular_dependencies: bool
    core_can_import_modules: bool
    strict_boundary_validation: bool
    core_module_import_exempt_paths: tuple[str, ...]
    allowed_dependencies: dict[str, set[str]]


@dataclass(frozen=True)
class ModuleManifest:
    name: str
    requires_domains: set[str]
    exposed_paths: set[str]


def load_structured(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
        if path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(text) or {}
        return json.loads(text) or {}
    except Exception as exc:  # pragma: no cover - guardrail must never crash on parsing
        print(f"⚠️  Failed to parse {path}: {exc}")
        return {}


def parse_observed_edges(payload: dict[str, Any]) -> list[tuple[str, str, int]]:
    edges: list[tuple[str, str, int]] = []
    for edge in payload.get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = edge.get("source")
        target = edge.get("target")
        if not source or not target or source == target:
            continue
        weight = edge.get("weight", 1)
        edges.append((str(source), str(target), int(weight)))
    return edges


def parse_declared_dependencies(payload: dict[str, Any]) -> dict[str, set[str]]:
    modules = payload.get("modules", {})
    declared: dict[str, set[str]] = {}
    if not isinstance(modules, dict):
        return declared

    for module_name, data in modules.items():
        if not isinstance(data, dict):
            continue
        depends_on = data.get("depends_on", [])
        if not isinstance(depends_on, list):
            depends_on = []
        declared[str(module_name)] = {
            str(dep) for dep in depends_on if isinstance(dep, str) and dep != module_name
        }
    return declared


def parse_module_domains(payload: dict[str, Any]) -> dict[str, str]:
    modules = payload.get("modules", {})
    if not isinstance(modules, dict):
        return {}

    mapping: dict[str, str] = {}
    for module_name, data in modules.items():
        if not isinstance(data, dict):
            continue
        domain_group = data.get("domain_group")
        if isinstance(domain_group, str) and domain_group:
            mapping[str(module_name)] = domain_group
        else:
            mapping[str(module_name)] = str(module_name)
    return mapping


def parse_policy(payload: dict[str, Any]) -> Policy:
    rules = payload.get("rules", {}) if isinstance(payload.get("rules"), dict) else {}
    domains = payload.get("domains", {}) if isinstance(payload.get("domains"), dict) else {}

    allowed: dict[str, set[str]] = {}
    for domain_name, domain_cfg in domains.items():
        if not isinstance(domain_cfg, dict):
            allowed[str(domain_name)] = set()
            continue
        deps = domain_cfg.get("allowed_dependencies", [])
        if not isinstance(deps, list):
            deps = []
        allowed[str(domain_name)] = {str(item) for item in deps if isinstance(item, str)}

    return Policy(
        allow_circular_dependencies=bool(rules.get("allow_circular_dependencies", False)),
        core_can_import_modules=bool(rules.get("core_can_import_modules", False)),
        strict_boundary_validation=bool(rules.get("strict_boundary_validation", True)),
        core_module_import_exempt_paths=tuple(
            str(item).strip("/")
            for item in rules.get("core_module_import_exempt_paths", [])
            if isinstance(item, str) and str(item).strip("/")
        ),
        allowed_dependencies=allowed,
    )


def load_module_manifests(repo_root: Path, manifest_glob: str) -> dict[str, ModuleManifest]:
    manifests: dict[str, ModuleManifest] = {}
    pattern = (repo_root / manifest_glob).as_posix()
    for match in sorted(glob.glob(pattern)):
        path = Path(match)
        payload = load_structured(path)
        if not isinstance(payload, dict):
            continue
        name = payload.get("name")
        if not isinstance(name, str) or not name:
            continue
        requires = payload.get("requires", {})
        requires_domains = {
            str(item)
            for item in (requires.get("domains", []) if isinstance(requires, dict) else [])
            if isinstance(item, str) and item
        }
        exposes = payload.get("exposes", {})
        exposed_paths: set[str] = set()
        if isinstance(exposes, dict):
            for key in ("api_routers", "public_models"):
                values = exposes.get(key, [])
                if not isinstance(values, list):
                    continue
                for item in values:
                    if isinstance(item, str) and item:
                        exposed_paths.add(item)
        manifests[name] = ModuleManifest(
            name=name,
            requires_domains=requires_domains,
            exposed_paths=exposed_paths,
        )
    return manifests


def scan_module_imports(repo_root: Path) -> dict[tuple[str, str], set[str]]:
    modules_root = repo_root / "apps" / "backend" / "app" / "modules"
    imports_by_edge: dict[tuple[str, str], set[str]] = {}
    if not modules_root.exists():
        return imports_by_edge

    for py_file in modules_root.rglob("*.py"):
        if "__pycache__" in py_file.parts or "tests" in py_file.parts:
            continue
        rel_parts = py_file.relative_to(modules_root).parts
        if len(rel_parts) < 2:
            continue
        source_module = rel_parts[0]
        try:
            content = py_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for match in MODULE_IMPORT_RE.finditer(content):
            target_module = match.group("target")
            if not target_module or target_module == source_module:
                continue
            suffix = match.group("suffix") or ""
            import_path = f"app.modules.{target_module}{suffix}"
            imports_by_edge.setdefault((source_module, target_module), set()).add(import_path)
    return imports_by_edge


def _is_exempt_path(rel_path: str, exemptions: tuple[str, ...]) -> bool:
    normalized = rel_path.strip("/")
    for exempt in exemptions:
        prefix = exempt.strip("/")
        if normalized == prefix or normalized.startswith(prefix + "/"):
            return True
    return False


def scan_core_imports(repo_root: Path, exemptions: tuple[str, ...]) -> list[tuple[str, int, str]]:
    core_dir = repo_root / "apps" / "backend" / "app" / "core"
    if not core_dir.exists():
        return []

    violations: list[tuple[str, int, str]] = []
    for py_file in core_dir.rglob("*.py"):
        rel = py_file.relative_to(repo_root).as_posix()
        if _is_exempt_path(rel, exemptions):
            continue
        if "__pycache__" in py_file.parts or "tests" in py_file.parts:
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(content.splitlines(), start=1):
            if CORE_IMPORT_RE.match(line):
                violations.append((rel, line_no, line.strip()))
    return violations


def build_report(
    observed_edges: list[tuple[str, str, int]],
    declared_deps: dict[str, set[str]],
    graph_violations: list[tuple[str, str, int]],
    policy_violations: list[tuple[str, str, str, str, int]],
    manifest_violations: list[tuple[str, str, str, int]],
    core_violations: list[tuple[str, int, str]],
    cycle_violations: list[list[str]],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    failed = any(
        (
            graph_violations,
            policy_violations,
            manifest_violations,
            core_violations,
            cycle_violations,
        )
    )

    lines: list[str] = []
    lines.append("# Domain Dependency Guardrail Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Status: {'FAILED' if failed else 'PASSED'}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Observed edges: **{len(observed_edges)}**")
    lines.append(f"- Declared modules: **{len(declared_deps)}**")
    lines.append(f"- Graph violations: **{len(graph_violations)}**")
    lines.append(f"- Policy violations: **{len(policy_violations)}**")
    lines.append(f"- Manifest violations: **{len(manifest_violations)}**")
    lines.append(f"- Core import violations: **{len(core_violations)}**")
    lines.append(f"- Cycle violations: **{len(cycle_violations)}**")
    lines.append("")

    lines.append("## Graph Violations")
    lines.append("")
    if graph_violations:
        lines.append("| Source | Target | Weight |")
        lines.append("| --- | --- | ---: |")
        for source, target, weight in graph_violations[:100]:
            lines.append(f"| `{source}` | `{target}` | {weight} |")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Policy Violations")
    lines.append("")
    if policy_violations:
        lines.append("| Source | Target | Source Domain | Target Domain | Weight |")
        lines.append("| --- | --- | --- | --- | ---: |")
        for source, target, source_domain, target_domain, weight in policy_violations[:100]:
            lines.append(
                f"| `{source}` | `{target}` | `{source_domain}` | `{target_domain}` | {weight} |"
            )
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Manifest Contract Violations")
    lines.append("")
    if manifest_violations:
        lines.append("| Source | Target | Rule | Weight |")
        lines.append("| --- | --- | --- | ---: |")
        for source, target, rule, weight in manifest_violations[:100]:
            lines.append(f"| `{source}` | `{target}` | {rule} | {weight} |")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Core Import Violations")
    lines.append("")
    if core_violations:
        for rel, line_no, line in core_violations[:100]:
            lines.append(f"- `{rel}:{line_no}` {line}")
    else:
        lines.append("- None.")
    lines.append("")

    lines.append("## Cycle Violations")
    lines.append("")
    if cycle_violations:
        for cycle in cycle_violations:
            chain = " -> ".join(f"`{node}`" for node in cycle)
            lines.append(f"- {chain}")
    else:
        lines.append("- None.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="SILA domain dependency guardrail")
    parser.add_argument("--observed-json", default="reports/module_dependency_graph.json")
    parser.add_argument("--declared-graph", default="docs/AI_ARCHITECTURE_GRAPH.yaml")
    parser.add_argument(
        "--policy-yaml",
        default="docs/architecture/domain_dependency_policy.yaml",
        help="Policy source-of-truth for allowed domain dependencies.",
    )
    parser.add_argument("--report-output", default="reports/domain_dependency_guardrail_report.md")
    parser.add_argument(
        "--manifest-glob",
        default="apps/backend/app/modules/*/module.yaml",
        help="Glob pattern for module contract manifests.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used to scan core imports.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    observed_payload = load_structured(repo_root / args.observed_json)
    declared_payload = load_structured(repo_root / args.declared_graph)
    policy_payload = load_structured(repo_root / args.policy_yaml)

    if not observed_payload or not declared_payload or not policy_payload:
        print("❌ Missing required artifacts. Run architecture generation first.")
        return 1

    observed_edges = parse_observed_edges(observed_payload)
    declared_deps = parse_declared_dependencies(declared_payload)
    module_domains = parse_module_domains(declared_payload)
    policy = parse_policy(policy_payload)
    manifests = load_module_manifests(repo_root, args.manifest_glob)
    import_map = scan_module_imports(repo_root)

    graph_violations: list[tuple[str, str, int]] = []
    policy_violations: list[tuple[str, str, str, str, int]] = []
    manifest_violations: list[tuple[str, str, str, int]] = []

    for source, target, weight in observed_edges:
        if source in declared_deps and target not in declared_deps[source] and target not in INTERNAL_TARGETS:
            graph_violations.append((source, target, weight))

        source_domain = module_domains.get(source, source)
        target_domain = module_domains.get(target, target)

        source_allowed = policy.allowed_dependencies.get(source_domain)
        if source_allowed is None:
            if policy.strict_boundary_validation:
                policy_violations.append((source, target, source_domain, target_domain, weight))
            continue

        if target_domain != source_domain and target_domain not in source_allowed:
            policy_violations.append((source, target, source_domain, target_domain, weight))

        source_manifest = manifests.get(source)
        target_manifest = manifests.get(target)
        if source_manifest is None and source not in INTERNAL_TARGETS:
            manifest_violations.append((source, target, "missing_source_manifest", weight))
        elif (
            source_manifest
            and target not in INTERNAL_TARGETS
            and target != source
            and target not in source_manifest.requires_domains
        ):
            manifest_violations.append((source, target, "requires.domains_missing_target", weight))

        if source_manifest and target_manifest and target not in INTERNAL_TARGETS and target != source:
            imported_paths = import_map.get((source, target), set())
            if not target_manifest.exposed_paths:
                manifest_violations.append(
                    (source, target, "target_has_no_exposed_contracts", weight)
                )
            for import_path in sorted(imported_paths):
                if not any(import_path.startswith(prefix) for prefix in target_manifest.exposed_paths):
                    manifest_violations.append(
                        (source, target, f"import_not_exposed:{import_path}", weight)
                    )

    core_violations = (
        scan_core_imports(
            repo_root,
            exemptions=policy.core_module_import_exempt_paths,
        )
        if not policy.core_can_import_modules
        else []
    )
    cycle_violations = (
        [list(group) for group in observed_payload.get("cycles", []) if isinstance(group, list)]
        if not policy.allow_circular_dependencies
        else []
    )

    report = build_report(
        observed_edges=observed_edges,
        declared_deps=declared_deps,
        graph_violations=graph_violations,
        policy_violations=policy_violations,
        manifest_violations=manifest_violations,
        core_violations=core_violations,
        cycle_violations=cycle_violations,
    )
    report_path = repo_root / args.report_output
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    total_violations = (
        len(graph_violations)
        + len(policy_violations)
        + len(manifest_violations)
        + len(core_violations)
        + len(cycle_violations)
    )
    if total_violations:
        print(f"❌ Found {total_violations} violations. See {args.report_output}")
        return 1

    print("✅ Compliance OK: Code matches architecture graph and policy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
