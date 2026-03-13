#!/usr/bin/env python3
"""Domain overlap scanner for SILA modules.

Generates a Markdown report with:
- duplicated domain concepts
- modules sharing entities
- modules sharing repositories
- cross-imports between modules
- candidate merges and recommended domain groups
"""

from __future__ import annotations

import argparse
import itertools
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
CAMEL_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|\d+")
MODULE_IMPORT_RE = re.compile(r"^app\.modules\.([a-zA-Z0-9_]+)")
CLASS_LINE_RE = re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\b")
IMPORT_FROM_LINE_RE = re.compile(r"^\s*from\s+app\.modules\.([A-Za-z0-9_]+)\b")
IMPORT_LINE_RE = re.compile(r"^\s*import\s+app\.modules\.([A-Za-z0-9_]+)\b")


SYNONYM_MAP = {
    "administracao": "governance",
    "apoio": "support",
    "assistencia": "assistance",
    "aviacao": "aviation",
    "civil": "civil",
    "comercio": "commerce",
    "consumidor": "consumer",
    "dados": "data",
    "defesa": "defense",
    "educacao": "education",
    "empresarial": "business",
    "emprego": "employment",
    "energia": "energy",
    "estatistica": "statistics",
    "familia": "family",
    "financas": "finance",
    "florestas": "forest",
    "fundiaria": "land",
    "habitacao": "housing",
    "identidade": "identity",
    "igualdade": "equality",
    "impostos": "taxation",
    "industriais": "industrial",
    "justica": "justice",
    "logistica": "logistics",
    "migracao": "migration",
    "obras": "works",
    "patrimonio": "heritage",
    "pecuaria": "livestock",
    "pescas": "fisheries",
    "petroleo": "petroleum",
    "planeamento": "planning",
    "portos": "ports",
    "primaria": "primary",
    "protecao": "protection",
    "publica": "public",
    "publicas": "public",
    "recursos": "resources",
    "registo": "registry",
    "saneamento": "sanitation",
    "saude": "health",
    "seguranca": "security",
    "servicos": "services",
    "social": "social",
    "statistics": "statistics",
    "taxpayer": "taxation",
    "telecomunicacoes": "telecom",
    "trabalho": "labor",
    "transportes": "transport",
    "turismo": "tourism",
    "urbanismo": "urbanism",
}


DOMAIN_GROUPS = {
    "governance": {
        "administracao_local",
        "arquivo_nacional",
        "bi",
        "cooperacao_internacional",
        "identidade_civil",
        "identity",
        "justica",
        "migracao",
        "planeamento",
        "protecao_dados",
        "registo_civil",
    },
    "economy": {
        "agricultura",
        "apoio_empresarial",
        "comercio_externo",
        "comercio_servicos",
        "financas",
        "financas_impostos",
        "financas_publicas",
        "industria",
        "pecuaria",
        "pescas",
        "pescas_industriais",
        "taxpayer",
        "turismo",
    },
    "social": {
        "assistencia_social",
        "ciencia_pesquisa",
        "cultura",
        "desporto",
        "educacao",
        "emprego",
        "familia",
        "igualdade",
        "juventude",
        "saude",
        "saude_primaria",
        "seguranca_social",
        "tecnologia_inovacao",
        "trabalho_inspecao",
    },
    "infrastructure": {
        "aguas_saneamento",
        "aviacao_civil",
        "energia",
        "gestao_fundiaria",
        "obras_publicas",
        "portos_logistica",
        "telecomunicacoes",
        "transportes_logistica",
        "urbanismo_habitacao",
    },
    "environment": {
        "ambiente",
        "florestas",
        "meteorologia",
        "patrimonio_cultural",
        "petroleo_gas",
        "recursos_minerais",
    },
    "security": {
        "defesa_consumidor",
        "protecao_civil",
        "seguranca_alimentar",
        "seguranca_publica",
    },
    "platform": {
        "estatistica",
        "operations",
        "service_requests",
        "statistics",
        "workflow",
    },
}


MERGE_SEEDS = [
    ("estatistica", "statistics"),
    ("identity", "identidade_civil"),
    ("identity", "registo_civil"),
    ("identidade_civil", "registo_civil"),
    ("financas", "financas_publicas"),
    ("financas", "financas_impostos"),
    ("financas_publicas", "financas_impostos"),
    ("financas_impostos", "taxpayer"),
    ("saude", "saude_primaria"),
    ("transportes_logistica", "portos_logistica"),
]


