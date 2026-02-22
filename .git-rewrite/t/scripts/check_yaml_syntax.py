#!/usr/bin/env python3
"""
Script para verificar sintaxe YAML dos arquivos principais
"""

import yaml
import sys
from pathlib import Path


def check_yaml_file(file_path):
    """Verifica sintaxe de um arquivo YAML"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        print(f"✅ {file_path} - YAML válido")
        return True
    except yaml.YAMLError as e:
        print(f"❌ {file_path} - Erro YAML: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {file_path} - Erro ao ler arquivo: {e}")
        return False


def main():
    """Verifica arquivos YAML principais"""
    root = Path(__file__).parent.parent

    yaml_files = [
        ".pre-commit-config.yaml",
        ".gitlab-ci.yml",
        ".github/workflows/ci-cd.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/sila-ci.yml",
        "DOCKER_COMPOSE_NGINX.yml",
        "True/config.yml",
        "scripts/config.yml",
    ]

    errors = 0

    print("🔍 Verificando sintaxe YAML...")
    print()

    for yaml_file in yaml_files:
        file_path = root / yaml_file
        if file_path.exists():
            if not check_yaml_file(file_path):
                errors += 1
        else:
            print(f"⏭️ {yaml_file} - Arquivo não encontrado")

    print()
    if errors == 0:
        print("🎉 Todos os arquivos YAML estão válidos!")
        return 0
    else:
        print(f"💥 {errors} arquivo(s) com problemas de sintaxe YAML")
        return 1


if __name__ == "__main__":
    sys.exit(main())
