#!/usr/bin/env python3
"""
Script para validar arquivos de requirements
Verifica sintaxe, duplicações e conflitos potenciais
"""

import re
import sys
from pathlib import Path
from collections import defaultdict


def parse_requirement(line):
    """Parse uma linha de requirement"""
    line = line.strip()

    # Ignorar comentários e linhas vazias
    if not line or line.startswith("#"):
        return None

    # Ignorar includes
    if line.startswith("-r "):
        return None

    # Parse package==version ou package>=version
    match = re.match(r"^([a-zA-Z0-9_\-\[\]]+)(==|>=|<=|>|<|~=)(.+)$", line)
    if match:
        return {
            "package": match.group(1),
            "operator": match.group(2),
            "version": match.group(3),
            "line": line,
        }

    # Package sem versão especificada
    match = re.match(r"^([a-zA-Z0-9_\-\[\]]+)$", line)
    if match:
        return {
            "package": match.group(1),
            "operator": None,
            "version": None,
            "line": line,
        }

    return {"line": line, "error": "Formato inválido"}


def validate_file(file_path):
    """Valida um arquivo de requirements"""
    errors = []
    warnings = []
    packages = defaultdict(list)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Erro ao ler arquivo: {e}"], []

    for i, line in enumerate(lines, 1):
        req = parse_requirement(line)
        if req is None:
            continue

        if "error" in req:
            errors.append(f"Linha {i}: {req['error']} - {req['line']}")
            continue

        package = req["package"].lower()
        packages[package].append((i, req))

        # Verificar versão não especificada (warning)
        if req["operator"] is None:
            warnings.append(f"Linha {i}: Versão não especificada para {req['package']}")

    # Verificar duplicações
    for package, occurrences in packages.items():
        if len(occurrences) > 1:
            lines_str = ", ".join(str(line) for line, _ in occurrences)
            errors.append(f"Pacote duplicado '{package}' nas linhas: {lines_str}")

    return errors, warnings


def main():
    project_root = Path(__file__).parent.parent

    files_to_check = [
        project_root / "requirements.txt",
        project_root / "requirements-dev.txt",
        project_root / "requirements-test.txt",
    ]

    print("🔍 Validando arquivos de requirements...\n")

    total_errors = 0
    total_warnings = 0

    for file_path in files_to_check:
        if not file_path.exists():
            print(f"⚠️  Arquivo não encontrado: {file_path}")
            continue

        print(f"📄 Validando: {file_path.name}")
        errors, warnings = validate_file(file_path)

        if errors:
            print(f"  ❌ {len(errors)} erro(s) encontrado(s):")
            for error in errors:
                print(f"     • {error}")
            total_errors += len(errors)

        if warnings:
            print(f"  ⚠️  {len(warnings)} aviso(s):")
            for warning in warnings:
                print(f"     • {warning}")
            total_warnings += len(warnings)

        if not errors and not warnings:
            print(f"  ✅ OK")

        print()

    print("=" * 60)
    if total_errors == 0:
        print(f"✅ Validação concluída: {total_warnings} avisos, 0 erros")
        return 0
    else:
        print(f"❌ Validação falhou: {total_warnings} avisos, {total_errors} erros")
        return 1


if __name__ == "__main__":
    sys.exit(main())
