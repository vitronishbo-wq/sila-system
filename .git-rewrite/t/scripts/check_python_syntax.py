#!/usr/bin/env python3
"""
Script para verificar e corrigir sintaxe Python de todos os arquivos .py
"""

import ast
import sys
import re
from pathlib import Path


def auto_fix_common_syntax_errors(source, file_path):
    """Corrige erros comuns de sintaxe Python automaticamente"""
    original_source = source
    fixed = False

    # 1. Corrigir f-strings quebrados: f"{var".2f"} -> f"{var:.2f}"
    fstring_pattern = r'f"([^"]*)\{([^}]+)\}"\.(\w+)f"'
    if re.search(fstring_pattern, source):
        source = re.sub(fstring_pattern, r'f"\1{\2:.\3f}"', source)
        fixed = True
        print(f"   🔧 Corrigido f-string quebrado")

    # 2. Corrigir colchetes não fechados: ]]] -> ]
    unmatched_brackets = r"\]\s*\]\s*\]"
    if re.search(unmatched_brackets, source):
        source = re.sub(unmatched_brackets, "]", source)
        fixed = True
        print(f"   🔧 Corrigido colchetes em excesso")

    # 3. Corrigir definições de função sem dois-pontos: def main() -> def main():
    func_no_colon = r"def\s+(\w+)\s*\([^)]*\)\s*$"
    if re.search(func_no_colon, source, re.MULTILINE):
        source = re.sub(func_no_colon, r"def \1():", source, flags=re.MULTILINE)
        fixed = True
        print(f"   🔧 Adicionado dois-pontos em definição de função")

    # 4. Corrigir vírgulas ausentes em listas/tuplas
    missing_comma = r"(\w+)\s+(\w+\s*=)"
    if re.search(missing_comma, source):
        source = re.sub(missing_comma, r"\1, \2", source)
        fixed = True
        print(f"   🔧 Adicionada vírgula ausente")

    return source, fixed


def check_python_syntax(file_path, auto_fix=False):
    """Verifica e opcionalmente corrige sintaxe de um arquivo Python"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        # Primeiro, tenta compilar como está
        try:
            ast.parse(source, filename=str(file_path))
            print(f"✅ {file_path.relative_to(Path.cwd())} - Sintaxe válida")
            return True
        except SyntaxError as e:
            if auto_fix:
                print(
                    f"🔧 {file_path.relative_to(Path.cwd())} - Tentando correção automática..."
                )
                fixed_source, was_fixed = auto_fix_common_syntax_errors(
                    source, file_path
                )

                if was_fixed:
                    # Testa se a correção funcionou
                    try:
                        ast.parse(fixed_source, filename=str(file_path))
                        # Salva o arquivo corrigido
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(fixed_source)
                        print(
                            f"✅ {file_path.relative_to(Path.cwd())} - Corrigido automaticamente!"
                        )
                        return True
                    except SyntaxError:
                        print(
                            f"❌ {file_path.relative_to(Path.cwd())} - Correção automática falhou"
                        )

            # Se não foi corrigido ou correção falhou, mostra o erro
            print(f"❌ {file_path.relative_to(Path.cwd())} - Erro de sintaxe:")
            print(f"   Linha {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
            print(f"   {' ' * (e.offset - 1 if e.offset else 0)}^ {e.msg}")
            return False

    except Exception as e:
        print(f"⚠️ {file_path.relative_to(Path.cwd())} - Erro ao ler: {e}")
        return False


def main():
    """Verifica sintaxe de todos os arquivos Python"""
    import argparse

    parser = argparse.ArgumentParser(description="Verificar e corrigir sintaxe Python")
    parser.add_argument(
        "--fix", action="store_true", help="Corrigir automaticamente erros comuns"
    )
    args = parser.parse_args()

    root = Path.cwd()

    # Diretórios a ignorar
    ignore_dirs = {
        "venv",
        ".venv",
        "env",
        ".env",
        "node_modules",
        "__pycache__",
        ".git",
        ".pytest_cache",
        "build",
        "dist",
        ".backups",
        "backup_onboarding",
    }

    python_files = []
    for py_file in root.rglob("*.py"):
        # Verifica se o arquivo está em um diretório ignorado
        if any(part in ignore_dirs for part in py_file.parts):
            continue
        python_files.append(py_file)

    if not python_files:
        print("⚠️ Nenhum arquivo Python encontrado")
        return 0

    action = "Corrigindo" if args.fix else "Verificando"
    print(f"🔍 {action} sintaxe de {len(python_files)} arquivos Python...")
    print()

    errors = 0
    fixed = 0
    for py_file in sorted(python_files):
        result = check_python_syntax(py_file, auto_fix=args.fix)
        if not result:
            errors += 1
        elif args.fix and result:
            # Se estava com erro e foi corrigido, conta como fixed
            fixed += 1

    print()
    if args.fix:
        print(f"🔧 {fixed} arquivo(s) corrigido(s) automaticamente")

    if errors == 0:
        print("🎉 Todos os arquivos Python têm sintaxe válida!")
        return 0
    else:
        print(f"💥 {errors} arquivo(s) ainda com problemas de sintaxe Python")
        if not args.fix:
            print("💡 Use --fix para tentar correção automática")
        return 1


if __name__ == "__main__":
    sys.exit(main())