@dataclass
class ModuleScan:
    name: str
    path: Path
    name_tokens: set[str] = field(default_factory=set)
    concept_tokens: Counter[str] = field(default_factory=Counter)
    entity_names: set[str] = field(default_factory=set)
    repository_names: set[str] = field(default_factory=set)
    imports_out: Counter[str] = field(default_factory=Counter)
    import_evidence: defaultdict[str, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )
    files_scanned: int = 0


def normalize_token(token: str) -> str:
    key = token.lower()
    return SYNONYM_MAP.get(key, key)


def tokenize_module_name(name: str) -> set[str]:
    raw = [p for p in name.split("_") if p]
    return {normalize_token(part) for part in raw}


def tokenize_identifier(identifier: str) -> list[str]:
    raw_parts = CAMEL_RE.findall(identifier)
    tokens = []
    for part in raw_parts:
        if not part:
            continue
        for nested in TOKEN_RE.findall(part):
            if nested:
                tokens.append(normalize_token(nested))
    return tokens


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    inter = left & right
    union = left | right
    return len(inter) / len(union)


def extract_imported_module(import_path: str) -> str | None:
    match = MODULE_IMPORT_RE.match(import_path)
    if not match:
        return None
    return match.group(1)


def is_entity_path(path: Path) -> bool:
    text = path.as_posix()
    return "/domain/entities/" in text or "/domain/models/" in text


def is_repository_path(path: Path) -> bool:
    return "/repositories/" in path.as_posix()


