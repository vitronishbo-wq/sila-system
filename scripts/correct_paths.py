#!/usr/bin/env python3
"""
SILA System - Path Correction Utility
Corrige paths relativos e absolutos em scripts Python e Shell
"""

import re
from pathlib import Path

# Padrões de paths problemáticos
PATH_PATTERNS = {
    # Imports incorretos do backend
    "backend_parent_parent": (
        r"backend_dir\s*=\s*Path\(__file__\)\.parent\.parent\s*\n\s*sys\.path\.insert\(0,\s*str\(backend_dir\)\)",
        "get_correct_backend_path",
    ),
    # Paths relativos hardcoded
    "relative_backend": (
        r'sys\.path\.(?:insert|append)\([01],\s*["\']\.\.\/backend["\']',
        "fix_relative_backend",
    ),
    # Paths relativos genéricos com ../
    "relative_dots": (r'["\'](\.\./)+([^"\']+)["\']', "fix_relative_dots"),
}

# Estrutura de diretórios do projeto
PROJECT_STRUCTURE = {
    "root": Path(__file__).resolve().parents[1],
    "apps": ["backend", "frontend", "worker", "api_gateway"],
    "scripts_dirs": ["scripts", "automation", "tools"],
}


def get_project_root() -> Path:
    """Retorna a raiz do projeto"""
    return Path(__file__).resolve().parents[1]


def get_relative_path(file_path: Path, target_path: Path) -> Path:
    """Calcula path relativo entre dois caminhos"""
    try:
        return file_path.parent.relative_to(target_path)
    except ValueError:
        return None


def get_parent_level(script_path: Path, target: str) -> int:
    """
    Calcula quantos níveis de .parent são necessários para chegar ao alvo

    Exemplo:
        script em: automation/deployment/sila_cli.py
        alvo: apps/backend
        resultado: 2 (para chegar à raiz) + path para backend
    """
    project_root = get_project_root()
    script_rel = script_path.relative_to(project_root)
    depth = len(script_rel.parents) - 1
    return depth


def get_correct_backend_path(match, script_path: Path) -> str:
    """Gera o caminho correto para o backend a partir de qualquer script"""
    get_project_root()
    parent_levels = get_parent_level(script_path, "apps/backend")

    return f"""# Adicionar backend ao Python path
PROJECT_ROOT = Path(__file__).resolve().parents[{parent_levels}]
sys.path.insert(0, str(PROJECT_ROOT / "apps" / "backend"))"""


def fix_relative_backend(match, script_path: Path) -> str:
    """Corrige sys.path com paths relativos ao backend"""
    parent_levels = get_parent_level(script_path, "apps/backend")
    return f'sys.path.insert(0, str(Path(__file__).resolve().parents[{parent_levels}] / "apps/backend"))'


def fix_relative_dots(match, script_path: Path) -> str:
    """Corrige paths relativos genéricos"""
    target_path = match.group(2)  # Captura o caminho sem ../
    parent_levels = match.group(1).count("../")
    return f'str(Path(__file__).resolve().parents[{parent_levels}] / "{target_path}")'


