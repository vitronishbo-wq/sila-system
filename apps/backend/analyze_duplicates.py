#!/usr/bin/env python3
"""Análise De Duplicidade De Diretórios - SILA Backend"""

import os
import subprocess
from pathlib import Path

BACKEND_PATH = Path("/home/dev12cls/sila-system/apps/backend")


def get_dir_size(path):
    """Calcula tamanho de um diretório"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir() and not entry.name.startswith("."):
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total


def count_files(path, pattern="*.py"):
    """Conta arquivos Python"""
    result = subprocess.run(
        f"find {path} -name '{pattern}' -type f 2>/dev/null | wc -l",
        shell=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def find_imports(directory, import_pattern):
    """Encontra imports em um diretório"""
    result = subprocess.run(
        f"grep -r '{import_pattern}' {directory} --include='*.py' 2>/dev/null || true",
        shell=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.split("\n") if line.strip()]


def analyze_duplicates():
    """Análise completa de duplicidades"""

    duplicates = {
        "app/infra": {
            "path": BACKEND_PATH / "app" / "infra",
            "import_patterns": ["from apps.backend.app.infra"],
            "status": "🔴 MORTO",
        },
        "app/infrastructure": {
            "path": BACKEND_PATH / "app" / "infrastructure",
            "import_patterns": ["from apps.backend.app.infrastructure"],
            "status": "🟢 ATIVO",
        },
        "application (root)": {
            "path": BACKEND_PATH / "application",
            "import_patterns": ["from application"],
            "status": "🔴 ÓRFÃO",
        },
        "app/application": {
            "path": BACKEND_PATH / "app" / "application",
            "import_patterns": ["from apps.backend.app.application"],
            "status": "🟢 PRINCIPAL",
        },
        "seeds (root)": {
            "path": BACKEND_PATH / "seeds",
            "import_patterns": ["from seeds"],
            "status": "🟡 REVISAR",
        },
        "app/seeds": {
            "path": BACKEND_PATH / "app" / "seeds",
            "import_patterns": ["from apps.backend.app.seeds"],
            "status": "🟡 DUPLICADO",
        },
        "apps/backend (nested)": {
            "path": BACKEND_PATH / "apps" / "backend",
            "import_patterns": [],
            "status": "🔴 REDUNDANTE",
        },
    }

    print("\n" + "=" * 80)
    print("🔍 ANÁLISE DE DUPLICIDADE - SILA BACKEND")
    print("=" * 80)

    for name, info in duplicates.items():
        path = info["path"]
        if path.exists():
            size = get_dir_size(path)
            py_files = count_files(path, "*.py")
            imports = []
            for pattern in info["import_patterns"]:
                imports.extend(find_imports(BACKEND_PATH, pattern))

            print(f"\n📁 {name}")
            print(f"   Path: {path.relative_to(BACKEND_PATH.parent)}")
            print(f"   Tamanho: {size:,} bytes ({size / 1024:.1f} KB)")
            print(f"   Arquivos Python: {py_files}")
            print(f"   Status: {info['status']}")
            print(f"   Importações encontradas: {len(imports)}")
            if imports:
                for imp in imports[:3]:
                    short = imp.replace(str(BACKEND_PATH), "...").split(":")
                    print(f"      - {short[0]}")
                if len(imports) > 3:
                    print(f"      ... e mais {len(imports) - 3}")
        else:
            print(f"\n📁 {name}")
            print("   ❌ Não encontrado")

    print("\n" + "=" * 80)
    print("🎯 RESUMO DE AÇÕES")
    print("=" * 80)
    print("""
P0 - ELIMINAR IMEDIATAMENTE (↓ 100+ KB):
   1. rm -rf app/infra/              [20 KB]  - Apenas audit_logger orfão
   2. rm -rf apps/backend/           [?? KB]  - Nested redundância
   3. rm -rf application/            [156 KB] - Legacy services orfãs

P1 - CONSOLIDAR (próximas 48h):
   1. Mover application/services/* → app/application/
   2. Atualizar todos os imports
   3. Mover seeds/core → app/seeds/core (ou reorg estrutura)

P2 - INVESTIGAR:
   1. infrastructure/ (raiz) - se tem código, consolidar com app/infrastructure/
    """)


if __name__ == "__main__":
    analyze_duplicates()
