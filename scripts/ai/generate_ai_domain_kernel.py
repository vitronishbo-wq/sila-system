#!/usr/bin/env python3
"""Generate AI Domain Kernel document for fast architecture navigation."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.module_registry import iter_modules  # noqa: E402
from generate_architecture_graph import parse_sectioned_lists  # noqa: E402


DOMAIN_METADATA: dict[str, tuple[str, str]] = {
    "governance": (
        "Governance e Estado",
        "Administracao publica, justica, planeamento e operacao estatal.",
    ),
    "economy": (
        "Economia e Financas",
        "Gestao fiscal, economia produtiva e comercio.",
    ),
    "social": (
        "Capital Humano e Social",
        "Educacao, saude, trabalho e politicas sociais ao cidadao.",
    ),
    "infrastructure": (
        "Infraestrutura Nacional",
        "Infraestrutura fisica, energia, telecom e logistica.",
    ),
    "environment": (
        "Ambiente e Recursos Naturais",
        "Sustentabilidade, recursos naturais e monitorizacao ambiental.",
    ),
    "security": (
        "Seguranca e Protecao",
        "Seguranca publica, protecao civil e garantias ao consumidor.",
    ),
    "identity": (
        "Identidade e Registro Civil",
        "Identidade legal do cidadao e protecao de dados pessoais.",
    ),
    "core_system": (
        "Core Platform",
        "Servicos transversais de plataforma, workflow e operacoes.",
    ),
}

DOMAIN_ORDER = (
    "identity",
    "governance",
    "economy",
    "social",
    "infrastructure",
    "environment",
    "security",
    "core_system",
)


def relpath(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def parse_graph_yaml(graph_path: Path) -> tuple[str, str, dict[str, dict[str, object]]]:
    """Parse minimal fields from AI architecture graph YAML without external deps."""
    lines = graph_path.read_text(encoding="utf-8").splitlines()
    system = "sila-system"
    generated_at = ""
    modules: dict[str, dict[str, object]] = {}

    current_module: str | None = None
    in_depends_on = False
    in_modules_block = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("system:"):
            system = line.split(":", 1)[1].strip().strip("'")
            continue
        if line.startswith("generated_at:"):
            generated_at = line.split(":", 1)[1].strip().strip("'")
            continue
        if line == "modules:":
            in_modules_block = True
            current_module = None
            in_depends_on = False
            continue
        if not in_modules_block:
            continue

        if line.startswith("  ") and not line.startswith("    ") and line.endswith(":"):
            module_name = line.strip()[:-1]
            current_module = module_name
            modules[current_module] = {"domain_group": "unknown", "depends_on": []}
            in_depends_on = False
            continue

        if not current_module:
            continue

        if line.startswith("    domain_group:"):
            domain = line.split(":", 1)[1].strip().strip("'")
            modules[current_module]["domain_group"] = domain
            in_depends_on = False
            continue

        if line.startswith("    depends_on:"):
            in_depends_on = True
            continue

        if in_depends_on and line.startswith("      - "):
            dep = line.split("- ", 1)[1].strip().strip("'")
            if dep:
                deps = modules[current_module]["depends_on"]
                if isinstance(deps, list):
                    deps.append(dep)
            continue

        if line.startswith("    ") and not line.startswith("      "):
            in_depends_on = False

    for module_data in modules.values():
        deps = module_data.get("depends_on", [])
        if isinstance(deps, list):
            module_data["depends_on"] = sorted({item for item in deps if isinstance(item, str)})
        else:
            module_data["depends_on"] = []
    return system, generated_at, modules


def section_text(doc_text: str, heading: str) -> str:
    lines = doc_text.splitlines()
    inside = False
    bucket: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        if line == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            bucket.append(line)
    return "\n".join(bucket).strip()


def read_module_doc(module_dir: Path) -> dict[str, object]:
    doc_path = module_dir / "ARCHITECTURE.md"
    if not doc_path.exists():
        return {
            "has_doc": False,
            "purpose": "",
            "core_responsibilities": [],
            "entities": [],
            "use_cases": [],
            "api": [],
        }
    text = doc_path.read_text(encoding="utf-8")
    parsed = parse_sectioned_lists(text)

    purpose = section_text(text, "## Purpose").splitlines()
    purpose_line = ""
    for line in purpose:
        cleaned = line.strip()
        if cleaned:
            purpose_line = cleaned
            break

    responsibilities_text = section_text(text, "## Core Responsibilities")
    core_responsibilities = [
        line.split("- ", 1)[1].strip()
        for line in responsibilities_text.splitlines()
        if line.strip().startswith("- ")
    ]

    return {
        "has_doc": True,
        "purpose": purpose_line,
        "core_responsibilities": core_responsibilities,
        "entities": parsed.get("entities", []),
        "use_cases": parsed.get("use_cases", []),
        "api": parsed.get("api", []),
    }


def build_domain_kernel(
    system: str,
    generated_at: str,
    modules_graph: dict[str, dict[str, object]],
    modules_root: Path,
) -> tuple[str, dict[str, object]]:
    registry_order = [spec.name for spec in iter_modules(enabled_only=False)]
    module_names = [name for name in registry_order if name in modules_graph]
    module_set = set(module_names)
    module_names.extend(
        sorted(name for name in modules_graph.keys() if name not in module_set)
    )
    module_details: dict[str, dict[str, object]] = {}

    for module_name in module_names:
        module_dir = modules_root / module_name
        module_details[module_name] = read_module_doc(module_dir)

    domain_modules: dict[str, list[str]] = defaultdict(list)
    for module_name in module_names:
        domain_group = str(modules_graph[module_name].get("domain_group", "unknown"))
        domain_modules[domain_group].append(module_name)
    for domain in domain_modules:
        domain_modules[domain] = sorted(domain_modules[domain])

    cross_domain: dict[tuple[str, str], int] = defaultdict(int)
    for source, data in modules_graph.items():
        source_domain = str(data.get("domain_group", "unknown"))
        deps = data.get("depends_on", [])
        if not isinstance(deps, list):
            continue
        for target in deps:
            if target not in modules_graph:
                continue
            target_domain = str(modules_graph[target].get("domain_group", "unknown"))
            if source_domain != target_domain:
                cross_domain[(source_domain, target_domain)] += 1

    module_count = len(module_names)
    cross_domain_edges = sum(cross_domain.values())
    domain_count = len([domain for domain in domain_modules if domain != "unknown"])
    doc_coverage = sum(1 for m in module_names if module_details[m]["has_doc"])

    lines: list[str] = []
    lines.append("# AI Domain Kernel")
    lines.append("")
    lines.append(f"Sistema: {system}")
    lines.append("Arquitetura:")
    lines.append("- DDD")
    lines.append("- Clean Architecture")
    lines.append("- Modular Monorepo")
    lines.append("")
    lines.append("Root:")
    lines.append("apps/backend/app/modules")
    lines.append("")
    lines.append(f"Gerado em: `{generated_at}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# Dominios do Sistema")
    lines.append("")

    for domain in DOMAIN_ORDER:
        modules = domain_modules.get(domain, [])
        if not modules:
            continue
        title, responsibility = DOMAIN_METADATA.get(
            domain,
            (domain.replace("_", " ").title(), "Responsabilidade federada do dominio."),
        )
        lines.append(f"## {title}")
        lines.append("")
        lines.append("Modulos:")
        for module_name in modules:
            lines.append(f"- {module_name}")
        lines.append("")
        lines.append("Responsabilidade:")
        lines.append(responsibility)
        lines.append("")

        sample_entities: list[str] = []
        sample_use_cases: list[str] = []
        for module_name in modules:
            sample_entities.extend(module_details[module_name]["entities"][:2])  # type: ignore[index]
            sample_use_cases.extend(module_details[module_name]["use_cases"][:2])  # type: ignore[index]
        entity_preview = ", ".join(sample_entities[:4]) if sample_entities else "n/a"
        use_case_preview = ", ".join(sample_use_cases[:4]) if sample_use_cases else "n/a"
        lines.append(f"Sinais do dominio: entidades `{entity_preview}`; use cases `{use_case_preview}`.")
        lines.append("")
        lines.append("---")
        lines.append("")

    unknown_modules = domain_modules.get("unknown", [])
    if unknown_modules:
        lines.append("## Unknown Domain")
        lines.append("")
        lines.append("Modulos:")
        for module_name in unknown_modules:
            lines.append(f"- {module_name}")
        lines.append("")
        lines.append("Responsabilidade:")
        lines.append("Modulos sem federacao explicita no module registry.")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("# Relacoes Entre Dominios")
    lines.append("")
    lines.append("| Source Domain | Target Domain | Edges |")
    lines.append("| --- | --- | ---: |")
    for (source_domain, target_domain), count in sorted(
        cross_domain.items(), key=lambda item: item[1], reverse=True
    ):
        lines.append(f"| `{source_domain}` | `{target_domain}` | {count} |")
    if not cross_domain:
        lines.append("| `n/a` | `n/a` | 0 |")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("# Camadas Arquiteturais")
    lines.append("")
    lines.append("Todos os modulos devem seguir:")
    lines.append("")
    lines.append("- `domain/`")
    lines.append("- `application/`")
    lines.append("- `infrastructure/`")
    lines.append("- `api/`")
    lines.append("")
    lines.append("Models ORM:")
    lines.append("")
    lines.append("- `infrastructure/models/`")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("# Regras Arquiteturais Globais")
    lines.append("")
    lines.append("1. Dominios nao importam infrastructure de outros dominios.")
    lines.append("2. Comunicacao entre dominios via application layer.")
    lines.append("3. Domain nao depende de frameworks.")
    lines.append("4. API depende apenas de application/domain.")
    lines.append("5. ORM models ficam em infrastructure/models.")
    lines.append("6. Cada modulo deve ter ARCHITECTURE.md.")
    lines.append("7. Dependencias observadas devem existir em docs/AI_ARCHITECTURE_GRAPH.yaml.")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("# Navegacao para AI Agents")
    lines.append("")
    lines.append("Sequencia obrigatoria:")
    lines.append("1. Ler `docs/AI_DOMAIN_KERNEL.md`.")
    lines.append("2. Ler `docs/AI_ARCHITECTURE_GRAPH.yaml`.")
    lines.append("3. Ler `apps/backend/app/modules/<module>/ARCHITECTURE.md`.")
    lines.append("4. So entao abrir codigo do modulo alvo.")
    lines.append("")
    lines.append("Regra operacional:")
    lines.append("- Nunca alterar multiplos dominios sem justificativa tecnica explicita.")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("# Estatisticas do Sistema")
    lines.append("")
    lines.append(f"- Modulos: **{module_count}**")
    lines.append(f"- Dominios federados: **{domain_count}**")
    lines.append(f"- Cobertura ARCHITECTURE.md: **{doc_coverage}/{module_count}**")
    lines.append(f"- Relacoes cross-domain: **{cross_domain_edges}**")
    lines.append("- Arquitetura: **DDD Modular**")
    lines.append("- Indice arquitetural: `ARCHITECTURE_INDEX.yaml`")
    lines.append("- Graph: `docs/AI_ARCHITECTURE_GRAPH.yaml`")
    lines.append("")
    lines.append(
        "_Auto-generated by `scripts/ai/generate_ai_domain_kernel.py`. "
        "Nao editar manualmente; regenerar via `make domain-kernel`._"
    )
    lines.append("")

    summary = {
        "module_count": module_count,
        "domain_count": domain_count,
        "doc_coverage": doc_coverage,
        "cross_domain_edges": cross_domain_edges,
        "domain_modules": {key: len(value) for key, value in domain_modules.items()},
        "cross_domain_matrix": {
            f"{source}->{target}": count for (source, target), count in cross_domain.items()
        },
    }
    return "\n".join(lines), summary


def render_visual_report(
    kernel_path: Path,
    summary: dict[str, object],
    output_path: Path,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    domain_modules = summary.get("domain_modules", {})
    matrix = summary.get("cross_domain_matrix", {})
    if not isinstance(domain_modules, dict):
        domain_modules = {}
    if not isinstance(matrix, dict):
        matrix = {}

    lines: list[str] = []
    lines.append("# AI Domain Kernel Visual Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Kernel: `{relpath(kernel_path)}`")
    lines.append(f"- Output: `{output_path.as_posix()}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules: **{summary.get('module_count', 0)}**")
    lines.append(f"- Domain groups: **{summary.get('domain_count', 0)}**")
    lines.append(f"- ARCHITECTURE.md coverage: **{summary.get('doc_coverage', 0)}**")
    lines.append(f"- Cross-domain edges: **{summary.get('cross_domain_edges', 0)}**")
    lines.append("")
    lines.append("## Modules by Domain")
    lines.append("")
    lines.append("| Domain | Modules |")
    lines.append("| --- | ---: |")
    for domain in sorted(domain_modules.keys()):
        lines.append(f"| `{domain}` | {domain_modules[domain]} |")
    lines.append("")
    lines.append("## Domain Relations (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for relation, count in sorted(
        ((k, v) for k, v in matrix.items() if isinstance(k, str) and isinstance(v, int)),
        key=lambda item: item[1],
        reverse=True,
    )[:40]:
        if "->" not in relation:
            continue
        source, target = relation.split("->", 1)
        lines.append(f"  {source} -->|{count}| {target}")
    if not matrix:
        lines.append("  A[\"No cross-domain edges\"]")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AI Domain Kernel document.")
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Modules root path.",
    )
    parser.add_argument(
        "--graph-yaml",
        default="docs/AI_ARCHITECTURE_GRAPH.yaml",
        help="Graph YAML input path.",
    )
    parser.add_argument(
        "--output",
        default="docs/AI_DOMAIN_KERNEL.md",
        help="Kernel markdown output path.",
    )
    parser.add_argument(
        "--visual-report-output",
        default="reports/ai_domain_kernel_visual_report.md",
        help="Visual report output path.",
    )
    args = parser.parse_args()

    modules_root = (REPO_ROOT / args.modules_root).resolve()
    graph_yaml = (REPO_ROOT / args.graph_yaml).resolve()
    output = (REPO_ROOT / args.output).resolve()
    visual_output = (REPO_ROOT / args.visual_report_output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")
    if not graph_yaml.exists():
        raise SystemExit(f"AI architecture graph not found: {graph_yaml}")

    system, generated_at, modules_graph = parse_graph_yaml(graph_yaml)
    kernel_doc, summary = build_domain_kernel(
        system=system,
        generated_at=generated_at,
        modules_graph=modules_graph,
        modules_root=modules_root,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    visual_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(kernel_doc, encoding="utf-8")
    visual_output.write_text(
        render_visual_report(output, summary, visual_output),
        encoding="utf-8",
    )

    print(f"Generated: {output}")
    print(f"Generated: {visual_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
