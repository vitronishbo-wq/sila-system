#!/usr/bin/env python3
"""
Guardrail: Enforce macro-domain boundaries using the dependency graph and module registry.
Provides high-speed validation for the SILA System.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Configuração de Permissões: Fonte da Verdade de Dependências Cruzadas
DEFAULT_ALLOWED = {
    "intelligence": [
        "justice",
        "economy",
        "governance",
        "resources",
        "society",
        "infrastructure_sector",
    ],
    "justice": ["governance"],
    "economy": ["governance", "justice", "resources", "society", "infrastructure_sector"],
    "society": ["governance", "justice", "economy", "infrastructure_sector"],
    "infrastructure_sector": [
        "governance",
        "economy",
    ],  # Precisa de Economia para Financiamento/Obras
    "resources": ["governance", "economy", "infrastructure_sector"],
    "governance": ["justice"],
}


def get_module_to_domain() -> dict[str, str]:
    """Mapeia sub-módulos para seus respectivos macro-domínios usando o registro oficial."""
    # Adiciona o backend ao path para importar o registro oficial
    backend_path = Path("apps/backend")
    sys.path.insert(0, str(backend_path.absolute()))

    mapping = {}
    try:
        # Tenta carregar o mapeamento dinâmico do sistema
        from apps.backend.app.core.module_registry import iter_modules

        for spec in iter_modules(enabled_only=False):
            mapping[spec.name] = spec.domain
    except ImportError:
        # Fallback: Mapeamento manual via inspeção de diretório se o registry falhar
        modules_root = Path("apps/backend/app/modules")
        if modules_root.exists():
            for domain_dir in modules_root.iterdir():
                if domain_dir.is_dir() and not domain_dir.name.startswith(("_", ".")):
                    for sub_dir in domain_dir.iterdir():
                        if sub_dir.is_dir() and not sub_dir.name.startswith(("_", ".")):
                            mapping[sub_dir.name] = domain_dir.name
    return mapping


def main():
    parser = argparse.ArgumentParser(description="SILA Macro-domain Boundary Guardrail")
    parser.add_argument("--dependency-json", default="reports/module_dependency_graph.json")
    parser.add_argument("--fail-on-violation", action="store_true")
    args = parser.parse_args()

    # 1. Obter o mapeamento de domínios
    module_to_domain = get_module_to_domain()
    if not module_to_domain:
        print("⚠️  Warning: Could not determine module-to-domain mapping. Check registry.")
        return 0

    # 2. Carregar o Grafo de Dependências (gerado pelo architecture-index)
    dep_graph_path = Path(args.dependency_json)
    if not dep_graph_path.exists():
        print(f"❌ Error: Dependency graph not found at {args.dependency_json}")
        print("   Run 'make architecture-index' first.")
        return 1

    try:
        dep_graph = json.loads(dep_graph_path.read_text())
    except json.JSONDecodeError:
        print(f"❌ Error: {args.dependency_json} is not a valid JSON.")
        return 1

    # 3. Validar Arestas (Edges) do Grafo
    edges = dep_graph.get("edges", [])
    violations = []

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if not src or not tgt:
            continue

        src_dom = module_to_domain.get(src)
        tgt_dom = module_to_domain.get(tgt)

        # Ignora se os domínios forem iguais ou se forem módulos core/shared
        if not src_dom or not tgt_dom or src_dom == tgt_dom:
            continue

        # Verifica se a importação entre macro-domínios é permitida
        allowed = DEFAULT_ALLOWED.get(src_dom, [])
        if tgt_dom not in allowed:
            # Filtro para ignorar utilitários globais se não estiverem no mapping
            if tgt not in ["core", "shared", "common"]:
                violations.append(
                    {"src_mod": src, "tgt_mod": tgt, "src_dom": src_dom, "tgt_dom": tgt_dom}
                )

    # 4. Report
    print("\nAudit: Macro-domain Boundaries")
    print("=" * 60)

    if violations:
        print(f"❌ FOUND {len(violations)} ARCHITECTURAL VIOLATIONS\n")
        for v in violations:
            print(f"  [ERROR] Module '{v['src_mod']}' ({v['src_dom']})")
            print(f"          illegal import from '{v['tgt_mod']}' ({v['tgt_dom']})")
        print("-" * 60)
        return 1 if args.fail_on_violation else 0

    print("✅ Success: All cross-domain dependencies respect the architecture graph.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
