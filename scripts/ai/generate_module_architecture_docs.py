#!/usr/bin/env python3
"""Generate ARCHITECTURE.md for every backend module plus a visual summary report."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.module_registry import MODULE_INDEX, iter_modules  # noqa: E402


DECORATOR_RE = re.compile(
    r"""@\s*(?P<router>[A-Za-z_][A-Za-z0-9_]*)\.
    (?P<method>get|post|put|patch|delete|options|head|api_route|websocket)
    \(\s*(?P<quote>["'])(?P<path>.*?)(?P=quote)""",
    re.VERBOSE,
)


@dataclass(slots=True)
class ModuleDocStats:
    name: str
    domain: str
    layers: list[str]
    entities: list[str]
    use_cases: list[str]
    endpoints: list[str]
    dependencies: list[str]
    output_path: Path


def run_dependency_scan(modules_root: Path, output_json: Path) -> None:
    cmd = [
        "python3",
        "scripts/module_dependency_analysis.py",
        "--modules-root",
        modules_root.as_posix(),
        "--output-json",
        output_json.as_posix(),
        "--output-md",
        "reports/module_dependencies.md",
    ]
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def read_dependency_graph(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def parse_symbols(py_file: Path) -> tuple[list[str], list[str]]:
    try:
        source = py_file.read_text(encoding="utf-8")
    except OSError:
        return [], []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [], []

    classes: list[str] = []
    functions: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            functions.append(node.name)
    return sorted(set(classes)), sorted(set(functions))


def collect_layers(module_dir: Path) -> list[str]:
    ordered = ["domain", "application", "infrastructure", "api", "tests"]
    layers = [layer for layer in ordered if (module_dir / layer).exists()]
    return layers


def collect_entities(module_dir: Path) -> list[str]:
    entities: set[str] = set()
    candidates: list[Path] = []

    primary = module_dir / "domain" / "entities.py"
    if primary.exists():
        candidates.append(primary)

    domain_dir = module_dir / "domain"
    if domain_dir.exists():
        for py_file in sorted(domain_dir.rglob("*.py")):
            if py_file.name in {"__init__.py", "conftest.py"}:
                continue
            if "__pycache__" in py_file.parts or "tests" in py_file.parts:
                continue
            if py_file not in candidates:
                candidates.append(py_file)

    for py_file in candidates:
        classes, _ = parse_symbols(py_file)
        entities.update(classes)

    if not entities:
        for py_file in candidates:
            if py_file.stem not in {"__init__", "conftest", "entities"}:
                entities.add(py_file.stem)
    return sorted(entities)


def collect_use_cases(module_dir: Path) -> list[str]:
    use_cases: set[str] = set()
    application_dir = module_dir / "application"
    if not application_dir.exists():
        return []

    preferred_dirs = ("use_cases", "services", "handlers")
    for folder_name in preferred_dirs:
        folder = application_dir / folder_name
        if not folder.exists():
            continue
        for py_file in sorted(folder.rglob("*.py")):
            if py_file.name in {"__init__.py", "conftest.py"}:
                continue
            if "__pycache__" in py_file.parts or "tests" in py_file.parts:
                continue
            classes, functions = parse_symbols(py_file)
            use_cases.update(classes)
            use_cases.update(functions)

    for single_file in ("commands.py", "queries.py", "service.py", "services.py"):
        py_file = application_dir / single_file
        if py_file.exists():
            classes, functions = parse_symbols(py_file)
            use_cases.update(classes)
            use_cases.update(functions)

    if not use_cases:
        for py_file in sorted(application_dir.rglob("*.py")):
            if py_file.name in {"__init__.py", "conftest.py"}:
                continue
            if "__pycache__" in py_file.parts or "tests" in py_file.parts:
                continue
            if py_file.stem.startswith("_"):
                continue
            use_cases.add(py_file.stem)
    return sorted(use_cases)


def resolve_router_files(module_dir: Path) -> list[Path]:
    api_dir = module_dir / "api"
    if not api_dir.exists():
        return []
    files: list[Path] = []
    primary = api_dir / "router.py"
    if primary.exists():
        files.append(primary)
    for pattern in ("*router*.py", "*routes*.py"):
        for py_file in sorted(api_dir.glob(pattern)):
            if py_file.name == "router.py":
                continue
            if py_file.name in {"__init__.py", "conftest.py"}:
                continue
            files.append(py_file)
    return files


def collect_endpoints(module_dir: Path, module_name: str) -> list[str]:
    spec = MODULE_INDEX.get(module_name)
    mount_prefix = ""
    if spec and spec.bootstrap_scope == "api":
        mount_prefix = spec.mount_prefix

    endpoints: set[str] = set()
    for router_file in resolve_router_files(module_dir):
        try:
            text = router_file.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in DECORATOR_RE.finditer(text):
            method = match.group("method").upper()
            raw_path = match.group("path").strip() or "/"
            if not raw_path.startswith("/"):
                raw_path = f"/{raw_path}"
            effective_path = raw_path
            if mount_prefix:
                if raw_path == "/":
                    effective_path = mount_prefix
                else:
                    effective_path = f"{mount_prefix.rstrip('/')}{raw_path}"
            endpoints.add(f"{method} {effective_path}")
    return sorted(endpoints)


def collect_dependencies(module_name: str, graph: dict) -> list[str]:
    deps: set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("source") == module_name and edge.get("target"):
            deps.add(edge["target"])
    return sorted(deps)


def purpose_for_module(module_name: str, domain: str) -> str:
    return (
        f"Gerir capacidades do dominio governamental `{module_name}` no contexto federado `{domain}`."
    )


def build_module_doc(module_dir: Path, stats: ModuleDocStats) -> str:
    lines: list[str] = []
    lines.append("# Module Architecture")
    lines.append("")
    lines.append(f"Domain: {stats.name}")
    lines.append("")
    lines.append("Path:")
    lines.append(f"{module_dir.as_posix()}")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append(purpose_for_module(stats.name, stats.domain))
    lines.append("")
    lines.append("## Core Responsibilities")
    lines.append("")
    lines.append(f"- Modelar regras de negocio do modulo `{stats.name}`.")
    lines.append("- Orquestrar casos de uso na camada `application`.")
    lines.append("- Expor capacidades publicas via camada `api`.")
    lines.append("")
    lines.append("## Architecture")
    lines.append("")
    lines.append("DDD + Clean Architecture")
    lines.append("")
    lines.append("Layers:")
    lines.append("")
    for layer in stats.layers:
        lines.append(f"- {layer}")
    lines.append("")
    lines.append("## Key Entities")
    lines.append("")
    if stats.entities:
        for entity in stats.entities[:80]:
            lines.append(f"- {entity}")
    else:
        lines.append("- Nenhuma entidade identificada automaticamente em `domain`.")
    lines.append("")
    lines.append("## Use Cases")
    lines.append("")
    if stats.use_cases:
        for use_case in stats.use_cases[:100]:
            lines.append(f"- {use_case}")
    else:
        lines.append("- Nenhum caso de uso identificado automaticamente em `application`.")
    lines.append("")
    lines.append("## Public API")
    lines.append("")
    if stats.endpoints:
        lines.append("Routers encontrados em `api/router.py` e arquivos `api/*router*.py`/`api/*routes*.py`:")
        lines.append("")
        for endpoint in stats.endpoints[:120]:
            lines.append(f"- {endpoint}")
    else:
        lines.append("- Nenhum endpoint detectado automaticamente no diretório `api`.")
    lines.append("")
    lines.append("## Dependencies")
    lines.append("")
    if stats.dependencies:
        for dep in stats.dependencies:
            lines.append(f"- {dep}")
    else:
        lines.append("- Sem dependencias externas de modulo detectadas.")
    lines.append("")
    lines.append("## Notes for AI Agents")
    lines.append("")
    lines.append("Regras importantes para IA:")
    lines.append("")
    lines.append("- Nao acessar outros dominios diretamente.")
    lines.append("- Usar `application` services/handlers como orquestracao.")
    lines.append("- Manter separacao DDD entre `domain`, `application`, `infrastructure` e `api`.")
    lines.append("")
    lines.append(
        "_Auto-generated by `scripts/ai/generate_module_architecture_docs.py`. "
        "Nao editar manualmente; regenerar via `make architecture-docs`._"
    )
    lines.append("")
    return "\n".join(lines)


def render_visual_report(stats: list[ModuleDocStats], output_path: Path) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    total_modules = len(stats)
    with_entities = sum(1 for item in stats if item.entities)
    with_use_cases = sum(1 for item in stats if item.use_cases)
    with_api = sum(1 for item in stats if item.endpoints)

    lines: list[str] = []
    lines.append("# Module Architecture Docs Visual Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Output: `{output_path.as_posix()}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules scanned: **{total_modules}**")
    lines.append(f"- ARCHITECTURE.md generated: **{total_modules}**")
    lines.append(f"- Modules with entities detected: **{with_entities}**")
    lines.append(f"- Modules with use cases detected: **{with_use_cases}**")
    lines.append(f"- Modules with API endpoints detected: **{with_api}**")
    lines.append("")
    lines.append("## Coverage Matrix")
    lines.append("")
    lines.append("| Module | Domain Group | Layers | Entities | Use Cases | API Endpoints | Dependencies |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    for item in sorted(stats, key=lambda x: x.name):
        lines.append(
            f"| `{item.name}` | `{item.domain}` | {len(item.layers)} | {len(item.entities)} | "
            f"{len(item.use_cases)} | {len(item.endpoints)} | {len(item.dependencies)} |"
        )
    lines.append("")
    lines.append("## Dependency Topology (Top 30 by outbound degree)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    ranked = sorted(stats, key=lambda x: len(x.dependencies), reverse=True)
    edge_count = 0
    for item in ranked:
        for dep in item.dependencies:
            lines.append(f"  {item.name} --> {dep}")
            edge_count += 1
            if edge_count >= 30:
                break
        if edge_count >= 30:
            break
    if edge_count == 0:
        lines.append("  A[\"No cross-module dependencies detected\"]")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def module_dirs(modules_root: Path) -> list[Path]:
    dirs = [
        d
        for d in sorted(modules_root.iterdir(), key=lambda p: p.name)
        if d.is_dir() and not d.name.startswith("__")
    ]
    return dirs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate ARCHITECTURE.md for all backend modules."
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root path.",
    )
    parser.add_argument(
        "--dependency-json",
        default="reports/module_dependency_graph.json",
        help="Dependency graph JSON path.",
    )
    parser.add_argument(
        "--refresh-dependencies",
        action="store_true",
        help="Regenerate dependency graph before generating docs.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/module_architecture_docs_visual_report.md",
        help="Visual report output path.",
    )
    args = parser.parse_args()

    modules_root = (REPO_ROOT / args.modules_root).resolve()
    dependency_json = (REPO_ROOT / args.dependency_json).resolve()
    report_output = (REPO_ROOT / args.report_output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    if args.refresh_dependencies or not dependency_json.exists():
        run_dependency_scan(modules_root, dependency_json)

    dependency_graph = read_dependency_graph(dependency_json)

    stats_rows: list[ModuleDocStats] = []
    registry_specs = {spec.name: spec for spec in iter_modules(enabled_only=False)}
    for module_dir in module_dirs(modules_root):
        module_name = module_dir.name
        spec = registry_specs.get(module_name)
        domain_group = spec.domain if spec else "unknown"

        stats = ModuleDocStats(
            name=module_name,
            domain=domain_group,
            layers=collect_layers(module_dir),
            entities=collect_entities(module_dir),
            use_cases=collect_use_cases(module_dir),
            endpoints=collect_endpoints(module_dir, module_name),
            dependencies=collect_dependencies(module_name, dependency_graph),
            output_path=module_dir / "ARCHITECTURE.md",
        )

        content = build_module_doc(module_dir, stats)
        stats.output_path.write_text(content, encoding="utf-8")
        stats_rows.append(stats)

    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(render_visual_report(stats_rows, report_output), encoding="utf-8")

    print(f"Generated module docs: {len(stats_rows)}")
    print(f"Generated visual report: {report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