def read_text_file(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def scan_module(module_dir: Path) -> ModuleScan:
    scan = ModuleScan(name=module_dir.name, path=module_dir)
    scan.name_tokens = tokenize_module_name(module_dir.name)
    scan.concept_tokens.update(scan.name_tokens)

    for py_file in module_dir.rglob("*.py"):
        rel_path = py_file.relative_to(module_dir)
        if "__pycache__" in rel_path.parts or "tests" in rel_path.parts:
            continue

        source = read_text_file(py_file)
        if source is None:
            continue

        scan.files_scanned += 1
        entity_path = is_entity_path(rel_path)
        repo_path = is_repository_path(rel_path)

        for lineno, line in enumerate(source.splitlines(), start=1):
            class_match = CLASS_LINE_RE.match(line)
            if class_match:
                class_name = class_match.group(1)
                tokens = tokenize_identifier(class_name)
                scan.concept_tokens.update(tokens)

                if entity_path:
                    scan.entity_names.add(class_name)

                if repo_path or class_name.endswith("Repository"):
                    scan.repository_names.add(class_name)

            import_target = None
            if line.lstrip().startswith("from "):
                from_match = IMPORT_FROM_LINE_RE.match(line)
                if from_match:
                    import_target = from_match.group(1)
            elif line.lstrip().startswith("import "):
                import_match = IMPORT_LINE_RE.match(line)
                if import_match:
                    import_target = import_match.group(1)

            if import_target and import_target != scan.name:
                scan.imports_out[import_target] += 1
                if len(scan.import_evidence[import_target]) < 5:
                    scan.import_evidence[import_target].append(
                        f"{rel_path}:{lineno} {line.strip()}"
                    )

    return scan


def pairwise_overlap(scans: dict[str, ModuleScan]) -> list[dict]:
    pairs: list[dict] = []
    names = sorted(scans.keys())

    for left_name, right_name in itertools.combinations(names, 2):
        left = scans[left_name]
        right = scans[right_name]

        shared_entities = sorted(left.entity_names & right.entity_names)
        shared_repos = sorted(left.repository_names & right.repository_names)
        direct_imports = left.imports_out[right_name] + right.imports_out[left_name]
        name_overlap = jaccard(left.name_tokens, right.name_tokens)

        left_top = {k for k, _ in left.concept_tokens.most_common(30)}
        right_top = {k for k, _ in right.concept_tokens.most_common(30)}
        concept_overlap = jaccard(left_top, right_top)

        score = (
            (name_overlap * 3.0)
            + (concept_overlap * 2.0)
            + (len(shared_entities) * 1.2)
            + (len(shared_repos) * 1.5)
            + (1.0 if direct_imports > 0 else 0.0)
        )

        seed_bonus = any(
            (left_name == a and right_name == b) or (left_name == b and right_name == a)
            for a, b in MERGE_SEEDS
        )
        if seed_bonus:
            score += 2.5

        if score < 2.3:
            continue

        pairs.append(
            {
                "left": left_name,
                "right": right_name,
                "score": round(score, 2),
                "name_overlap": round(name_overlap, 2),
                "concept_overlap": round(concept_overlap, 2),
                "direct_imports": direct_imports,
                "shared_entities": shared_entities,
                "shared_repos": shared_repos,
            }
        )

    pairs.sort(key=lambda item: item["score"], reverse=True)
    return pairs


def build_group_map(modules: set[str]) -> tuple[dict[str, list[str]], list[str]]:
    assigned: dict[str, list[str]] = {group: [] for group in DOMAIN_GROUPS}
    unknown: list[str] = []
    used: set[str] = set()

    for group, members in DOMAIN_GROUPS.items():
        for member in sorted(members):
            if member in modules:
                assigned[group].append(member)
                used.add(member)

    for module in sorted(modules - used):
        unknown.append(module)

    return assigned, unknown


def infer_conflicts(scans: dict[str, ModuleScan]) -> dict[str, list]:
    outbound_hotspots: list[dict] = []
    inbound_counter: Counter[str] = Counter()
    bidirectional: list[dict] = []

    for module, scan in scans.items():
        for target, count in scan.imports_out.items():
            inbound_counter[target] += count

        outbound_total = sum(scan.imports_out.values())
        if outbound_total >= 10 or len(scan.imports_out) >= 5:
            outbound_hotspots.append(
                {
                    "module": module,
                    "total_imports": outbound_total,
                    "distinct_targets": len(scan.imports_out),
                    "top_targets": scan.imports_out.most_common(5),
                }
            )

    seen_pairs: set[tuple[str, str]] = set()
    for module, scan in scans.items():
        for target, count in scan.imports_out.items():
            reverse = scans[target].imports_out[module] if target in scans else 0
            if reverse <= 0:
                continue
            pair = tuple(sorted((module, target)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            bidirectional.append(
                {"left": pair[0], "right": pair[1], "left_to_right": count, "right_to_left": reverse}
            )

    outbound_hotspots.sort(key=lambda item: item["total_imports"], reverse=True)
    inbound_hotspots = inbound_counter.most_common(20)
    bidirectional.sort(
        key=lambda item: item["left_to_right"] + item["right_to_left"], reverse=True
    )

    return {
        "outbound_hotspots": outbound_hotspots[:20],
        "inbound_hotspots": inbound_hotspots,
        "bidirectional": bidirectional[:20],
    }


def build_report(
    scans: dict[str, ModuleScan],
    overlap_pairs: list[dict],
    shared_entities: list[tuple[str, list[str]]],
    shared_repositories: list[tuple[str, list[str]]],
    conflicts: dict[str, list],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    modules = sorted(scans.keys())
    groups, unknown_modules = build_group_map(set(modules))

    total_files = sum(scan.files_scanned for scan in scans.values())
    total_cross_edges = sum(sum(scan.imports_out.values()) for scan in scans.values())
    total_distinct_edges = sum(len(scan.imports_out) for scan in scans.values())

    lines: list[str] = []
    lines.append("# Domain Overlap Report")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append("- Scope: `apps/backend/app/modules`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules scanned: **{len(modules)}**")
    lines.append(f"- Python files parsed: **{total_files}**")
    lines.append(f"- Cross-import edges (total): **{total_cross_edges}**")
    lines.append(f"- Cross-import edges (distinct): **{total_distinct_edges}**")
    lines.append(f"- Shared entity names detected: **{len(shared_entities)}**")
    lines.append(f"- Shared repository names detected: **{len(shared_repositories)}**")
    lines.append(f"- Candidate overlap pairs: **{len(overlap_pairs)}**")
    lines.append("")
    lines.append("## Candidate Module Merges")
    lines.append("")
    if overlap_pairs:
        lines.append("| Pair | Score | Name overlap | Concept overlap | Direct cross-imports | Shared entities | Shared repositories |")
        lines.append("| --- | ---: | ---: | ---: | ---: | --- | --- |")
        for pair in overlap_pairs[:25]:
            shared_entities_preview = ", ".join(pair["shared_entities"][:3]) or "-"
            shared_repos_preview = ", ".join(pair["shared_repos"][:3]) or "-"
            lines.append(
                f"| `{pair['left']}` + `{pair['right']}` | {pair['score']} | "
                f"{pair['name_overlap']} | {pair['concept_overlap']} | {pair['direct_imports']} | "
                f"{shared_entities_preview} | {shared_repos_preview} |"
            )
    else:
        lines.append("- No high-confidence merge candidates detected with current heuristics.")
    lines.append("")
    lines.append("## Conflicting Domain Boundaries")
    lines.append("")
    lines.append("### Cross-import hotspots (outbound)")
    lines.append("")
    if conflicts["outbound_hotspots"]:
        lines.append("| Module | Total cross-imports | Distinct targets | Top targets |")
        lines.append("| --- | ---: | ---: | --- |")
        for item in conflicts["outbound_hotspots"]:
            top_targets = ", ".join([f"`{name}` ({count})" for name, count in item["top_targets"]])
            lines.append(
                f"| `{item['module']}` | {item['total_imports']} | {item['distinct_targets']} | {top_targets} |"
            )
    else:
        lines.append("- No outbound hotspots above threshold.")
    lines.append("")
    lines.append("### Bidirectional dependencies")
    lines.append("")
    if conflicts["bidirectional"]:
        lines.append("| Module A | Module B | A -> B | B -> A |")
        lines.append("| --- | --- | ---: | ---: |")
        for item in conflicts["bidirectional"]:
            lines.append(
                f"| `{item['left']}` | `{item['right']}` | {item['left_to_right']} | {item['right_to_left']} |"
            )
    else:
        lines.append("- No bidirectional module dependencies detected.")
    lines.append("")
    lines.append("## Modules Sharing Entities")
    lines.append("")
    if shared_entities:
        lines.append("| Entity/Class | Modules |")
        lines.append("| --- | --- |")
        for entity_name, modules_with_entity in shared_entities[:80]:
            lines.append(f"| `{entity_name}` | {', '.join(f'`{mod}`' for mod in modules_with_entity)} |")
    else:
        lines.append("- No shared entity class names detected.")
    lines.append("")
    lines.append("## Modules Sharing Repositories")
    lines.append("")
    if shared_repositories:
        lines.append("| Repository/Class | Modules |")
        lines.append("| --- | --- |")
        for repo_name, modules_with_repo in shared_repositories[:80]:
            lines.append(f"| `{repo_name}` | {', '.join(f'`{mod}`' for mod in modules_with_repo)} |")
    else:
        lines.append("- No shared repository class names detected.")
    lines.append("")
    lines.append("## Recommended Domain Groups")
    lines.append("")
    for group in ("governance", "economy", "social", "infrastructure", "environment", "security", "platform"):
        members = groups[group]
        lines.append(f"### {group}")
        lines.append("")
        if members:
            lines.append(", ".join(f"`{name}`" for name in members))
        else:
            lines.append("- No modules currently mapped.")
        lines.append("")

    if unknown_modules:
        lines.append("### Unclassified")
        lines.append("")
        lines.append(", ".join(f"`{name}`" for name in unknown_modules))
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- This report is static analysis only (naming, imports, class signatures).")
    lines.append("- Merge recommendations should be validated with business ownership and API contracts.")
    lines.append("- Suggested next step: create a staged migration map (`domains/<group>/modules/<module>`).")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan module overlap and generate domain overlap report."
    )
    parser.add_argument(
        "--modules-root",
        default="apps/backend/app/modules",
        help="Path to modules root.",
    )
    parser.add_argument(
        "--output",
        default="reports/domain_overlap_report.md",
        help="Output Markdown report path.",
    )
    args = parser.parse_args()

    modules_root = Path(args.modules_root).resolve()
    output = Path(args.output).resolve()

    if not modules_root.exists():
        raise SystemExit(f"Modules root not found: {modules_root}")

    module_dirs = sorted(
        [d for d in modules_root.iterdir() if d.is_dir() and not d.name.startswith("__")]
    )
    scans: dict[str, ModuleScan] = {module_dir.name: scan_module(module_dir) for module_dir in module_dirs}

    entity_index: defaultdict[str, set[str]] = defaultdict(set)
    repo_index: defaultdict[str, set[str]] = defaultdict(set)
    for module_name, scan in scans.items():
        for entity in scan.entity_names:
            entity_index[entity].add(module_name)
        for repo in scan.repository_names:
            repo_index[repo].add(module_name)

    shared_entities = sorted(
        (
            (name, sorted(modules))
            for name, modules in entity_index.items()
            if len(modules) > 1
        ),
        key=lambda item: (len(item[1]), item[0]),
        reverse=True,
    )
    shared_repositories = sorted(
        (
            (name, sorted(modules))
            for name, modules in repo_index.items()
            if len(modules) > 1
        ),
        key=lambda item: (len(item[1]), item[0]),
        reverse=True,
    )

    overlap_pairs = pairwise_overlap(scans)
    conflicts = infer_conflicts(scans)
    report = build_report(
        scans=scans,
        overlap_pairs=overlap_pairs,
        shared_entities=shared_entities,
        shared_repositories=shared_repositories,
        conflicts=conflicts,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
