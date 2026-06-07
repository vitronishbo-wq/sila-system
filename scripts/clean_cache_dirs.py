#!/usr/bin/env python3
"""
Script para limpar diretórios de cache que podem causar problemas de permissão
"""

import shutil
from pathlib import Path


def clean_cache_directories():
    """Remove diretórios de cache problemáticos"""
    root = Path(__file__).parent.parent

    cache_dirs = [
        "node_modules/.vite",
        "apps/frontend/node_modules/.vite",
        "apps/frontend/apps/web/node_modules/.vite",
        ".vite",
        ".cache",
        "__pycache__",
        ".pytest_cache",
        "apps/backend/.pytest_cache",
        "apps/backend/__pycache__",
        "venv/__pycache__",
        "build",
        "dist",
    ]

    cleaned = 0
    errors = 0

    print("🧹 Limpando diretórios de cache...")

    for cache_dir in cache_dirs:
        cache_path = root / cache_dir
        if cache_path.exists():
            try:
                if cache_path.is_dir():
                    shutil.rmtree(cache_path)
                    print(f"✅ Removido: {cache_dir}")
                    cleaned += 1
                else:
                    cache_path.unlink()
                    print(f"✅ Removido arquivo: {cache_dir}")
                    cleaned += 1
            except PermissionError:
                print(f"⚠️ Sem permissão para remover: {cache_dir}")
                errors += 1
            except Exception as e:
                print(f"❌ Erro ao remover {cache_dir}: {e}")
                errors += 1

    print(f"\n📊 Resumo: {cleaned} removidos, {errors} erros")

    if errors > 0:
        print("\n💡 Dica: Execute como administrador se necessário")
        return 1

    return 0


if __name__ == "__main__":
    exit(clean_cache_directories())