def scan_python_file(file_path: Path) -> list[dict]:
    """Escaneia um arquivo Python procurando problemas de path"""
    issues = []

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Verificar cada padrão
        for issue_type, (pattern, _) in PATH_PATTERNS.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                issues.append(
                    {
                        "type": issue_type,
                        "file": str(file_path),
                        "line": content[: match.start()].count("\n") + 1,
                        "match": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

    except Exception as e:
        print(f"❌ Erro ao ler {file_path}: {e}")

    return issues


def fix_python_file(file_path: Path, dry_run: bool = True) -> bool:
    """Corrige paths em um arquivo Python"""
    try:
        with open(file_path, encoding="utf-8") as f:
            original_content = f.read()

        modified_content = original_content
        changes_made = []

        # Aplicar correções
        for issue_type, (pattern, fix_func_name) in PATH_PATTERNS.items():
            # Obter a função de correção pelo nome
            fix_func = globals()[fix_func_name]

            def replacer(match):
                replacement = fix_func(match, file_path)
                changes_made.append(
                    f"  - {issue_type}: {match.group(0)[:50]}... → {replacement[:50]}..."
                )
                return replacement

            modified_content = re.sub(pattern, replacer, modified_content)

        if modified_content != original_content:
            if not dry_run:
                # Fazer backup
                backup_path = file_path.with_suffix(file_path.suffix + ".backup")
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(original_content)

                # Escrever arquivo corrigido
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

                print(f"✅ Corrigido: {file_path.relative_to(get_project_root())}")
            else:
                print(f"🔍 Mudanças necessárias em: {file_path.relative_to(get_project_root())}")

            for change in changes_made:
                print(change)

            return True

        return False

    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False


def scan_directory(directory: Path, extensions: list[str] = None) -> list[Path]:
    """Escaneia diretório recursivamente procurando arquivos"""
    if extensions is None:
        extensions = [".py"]
    files = []

    for ext in extensions:
        files.extend(directory.rglob(f"*{ext}"))

    return files


def generate_report(all_issues: list[dict]) -> str:
    """Gera relatório de problemas encontrados"""
    if not all_issues:
        return "✅ Nenhum problema de path encontrado!"

    report = [
        "=" * 80,
        "RELATÓRIO DE PROBLEMAS DE PATHS",
        "=" * 80,
        f"\nTotal de problemas encontrados: {len(all_issues)}\n",
    ]

    # Agrupar por tipo
    by_type = {}
    for issue in all_issues:
        issue_type = issue["type"]
        if issue_type not in by_type:
            by_type[issue_type] = []
        by_type[issue_type].append(issue)

    for issue_type, issues in by_type.items():
        report.append(f"\n## {issue_type.upper()} ({len(issues)} ocorrências)")
        report.append("-" * 80)

        for issue in issues:
            report.append(f"\n📁 Arquivo: {issue['file']}")
            report.append(f"📍 Linha: {issue['line']}")
            report.append(f"🔍 Código: {issue['match'][:100]}")

    report.append("\n" + "=" * 80)
    return "\n".join(report)


def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Corrige paths em scripts do SILA System")
    parser.add_argument(
        "--scan-only", action="store_true", help="Apenas escanear, não fazer correções"
    )
    parser.add_argument("--fix", action="store_true", help="Aplicar correções (cria backups)")
    parser.add_argument(
        "--directories",
        nargs="+",
        default=["scripts", "automation", "tools"],
        help="Diretórios para processar",
    )
    parser.add_argument("--report", type=str, help="Salvar relatório em arquivo")

    args = parser.parse_args()

    project_root = get_project_root()
    print(f"🏠 Raiz do projeto: {project_root}\n")

    all_issues = []
    files_to_fix = []

    # Escanear diretórios
    for directory_name in args.directories:
        directory = project_root / directory_name

        if not directory.exists():
            print(f"⚠️  Diretório não encontrado: {directory}")
            continue

        print(f"📂 Escaneando: {directory_name}/")

        python_files = scan_directory(directory, [".py"])
        print(f"   Encontrados {len(python_files)} arquivos Python")

        for file_path in python_files:
            issues = scan_python_file(file_path)
            if issues:
                all_issues.extend(issues)
                files_to_fix.append(file_path)

        print()

    # Gerar relatório
    report = generate_report(all_issues)
    print(report)

    if args.report:
        report_path = project_root / args.report
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 Relatório salvo em: {report_path}")

    # Aplicar correções se solicitado
    if args.fix and files_to_fix:
        print("\n" + "=" * 80)
        print("APLICANDO CORREÇÕES")
        print("=" * 80 + "\n")

        fixed_count = 0
        for file_path in files_to_fix:
            if fix_python_file(file_path, dry_run=False):
                fixed_count += 1

        print(f"\n✅ Total de arquivos corrigidos: {fixed_count}")
        print("💾 Backups criados com extensão .backup")

    elif not args.fix and files_to_fix:
        print("\n💡 Use --fix para aplicar as correções automaticamente")
        print("   Exemplo: python scripts/correct_paths.py --fix")


if __name__ == "__main__":
    main()
