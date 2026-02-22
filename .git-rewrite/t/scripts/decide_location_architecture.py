#!/usr/bin/env python3
"""
Script para decidir qual arquitetura manter: Opção A ou B

Opção A: Manter models.py (RECOMENDADA)
- Deletar diretório models/
- Simplifica estrutura
- Remove conflito de importação
- 1-2 horas de trabalho

Opção B: Manter models/
- Deletar models.py
- Oferece ambas arquiteturas
- Padrão moderno
- 4-6 horas de trabalho
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def search_for_usage(pattern, directory):
    """Search for usage of models in codebase."""
    matches = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git", ".venv", "venv"]]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_no, line in enumerate(f, 1):
                            if re.search(pattern, line, re.IGNORECASE):
                                matches[filepath].append((line_no, line.strip()))
                except Exception:
                    pass

    return matches


def main():
    print(
        f"\n{BOLD}{CYAN}═══════════════════════════════════════════════════════════════════{RESET}"
    )
    print(f"{BOLD}LOCATION MODELS - DECISÃO ARQUITETURAL{RESET}")
    print(
        f"{CYAN}═══════════════════════════════════════════════════════════════════{RESET}\n"
    )

    base_path = Path.cwd()
    apps_path = base_path / "apps" / "backend"

    if not apps_path.exists():
        print(f"{RED}❌ Não foi possível encontrar apps/backend{RESET}")
        return

    print(f"{BOLD}Analisando codebase...{RESET}\n")

    # Search for usage patterns
    print(f"{YELLOW}🔍 Procurando referências de modelos...{RESET}\n")

    # Models específicas (Opção A - models.py)
    hierarchy_models = [
        ("CountryModel", "CountryModel"),
        ("ProvinceModel", "ProvinceModel"),
        ("MunicipalityModel", "MunicipalityModel"),
        ("CommuneModel", "CommuneModel"),
        ("CityModel", "CityModel"),
        ("FullAddress", "FullAddress"),
    ]

    # Modelo genérico (Opção B - models/region.py)
    generic_model = [
        ("Region", "Region"),
    ]

    hierarchy_usage = {}
    for model_name, pattern in hierarchy_models:
        matches = search_for_usage(f"\\b{pattern}\\b", apps_path)
        hierarchy_usage[model_name] = len(matches)

    generic_usage = {}
    for model_name, pattern in generic_model:
        matches = search_for_usage(f"\\b{pattern}\\b", apps_path)
        generic_usage[model_name] = len(matches)

    # Display results
    print(f"{BOLD}Uso de Modelos Hierárquicos (Country, Province, etc):{RESET}")
    hierarchy_count = 0
    for model_name, count in hierarchy_usage.items():
        status = "✅ Encontrado" if count > 0 else "⚠️  Não usado"
        hierarchy_count += count
        print(f"  {model_name}: {count} referências {status}")

    print(f"\n{BOLD}Uso de Modelo Genérico (Region):{RESET}")
    generic_count = 0
    for model_name, count in generic_usage.items():
        status = "✅ Encontrado" if count > 0 else "⚠️  Não usado"
        generic_count += count
        print(f"  {model_name}: {count} referências {status}")

    print(f"\n")
    print(
        f"{BOLD}═══════════════════════════════════════════════════════════════════{RESET}"
    )
    print(f"{BOLD}RECOMENDAÇÃO:{RESET}\n")

    if hierarchy_count > 0 and generic_count == 0:
        print(f"{GREEN}✅ OPÇÃO A (Manter models.py){RESET}")
        print(f"   Razão: Só usa modelos hierárquicos")
        print(f"   ├─ Simplicidade: ✅ Máxima")
        print(f"   ├─ Tempo: ✅ 1-2 horas")
        print(f"   ├─ Risco: ✅ Mínimo")
        print(f"   └─ Ação: Deletar models/ inteiro")
        option = "A"

    elif generic_count > 0 and hierarchy_count == 0:
        print(f"{YELLOW}⚠️  OPÇÃO B (Manter models/){RESET}")
        print(f"   Razão: Só usa modelo genérico")
        print(f"   ├─ Flexibilidade: ✅ Máxima")
        print(f"   ├─ Tempo: ❌ 4-6 horas")
        print(f"   ├─ Risco: ⚠️  Médio")
        print(f"   └─ Ação: Deletar models.py e refatorar")
        option = "B"

    elif hierarchy_count > 0 and generic_count > 0:
        print(f"{YELLOW}⚠️  OPÇÃO B (Manter models/){RESET}")
        print(f"   Razão: Usa AMBAS arquiteturas")
        print(f"   ├─ Necessário oferecer ambas")
        print(f"   ├─ Tempo: ❌ 4-6 horas")
        print(f"   ├─ Risco: ⚠️  Médio")
        print(f"   └─ Ação: Consolidar em models/ como submodelos")
        option = "B"

    else:
        print(f"{BLUE}ℹ️  NENHUM USO DETECTADO{RESET}")
        print(f"   Recomendação: OPÇÃO A (mais simples)")
        print(f"   Ação: Deletar models/ inteiro")
        option = "A"

    print(
        f"\n{BOLD}═══════════════════════════════════════════════════════════════════{RESET}\n"
    )

    # Print execution instructions
    print(f"{BOLD}Próximos Passos ({option}):{RESET}\n")

    if option == "A":
        print(f"{GREEN}OPÇÃO A - MANTER models.py{RESET}\n")
        print(f"1. Deletar diretório models/:")
        print(f"   rm -rf apps/backend/modules/location/models/\n")
        print(f"2. Verificar que não há importações do models/ package:")
        print(f"   grep -r 'from.*models import' apps/backend/\n")
        print(f"3. Executar testes:")
        print(f"   pytest tests/modules/location/ -v\n")

    else:
        print(f"{YELLOW}OPÇÃO B - MANTER models/{RESET}\n")
        print(f"1. Deletar models.py:")
        print(f"   rm apps/backend/modules/location/models.py\n")
        print(f"2. Reorganizar models/ em submodelos:")
        print(f"   models/")
        print(f"   ├─ __init__.py (limpo, sem shim)")
        print(f"   ├─ hierarchy.py (Country, Province, etc)")
        print(f"   └─ region.py (Region - já existe)\n")
        print(f"3. Atualizar models/__init__.py:")
        print(f"   from .hierarchy import CountryModel, ProvinceModel, ...")
        print(f"   from .region import Region\n")
        print(f"4. Atualizar importações em todo código\n")
        print(f"5. Executar testes:")
        print(f"   pytest tests/modules/location/ -v\n")

    print(
        f"{BOLD}═══════════════════════════════════════════════════════════════════{RESET}\n"
    )

    # Summary
    print(f"{BOLD}RESUMO:{RESET}\n")
    print(f"Modelos Hierárquicos (A):  {hierarchy_count:3d} referências")
    print(f"Modelos Genéricos (B):     {generic_count:3d} referências")
    print(f"\n{BOLD}Escolha:  OPÇÃO {option}{RESET}\n")


if __name__ == "__main__":
    main()
