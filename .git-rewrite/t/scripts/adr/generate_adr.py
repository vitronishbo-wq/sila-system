#!/usr/bin/env python3
"""
Script para gerar novos ADRs (Architectural Decision Records)

Uso:
    python scripts/adr/generate_adr.py --title "Título da Decisão" --category "architecture"
    python scripts/adr/generate_adr.py --title "Migration to Microservices" --category "architecture" --author "João Silva"
"""

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configurações
ADR_DIR = Path("docs/adr")
TEMPLATE_FILE = ADR_DIR / "template.md"
INDEX_FILE = ADR_DIR / "index.md"

# Categorias válidas
VALID_CATEGORIES = [
    "architecture",
    "technology",
    "security",
    "data",
    "deployment",
    "quality",
]


def get_next_adr_number() -> str:
    """Obtém o próximo número sequencial de ADR"""
    if not ADR_DIR.exists():
        ADR_DIR.mkdir(parents=True, exist_ok=True)
        return "0001"

    adr_files = list(ADR_DIR.glob("*.md"))
    adr_files = [
        f for f in adr_files if f.name not in ["README.md", "template.md", "index.md"]
    ]

    if not adr_files:
        return "0001"

    # Extrair números dos arquivos existentes
    numbers = []
    for file in adr_files:
        match = re.match(r"(\d{4})", file.name)
        if match:
            numbers.append(int(match.group(1)))

    if not numbers:
        return "0001"

    next_number = max(numbers) + 1
    return f"{next_number:04d}"


def sanitize_title(title: str) -> str:
    """Sanitiza título para uso em nome de arquivo"""
    # Converter para lowercase e substituir espaços por hífens
    sanitized = title.lower()
    sanitized = re.sub(r"[^\w\s-]", "", sanitized)  # Remover caracteres especiais
    sanitized = re.sub(r"\s+", "-", sanitized)  # Substituir espaços por hífens
    sanitized = re.sub(r"-+", "-", sanitized)  # Remover hífens duplicados
    sanitized = sanitized.strip("-")  # Remover hífens do início/fim

    return sanitized


def get_git_author() -> str:
    """Obtém autor do git ou usa padrão"""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "SILA Development Team"


def create_adr_file(
    title: str,
    category: str,
    author: Optional[str] = None,
    decision_date: Optional[str] = None,
) -> Path:
    """Cria arquivo de ADR a partir do template"""

    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Template não encontrado: {TEMPLATE_FILE}")

    # Ler template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Obter informações
    adr_number = get_next_adr_number()
    sanitized_title = sanitize_title(title)
    filename = f"{adr_number}-{sanitized_title}.md"
    filepath = ADR_DIR / filename

    if author is None:
        author = get_git_author()

    if decision_date is None:
        decision_date = datetime.now().strftime("%Y-%m-%d")

    # Substituir placeholders no template
    content = template_content.replace("ADR-XXXX", f"ADR-{adr_number}")
    content = content.replace("[Título da Decisão]", title)
    content = content.replace("[YYYY-MM-DD]", decision_date)
    content = content.replace("[Nomes dos responsáveis]", author)
    content = content.replace("[Nomes dos revisores]", "Equipe de Arquitetura SILA")
    content = content.replace("[categoria]", category)

    # Adicionar tags baseadas na categoria
    tags = [category, "accepted"]
    if category == "architecture":
        tags.extend(["system-design", "patterns"])
    elif category == "technology":
        tags.extend(["tools", "framework"])
    elif category == "security":
        tags.extend(["security", "compliance"])
    elif category == "data":
        tags.extend(["database", "persistence"])
    elif category == "deployment":
        tags.extend(["devops", "infrastructure"])
    elif category == "quality":
        tags.extend(["testing", "standards"])

    content = content.replace(
        "`[categoria]` `[tecnologia]` `[impacto]` `[status]`",
        " ".join([f"`{tag}`" for tag in tags]),
    )

    # Escrever arquivo
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def update_index(filepath: Path, title: str, category: str, status: str = "Proposto"):
    """Atualiza o índice de ADRs (placeholder - implementação futura)"""
    print(f"📝 Para adicionar {filepath.name} ao índice, execute:")
    print(f"   python scripts/adr/generate_index.py")


def validate_category(category: str) -> bool:
    """Valida se a categoria é válida"""
    return category in VALID_CATEGORIES


def main():
    parser = argparse.ArgumentParser(
        description="Gerar novo ADR (Architectural Decision Record)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --title "Migration to Microservices" --category "architecture"
  %(prog)s --title "Add Redis Cache" --category "technology" --author "João Silva"
  %(prog)s --title "Security Audit Process" --category "security" --date "2025-12-01"

Categorias válidas:
  """
        + ", ".join(VALID_CATEGORIES),
    )

    parser.add_argument(
        "--title", required=True, help="Título da decisão arquitetônica"
    )

    parser.add_argument(
        "--category",
        required=True,
        choices=VALID_CATEGORIES,
        help="Categoria da decisão",
    )

    parser.add_argument(
        "--author", help="Nome do autor/responsável (padrão: git config user.name)"
    )

    parser.add_argument(
        "--date", help="Data da decisão (formato: YYYY-MM-DD, padrão: hoje)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar o que seria criado sem criar arquivos",
    )

    args = parser.parse_args()

    # Validar data se fornecida
    if args.date:
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("❌ Erro: Data deve estar no formato YYYY-MM-DD")
            return 1

    # Obter informações
    adr_number = get_next_adr_number()
    sanitized_title = sanitize_title(args.title)
    filename = f"{adr_number}-{sanitized_title}.md"
    filepath = ADR_DIR / filename

    if args.dry_run:
        print(f"🔍 Dry run - ADR que seria criado:")
        print(f"   Número: ADR-{adr_number}")
        print(f"   Título: {args.title}")
        print(f"   Categoria: {args.category}")
        print(f"   Arquivo: {filepath}")
        print(f"   Autor: {args.author or get_git_author()}")
        print(f"   Data: {args.date or datetime.now().strftime('%Y-%m-%d')}")
        return 0

    # Verificar se arquivo já existe
    if filepath.exists():
        print(f"❌ Erro: Arquivo {filepath} já existe")
        return 1

    try:
        # Criar diretório se não existir
        ADR_DIR.mkdir(parents=True, exist_ok=True)

        # Criar arquivo ADR
        created_file = create_adr_file(
            title=args.title,
            category=args.category,
            author=args.author,
            decision_date=args.date,
        )

        print(f"✅ ADR criado com sucesso:")
        print(f"   📁 Arquivo: {created_file}")
        print(f"   🔢 Número: ADR-{adr_number}")
        print(f"   📋 Título: {args.title}")
        print(f"   🏷️  Categoria: {args.category}")

        # Instruir sobre próximos passos
        print(f"\n📝 Próximos passos:")
        print(f"   1. Edite o arquivo: {created_file}")
        print(f"   2. Preencha todas as seções do template")
        print(f"   3. Submeta para revisão técnica")
        print(f"   4. Atualize o índice: python scripts/adr/generate_index.py")

        # Sugerir atualização do índice
        update_index(created_file, args.title, args.category)

        return 0

    except Exception as e:
        print(f"❌ Erro ao criar ADR: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
