#!/usr/bin/env python3
"""Generate architecture index artifacts for fast AI navigation in monorepos."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.core.module_registry import iter_modules  # noqa: E402

DECORATOR_RE = re.compile(
    r"""@\s*(?P<router>[A-Za-z_][A-Za-z0-9_]*)\.
    (?P<method>get|post|put|patch|delete|options|head|api_route|websocket)
    \(\s*(?P<quote>["'])(?P<path>.*?)(?P=quote)""",
    re.VERBOSE,
)

BOUNDED_CONTEXT_ALIASES = {
    "educacao": "education",
}


def relpath(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return "''"
    safe = re.fullmatch(r"[A-Za-z0-9_./:+\-]+", text) is not None
    if safe and ":" not in text:
        return text
    escaped = text.replace("'", "''")
    return f"'{escaped}'"


def dump_yaml(data: Any, indent: int = 0) -> str:
    space = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, dict):
                if value:
                    lines.append(f"{space}{key}:")
                    lines.append(dump_yaml(value, indent + 2))
                else:
                    lines.append(f"{space}{key}: {{}}")
                continue
            if isinstance(value, list):
                if value:
                    lines.append(f"{space}{key}:")
                    lines.append(dump_yaml(value, indent + 2))
                else:
                    lines.append(f"{space}{key}: []")
                continue
            lines.append(f"{space}{key}: {yaml_scalar(value)}")
        return "\n".join(lines) if lines else f"{space}{{}}"
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{space}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{space}- {yaml_scalar(item)}")
        return "\n".join(lines) if lines else f"{space}[]"
    return f"{space}{yaml_scalar(data)}"


def read_dependency_graph(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


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


def service_hint(module_dir: Path) -> str | None:
    services_dir = module_dir / "application" / "services"
    if services_dir.is_dir():
        return relpath(services_dir)

    candidates = (
        module_dir / "application" / "services.py",
        module_dir / "application" / "service.py",
    )
    for candidate in candidates:
        if candidate.exists():
            return relpath(candidate)

    fallback = module_dir / "application"
    if fallback.exists():
        return relpath(fallback)
    return None


def resolve_router_path(router_import: str | None, module_dir: Path) -> Path | None:
    if router_import:
        module_path = router_import.split(":", maxsplit=1)[0]
        if module_path.startswith("apps.backend.app."):
            candidate = BACKEND_ROOT / (module_path.replace(".", "/") + ".py")
            if candidate.exists():
                return candidate
    default_router = module_dir / "api" / "router.py"
    if default_router.exists():
        return default_router
    return None


def parse_api_endpoints(
    router_file: Path, mount_prefix: str, bootstrap_scope: str
) -> dict[str, set[str]]:
    try:
        text = router_file.read_text(encoding="utf-8")
    except OSError:
        return {}

    endpoints: dict[str, set[str]] = defaultdict(set)
    prefix = mount_prefix if bootstrap_scope == "api" else ""
    for match in DECORATOR_RE.finditer(text):
        method = match.group("method").upper()
        raw_path = match.group("path").strip()
        if not raw_path:
            raw_path = "/"
        if not raw_path.startswith("/"):
            raw_path = f"/{raw_path}"

        if prefix:
            if raw_path == "/":
                effective = prefix
            else:
                effective = f"{prefix.rstrip('/')}{raw_path}"
        else:
            effective = raw_path

        endpoints[effective].add(method)
    return endpoints


def compute_instability_metrics(
    dependency_graph: dict[str, Any],
    module_names: list[str],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    fan_out: dict[str, set[str]] = {name: set() for name in module_names}
    fan_in: dict[str, set[str]] = {name: set() for name in module_names}

    for edge in dependency_graph.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")
        if source not in fan_out or target not in fan_in or source == target:
            continue
        fan_out[source].add(target)
        fan_in[target].add(source)

    metrics: dict[str, dict[str, Any]] = {}
    for name in module_names:
        out_count = len(fan_out[name])
        in_count = len(fan_in[name])
        denom = out_count + in_count
        instability = (out_count / denom) if denom else 0.0
        metrics[name] = {
            "fan_in": in_count,
            "fan_out": out_count,
            "instability": round(instability, 4),
        }

    ranking = sorted(
        (
            {
                "module": name,
                "fan_in": metrics[name]["fan_in"],
                "fan_out": metrics[name]["fan_out"],
                "instability": metrics[name]["instability"],
            }
            for name in module_names
        ),
        key=lambda item: (item["instability"], item["fan_out"], -item["fan_in"], item["module"]),
        reverse=True,
    )

    return metrics, ranking


def build_index_payload(
    system_name: str, modules_root: Path, dependency_graph: dict[str, Any]
) -> dict[str, Any]:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    modules_block: dict[str, Any] = {}
    specs = list(iter_modules(enabled_only=False))
    metrics_by_module, instability_ranking = compute_instability_metrics(
        dependency_graph=dependency_graph,
        module_names=[spec.name for spec in specs],
    )

    for spec in specs:
        module_dir = modules_root / spec.name
        router_path = resolve_router_path(spec.router_import, module_dir)
        domain_path = module_dir / "domain"
        metrics = metrics_by_module.get(spec.name, {"fan_in": 0, "fan_out": 0, "instability": 0.0})
        module_record: dict[str, Any] = {
            "domain_group": spec.domain,
            "bounded_context": BOUNDED_CONTEXT_ALIASES.get(spec.name, spec.name),
            "layer": "domain" if domain_path.exists() else None,
            "enabled": spec.enabled,
            "bootstrap_scope": spec.bootstrap_scope,
            "domain": relpath(domain_path) if domain_path.exists() else None,
            "services": service_hint(module_dir),
            "api": relpath(router_path) if router_path else None,
            "mount_prefix": spec.mount_prefix if spec.bootstrap_scope == "api" else "",
            "mount_tags": list(spec.mount_tags),
            "fan_in": metrics["fan_in"],
            "fan_out": metrics["fan_out"],
            "instability": metrics["instability"],
        }
        if spec.notes:
            module_record["notes"] = spec.notes
        modules_block[spec.name] = module_record

    return {
        "system": system_name,
        "generated_at": generated_at,
        "backend": {
            "path": "apps/backend/app",
            "module_registry": "apps/backend/app/core/module_registry.py",
            "modules": modules_block,
        },
        "architecture_health": {
            "most_unstable_modules": instability_ranking[:10],
        },
    }


def build_dependencies_payload(
    system_name: str,
    dependency_graph: dict[str, Any],
    module_names: list[str],
) -> dict[str, Any]:
    deps: dict[str, set[str]] = {name: set() for name in module_names}
    edges = dependency_graph.get("edges", [])
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if source in deps and target in deps:
            deps[source].add(target)

    modules_block: dict[str, Any] = {}
    for name in module_names:
        modules_block[name] = {"depends_on": sorted(deps[name])}

    return {
        "system": system_name,
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "reports/module_dependency_graph.json",
        "modules": modules_block,
    }


def build_api_map_payload(system_name: str, modules_root: Path) -> tuple[dict[str, Any], int]:
    modules_block: dict[str, Any] = {}
    endpoint_count = 0

    for spec in iter_modules(enabled_only=False):
        module_dir = modules_root / spec.name
        router_file = resolve_router_path(spec.router_import, module_dir)
        if not router_file:
            modules_block[spec.name] = {}
            continue

        endpoints = parse_api_endpoints(router_file, spec.mount_prefix, spec.bootstrap_scope)
        service_path = service_hint(module_dir)
        router_rel = relpath(router_file)
        module_endpoints: dict[str, Any] = {}
        for endpoint in sorted(endpoints.keys()):
            module_endpoints[endpoint] = {
                "router": router_rel,
                "methods": sorted(endpoints[endpoint]),
                "service": service_path,
            }
            endpoint_count += 1

        modules_block[spec.name] = module_endpoints

    payload = {
        "system": system_name,
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "modules": modules_block,
    }
    return payload, endpoint_count


def build_entrypoints_payload(system_name: str) -> dict[str, Any]:
    workers_path = Path("apps/backend/workers")
    celery_path = Path("apps/backend/app/core/celery")
    worker_entry = workers_path.as_posix() if workers_path.exists() else celery_path.as_posix()

    return {
        "system": system_name,
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "backend_start": {
            "file": "apps/backend/app/main.py",
        },
        "api_router": {
            "file": "apps/backend/app/api/router.py",
        },
        "module_registry": {
            "file": "apps/backend/app/core/module_registry.py",
        },
        "workers": {
            "path": worker_entry,
        },
        "architecture_reports": {
            "command": "make architecture-report",
            "outputs": [
                "reports/architecture_map.md",
                "reports/module_dependencies.md",
                "reports/module_health_report.md",
                "reports/domain_overlap_report.md",
                "reports/migration_domain_inventory.md",
                "reports/architecture_index_visual_report.md",
                "docs/AI_ARCHITECTURE_GRAPH.yaml",
                "docs/AI_DOMAIN_KERNEL.md",
                "reports/ai_architecture_graph_visual_report.md",
                "reports/ai_domain_kernel_visual_report.md",
                "reports/domain_dependency_guardrail_report.md",
            ],
        },
    }


def collect_domain_groups(index_payload: dict[str, Any]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    modules = index_payload["backend"]["modules"]
    for module_name, module_data in modules.items():
        groups[module_data["domain_group"]].append(module_name)
    return {domain: sorted(names) for domain, names in sorted(groups.items())}


def build_repository_map_payload(system_name: str, index_payload: dict[str, Any]) -> dict[str, Any]:
    domain_groups = collect_domain_groups(index_payload)
    domains_block: dict[str, Any] = {}
    for domain, modules in domain_groups.items():
        domains_block[domain] = {
            "path": "apps/backend/app/modules",
            "modules": modules,
        }

    return {
        "system": {
            "name": system_name,
        },
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "backend": {
            "path": "apps/backend/app",
            "domains": domains_block,
        },
        "platform": {
            "api": {"path": "apps/backend/app/api"},
            "core": {"path": "apps/backend/app/core"},
            "module_registry": {"file": "apps/backend/app/core/module_registry.py"},
            "scripts_architecture": {"path": "scripts/architecture"},
            "scripts_guardrails": {"path": "scripts/guardrails"},
        },
    }


def build_system_overview_md(
    system_name: str,
    index_payload: dict[str, Any],
    dependency_graph: dict[str, Any],
    endpoint_count: int,
) -> str:
    domain_groups = collect_domain_groups(index_payload)
    module_count = len(index_payload["backend"]["modules"])
    edge_count = len(dependency_graph.get("edges", []))
    cycles = len(dependency_graph.get("cycles", []))
    lines = [
        "# System Overview",
        "",
        f"- System: `{system_name}`",
        f"- Modules: **{module_count}**",
        f"- Domain groups: **{len(domain_groups)}**",
        f"- Dependency edges: **{edge_count}**",
        f"- Circular groups: **{cycles}**",
        f"- API endpoints mapped: **{endpoint_count}**",
        "",
        "## Domain Groups",
        "",
    ]
    for domain, modules in domain_groups.items():
        lines.append(f"- `{domain}`: {len(modules)} modules")
    lines.append("")
    lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
    lines.append("")
    return "\n".join(lines)


def build_backend_architecture_md(index_payload: dict[str, Any]) -> str:
    domain_groups = collect_domain_groups(index_payload)
    lines = [
        "# Backend Architecture",
        "",
        "Backend root: `apps/backend/app`",
        "",
        "## Core Entry Points",
        "",
        "- `apps/backend/app/main.py`",
        "- `apps/backend/app/api/router.py`",
        "- `apps/backend/app/core/module_registry.py`",
        "",
        "## Domain Federation",
        "",
    ]
    for domain, modules in domain_groups.items():
        lines.append(f"### {domain}")
        lines.append("")
        lines.append(", ".join(f"`{name}`" for name in modules) if modules else "-")
        lines.append("")
    lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
    lines.append("")
    return "\n".join(lines)


def build_domain_map_md(index_payload: dict[str, Any], dependencies_payload: dict[str, Any]) -> str:
    domain_groups = collect_domain_groups(index_payload)
    deps = dependencies_payload.get("modules", {})
    lines = [
        "# Domain Map",
        "",
        "## Bounded Contexts",
        "",
    ]
    for domain, modules in domain_groups.items():
        lines.append(f"### {domain}")
        lines.append("")
        lines.append(f"- Modules: {', '.join(f'`{m}`' for m in modules)}")
        cross_dep_count = 0
        for module in modules:
            module_deps = deps.get(module, {}).get("depends_on", [])
            cross_dep_count += len(module_deps)
        lines.append(f"- Declared cross-module deps: **{cross_dep_count}**")
        lines.append("")
    lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
    lines.append("")
    return "\n".join(lines)


def build_api_entrypoints_md(api_map_payload: dict[str, Any]) -> str:
    modules = api_map_payload.get("modules", {})
    lines = [
        "# API Entrypoints",
        "",
        "## Routes by Module",
        "",
    ]
    for module in sorted(modules.keys()):
        endpoints = modules[module]
        lines.append(f"### {module}")
        lines.append("")
        if not endpoints:
            lines.append("- No direct decorated endpoints found in `api/router.py`.")
            lines.append("")
            continue
        lines.append("| Endpoint | Methods | Router |")
        lines.append("| --- | --- | --- |")
        for endpoint, data in sorted(endpoints.items()):
            methods = ", ".join(data.get("methods", []))
            router = data.get("router", "")
            lines.append(f"| `{endpoint}` | `{methods}` | `{router}` |")
        lines.append("")
    lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
    lines.append("")
    return "\n".join(lines)


def build_data_flow_md(dependency_graph: dict[str, Any]) -> str:
    edges = dependency_graph.get("edges", [])
    lines = [
        "# Data Flow",
        "",
        "## Module Dependency Flow (Top 25)",
        "",
    ]
    if not edges:
        lines.append("- No dependency edges available.")
    else:
        lines.append("| Source | Target | Weight |")
        lines.append("| --- | --- | ---: |")
        for edge in edges[:25]:
            lines.append(
                f"| `{edge.get('source')}` | `{edge.get('target')}` | {edge.get('weight')} |"
            )
    lines.append("")
    lines.append("## Mermaid")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for edge in edges[:25]:
        source = edge.get("source")
        target = edge.get("target")
        weight = edge.get("weight")
        if source and target:
            lines.append(f"  {source} -->|{weight}| {target}")
    lines.append("```")
    lines.append("")
    lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
    lines.append("")
    return "\n".join(lines)


def build_ai_context_md() -> str:
    lines = [
        "# AI Context Entry Point",
        "",
        "Este arquivo define a ordem obrigatoria de leitura para agentes de IA.",
        "",
        "## Start Here",
        "",
        "1. `docs/tree.md`",
        "2. `docs/AI_BOOTSTRAP_PROMPT.md`",
        "3. `docs/AI_ARCHITECTURE_GUIDE.md`",
        "4. `docs/AI_DOMAIN_KERNEL.md`",
        "5. `docs/AI_ARCHITECTURE_GRAPH.yaml`",
        "6. `docs/architecture/domain_dependency_policy.yaml`",
        "7. `docs/architecture/entrypoints/SYSTEM_OVERVIEW.md`",
        "8. `docs/architecture/REPOSITORY_MAP.yaml`",
        "9. `docs/architecture/entrypoints/DOMAIN_MAP.md`",
        "10. `docs/architecture/entrypoints/API_ENTRYPOINTS.md`",
        "11. `docs/architecture/domains/<domain>/ARCHITECTURE.md` (quando houver dominio alvo).",
        "12. `apps/backend/app/modules/<module>/ARCHITECTURE.md` (quando houver modulo alvo).",
        "13. `/.ai/AI_ENTRYPOINTS.yaml`",
        "14. `docs/architecture/ARCHITECTURE_INDEX.yaml`",
        "15. `docs/architecture/ARCHITECTURE_DEPENDENCIES.yaml`",
        "",
        "## Rules",
        "",
        "- Dominios devem usar dependencias explicitas e evitar ciclos.",
        "- Bootstrap de modulos deve usar apenas `app/core/module_registry.py`.",
        "- Antes de alterar arquitetura, execute `make sovereign-ritual`.",
        "- Sempre iniciar por `docs/AI_DOMAIN_KERNEL.md` em tarefas estruturais.",
        "- Imports entre modulos devem respeitar `docs/AI_ARCHITECTURE_GRAPH.yaml` e `docs/architecture/domain_dependency_policy.yaml`.",
        "- Escopo de leitura de IA deve respeitar `/.ai/AI_FILE_SCOPE.yaml`.",
        "- Use `bash scripts/ai/bootstrap_context.sh` para extrair contexto rapido.",
        "",
        "_Auto-generated by `scripts/architecture/generate_architecture_index.py`._",
        "",
    ]
    return "\n".join(lines)


def build_domain_architecture_docs(
    index_payload: dict[str, Any],
    dependencies_payload: dict[str, Any],
    api_map_payload: dict[str, Any],
) -> dict[str, str]:
    domain_groups = collect_domain_groups(index_payload)
    modules_info = index_payload["backend"]["modules"]
    module_to_domain = {
        module_name: module_data["domain_group"]
        for module_name, module_data in modules_info.items()
    }
    module_deps = dependencies_payload.get("modules", {})
    api_modules = api_map_payload.get("modules", {})

    docs: dict[str, str] = {}
    for domain, modules in domain_groups.items():
        external_domains: set[str] = set()
        endpoint_lines: list[str] = []
        for module in modules:
            deps = module_deps.get(module, {}).get("depends_on", [])
            for dep in deps:
                dep_domain = module_to_domain.get(dep)
                if dep_domain and dep_domain != domain:
                    external_domains.add(dep_domain)

            endpoints = api_modules.get(module, {})
            for endpoint, data in sorted(endpoints.items()):
                methods = ",".join(data.get("methods", []))
                endpoint_lines.append(f"- `{methods}` `{endpoint}` ({module})")

        lines = [
            f"# {domain.title()} Domain Architecture",
            "",
            "Responsabilidade:",
            f"- Coordenar capacidades do domínio `{domain}` no SILA.",
            "",
            "Módulos:",
        ]
        lines.extend(f"- `{module}`" for module in modules)
        lines.append("")

        lines.append("Dependências externas permitidas (observadas):")
        if external_domains:
            lines.extend(f"- `{item}`" for item in sorted(external_domains))
        else:
            lines.append("- Nenhuma dependência externa observada.")
        lines.append("")

        lines.append("Dependências proibidas por padrão:")
        lines.append("- Qualquer domínio não listado acima (exceto o próprio domínio).")
        lines.append("")

        lines.append("Entradas de API (amostra):")
        if endpoint_lines:
            lines.extend(endpoint_lines[:40])
        else:
            lines.append("- Sem endpoints mapeados para este domínio.")
        lines.append("")
        lines.append("_Auto-generated by `scripts/architecture/generate_architecture_index.py`._")
        lines.append("")

        docs[f"{domain}/ARCHITECTURE.md"] = "\n".join(lines)

    return docs


def build_ai_bootstrap_prompt_md() -> str:
    lines = [
        "# AI Bootstrap Prompt",
        "",
        "Ritual de operacao soberana antes de qualquer mudanca estrutural (feature nova, refactor, novo modulo, mudanca arquitetural):",
        "",
        "1. Sincronizacao de terreno (GPS):",
        "   - Ler `docs/tree.md` e usar como fonte unica para localizar diretorios.",
        "2. Auditoria de saude (Raio-X):",
        "   - Executar `make architecture-report && bash scripts/guardrails/run_all_guardrails.sh && python3 scripts/guardrails/check_domain_dependencies.py --repo-root .`.",
        "   - Revisar `reports/` antes de tocar no codigo.",
        "3. Alinhamento constitucional (Lei):",
        "   - Ler `docs/AI_ARCHITECTURE_GRAPH.yaml`.",
        "   - Ler `docs/architecture/domain_dependency_policy.yaml`.",
        "   - Ler `docs/AI_DOMAIN_KERNEL.md`.",
        "4. Execucao tecnica (Missao):",
        "   - So depois dos passos acima executar build/refactor/testes.",
        "   - Se criar arquivo novo, sincronizar `docs/tree.md`.",
        "   - Se criar import novo, validar contra a policy YAML.",
        "",
        "Regra dura:",
        "- Nunca violar separacao de camadas (domain/application/infrastructure/api).",
        "- Nunca contornar `app/core/module_registry.py` no bootstrap de modulos.",
        "- `core` nao importa `modules` fora das excecoes declaradas em policy.",
        "- Bloquear ciclos de dependencia entre dominios.",
        "- Sempre registrar evidencias before/after em `reports/`.",
        "",
        "Use tambem:",
        "- `bash scripts/ai/bootstrap_context.sh` para montar contexto rapido.",
        "- `make sovereign-ritual` para executar o protocolo completo em um unico alvo.",
        "",
        "_Auto-generated by `scripts/architecture/generate_architecture_index.py`._",
        "",
    ]
    return "\n".join(lines)


def build_visual_report(
    system_name: str,
    module_names: list[str],
    dependency_graph: dict[str, Any],
    endpoint_count: int,
    index_path: Path,
    deps_path: Path,
    api_map_path: Path,
    entrypoints_path: Path,
    repository_map_path: Path,
    ai_context_path: Path,
    ai_bootstrap_prompt_path: Path,
    architecture_entrypoints_dir: Path,
    domain_architecture_dir: Path,
) -> str:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    edges = dependency_graph.get("edges", [])
    cycles = dependency_graph.get("cycles", [])

    lines: list[str] = []
    lines.append("# Architecture Index Visual Report")
    lines.append("")
    lines.append(f"- System: `{system_name}`")
    lines.append(f"- Generated at: `{generated_at}`")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- `{index_path.as_posix()}`")
    lines.append(f"- `{deps_path.as_posix()}`")
    lines.append(f"- `{api_map_path.as_posix()}`")
    lines.append(f"- `{entrypoints_path.as_posix()}`")
    lines.append(f"- `{repository_map_path.as_posix()}`")
    lines.append(f"- `{ai_context_path.as_posix()}`")
    lines.append(f"- `{ai_bootstrap_prompt_path.as_posix()}`")
    lines.append("- `docs/AI_ARCHITECTURE_GRAPH.yaml`")
    lines.append("- `docs/AI_DOMAIN_KERNEL.md`")
    lines.append("- `reports/ai_architecture_graph_visual_report.md`")
    lines.append("- `reports/ai_domain_kernel_visual_report.md`")
    lines.append("- `reports/domain_dependency_guardrail_report.md`")
    lines.append(f"- `{architecture_entrypoints_dir.as_posix()}/`")
    lines.append(f"- `{domain_architecture_dir.as_posix()}/**/ARCHITECTURE.md`")
    lines.append("- `apps/backend/app/modules/*/ARCHITECTURE.md`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules indexed: **{len(module_names)}**")
    lines.append(f"- Dependency edges: **{len(edges)}**")
    lines.append(f"- Circular dependency groups: **{len(cycles)}**")
    lines.append(f"- API endpoints mapped: **{endpoint_count}**")
    lines.append("")
    lines.append("## Dependency Graph (Top 30 Edges)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for edge in edges[:30]:
        source = edge.get("source")
        target = edge.get("target")
        weight = edge.get("weight")
        if not source or not target:
            continue
        lines.append(f"  {source} -->|{weight}| {target}")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    text = dump_yaml(payload).rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate architecture index artifacts.")
    parser.add_argument("--system", default="sila-system", help="System identifier.")
    parser.add_argument("--modules-root", default="apps/backend/app/modules", help="Modules root.")
    parser.add_argument(
        "--dependency-json",
        default="reports/module_dependency_graph.json",
        help="Dependency graph JSON path.",
    )
    parser.add_argument(
        "--refresh-dependencies",
        action="store_true",
        help="Regenerate dependency graph before generating index files.",
    )
    parser.add_argument(
        "--index-output",
        default="docs/architecture/ARCHITECTURE_INDEX.yaml",
        help="Index output path.",
    )
    parser.add_argument(
        "--dependencies-output",
        default="docs/architecture/ARCHITECTURE_DEPENDENCIES.yaml",
        help="Dependencies output path.",
    )
    parser.add_argument(
        "--api-map-output", default="docs/architecture/API_MAP.yaml", help="API map output path."
    )
    parser.add_argument(
        "--entrypoints-output", default=".ai/AI_ENTRYPOINTS.yaml", help="Entrypoints output path."
    )
    parser.add_argument(
        "--repository-map-output",
        default="docs/architecture/REPOSITORY_MAP.yaml",
        help="Repository semantic map output path.",
    )
    parser.add_argument(
        "--ai-context-output",
        default="docs/AI_CONTEXT.md",
        help="AI context gateway output path.",
    )
    parser.add_argument(
        "--ai-bootstrap-prompt-output",
        default="docs/AI_BOOTSTRAP_PROMPT.md",
        help="AI bootstrap prompt output path.",
    )
    parser.add_argument(
        "--architecture-entrypoints-dir",
        default="docs/architecture/entrypoints",
        help="Architecture entrypoint docs directory.",
    )
    parser.add_argument(
        "--domain-architecture-dir",
        default="docs/architecture/domains",
        help="Domain architecture docs directory.",
    )
    parser.add_argument(
        "--visual-report-output",
        default="reports/architecture_index_visual_report.md",
        help="Visual report output path.",
    )
    args = parser.parse_args()

    modules_root = (REPO_ROOT / args.modules_root).resolve()
    dependency_json = (REPO_ROOT / args.dependency_json).resolve()
    index_output = (REPO_ROOT / args.index_output).resolve()
    dependencies_output = (REPO_ROOT / args.dependencies_output).resolve()
    api_map_output = (REPO_ROOT / args.api_map_output).resolve()
    entrypoints_output = (REPO_ROOT / args.entrypoints_output).resolve()
    repository_map_output = (REPO_ROOT / args.repository_map_output).resolve()
    ai_context_output = (REPO_ROOT / args.ai_context_output).resolve()
    ai_bootstrap_prompt_output = (REPO_ROOT / args.ai_bootstrap_prompt_output).resolve()
    architecture_entrypoints_dir = (REPO_ROOT / args.architecture_entrypoints_dir).resolve()
    domain_architecture_dir = (REPO_ROOT / args.domain_architecture_dir).resolve()
    visual_report_output = (REPO_ROOT / args.visual_report_output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    if args.refresh_dependencies or not dependency_json.exists():
        run_dependency_scan(modules_root, dependency_json)

    dependency_graph = read_dependency_graph(dependency_json)

    index_payload = build_index_payload(args.system, modules_root, dependency_graph)
    module_names = list(index_payload["backend"]["modules"].keys())
    dependencies_payload = build_dependencies_payload(args.system, dependency_graph, module_names)
    api_map_payload, endpoint_count = build_api_map_payload(args.system, modules_root)
    entrypoints_payload = build_entrypoints_payload(args.system)
    repository_map_payload = build_repository_map_payload(args.system, index_payload)

    system_overview_md = build_system_overview_md(
        args.system,
        index_payload,
        dependency_graph,
        endpoint_count,
    )
    backend_architecture_md = build_backend_architecture_md(index_payload)
    domain_map_md = build_domain_map_md(index_payload, dependencies_payload)
    api_entrypoints_md = build_api_entrypoints_md(api_map_payload)
    data_flow_md = build_data_flow_md(dependency_graph)
    ai_context_md = build_ai_context_md()
    ai_bootstrap_prompt_md = build_ai_bootstrap_prompt_md()
    domain_docs = build_domain_architecture_docs(
        index_payload, dependencies_payload, api_map_payload
    )

    for out in (
        index_output,
        dependencies_output,
        api_map_output,
        entrypoints_output,
        repository_map_output,
        ai_context_output,
        ai_bootstrap_prompt_output,
        visual_report_output,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)
    architecture_entrypoints_dir.mkdir(parents=True, exist_ok=True)
    domain_architecture_dir.mkdir(parents=True, exist_ok=True)

    write_yaml(index_output, index_payload)
    write_yaml(dependencies_output, dependencies_payload)
    write_yaml(api_map_output, api_map_payload)
    write_yaml(entrypoints_output, entrypoints_payload)
    write_yaml(repository_map_output, repository_map_payload)

    (architecture_entrypoints_dir / "SYSTEM_OVERVIEW.md").write_text(
        system_overview_md,
        encoding="utf-8",
    )
    (architecture_entrypoints_dir / "BACKEND_ARCHITECTURE.md").write_text(
        backend_architecture_md,
        encoding="utf-8",
    )
    (architecture_entrypoints_dir / "DOMAIN_MAP.md").write_text(
        domain_map_md,
        encoding="utf-8",
    )
    (architecture_entrypoints_dir / "API_ENTRYPOINTS.md").write_text(
        api_entrypoints_md,
        encoding="utf-8",
    )
    (architecture_entrypoints_dir / "DATA_FLOW.md").write_text(
        data_flow_md,
        encoding="utf-8",
    )
    ai_context_output.write_text(ai_context_md, encoding="utf-8")
    ai_bootstrap_prompt_output.write_text(ai_bootstrap_prompt_md, encoding="utf-8")
    for relative_doc_path, content in domain_docs.items():
        output_file = domain_architecture_dir / relative_doc_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding="utf-8")

    visual_report = build_visual_report(
        args.system,
        module_names,
        dependency_graph,
        endpoint_count,
        index_output.relative_to(REPO_ROOT),
        dependencies_output.relative_to(REPO_ROOT),
        api_map_output.relative_to(REPO_ROOT),
        entrypoints_output.relative_to(REPO_ROOT),
        repository_map_output.relative_to(REPO_ROOT),
        ai_context_output.relative_to(REPO_ROOT),
        ai_bootstrap_prompt_output.relative_to(REPO_ROOT),
        architecture_entrypoints_dir.relative_to(REPO_ROOT),
        domain_architecture_dir.relative_to(REPO_ROOT),
    )
    visual_report_output.write_text(visual_report, encoding="utf-8")

    print(f"Generated: {index_output}")
    print(f"Generated: {dependencies_output}")
    print(f"Generated: {api_map_output}")
    print(f"Generated: {entrypoints_output}")
    print(f"Generated: {repository_map_output}")
    print(f"Generated: {ai_context_output}")
    print(f"Generated: {ai_bootstrap_prompt_output}")
    print(f"Generated: {architecture_entrypoints_dir / 'SYSTEM_OVERVIEW.md'}")
    print(f"Generated: {architecture_entrypoints_dir / 'BACKEND_ARCHITECTURE.md'}")
    print(f"Generated: {architecture_entrypoints_dir / 'DOMAIN_MAP.md'}")
    print(f"Generated: {architecture_entrypoints_dir / 'API_ENTRYPOINTS.md'}")
    print(f"Generated: {architecture_entrypoints_dir / 'DATA_FLOW.md'}")
    for relative_doc_path in sorted(domain_docs.keys()):
        print(f"Generated: {domain_architecture_dir / relative_doc_path}")
    print(f"Generated: {visual_report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
