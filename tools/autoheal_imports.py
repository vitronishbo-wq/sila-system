#!/usr/bin/env python3
"""
🧩 autoheal_imports.py

Ferramenta automática para reconstruir módulos, classes e funções ausentes
baseando-se nos erros de importação gerados por pytest ou outros logs.

Modo de uso:
    1. Gere um log de erros: `pytest > logs/errors.txt 2>&1`
    2. Execute o auto-healer: `python tools/autoheal_imports.py logs/errors.txt`
"""

import re
import sys
from pathlib import Path

# --- Configuração ---
ROOT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = ROOT_DIR / "backend" / "app"

# --- Regex para Parsers de Erro ---
# 'No module named 'app.modules.example''
MODULE_NOT_FOUND_PATTERN = re.compile(r"No module named '([\w\.]+)'")
# 'cannot import name 'MyClass' from 'app.modules.example''
SYMBOL_NOT_FOUND_PATTERN = re.compile(r"cannot import name '(\w+)' from '([\w\.]+)'")


# --- Placeholders Inteligentes ---
def get_placeholder_content(module_path: Path, symbol_name: str) -> str:
    """Gera conteúdo de placeholder com base no caminho do módulo e no nome do símbolo."""
    path_str = module_path.as_posix().lower()

    if "schema" in path_str:
        return f'\n\nfrom pydantic import BaseModel\n\nclass {symbol_name}(BaseModel):\n    """Auto-healed Pydantic schema for {symbol_name}."""\n    pass\n'

    if "model" in path_str:
        return f'\n\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy import Column, Integer\n\nBase = declarative_base()\n\nclass {symbol_name}(Base):\n    """Auto-healed SQLAlchemy model for {symbol_name}."""\n    __tablename__ = \'{symbol_name.lower()}s\'\n    id = Column(Integer, primary_key=True)\n'

    if "get_current_active_user" in symbol_name:
        return f'\n\nfrom fastapi import Depends\nfrom pydantic import BaseModel\n\nclass User(BaseModel): username: str = \'placeholder\'\n\nasync def {symbol_name}(user: User = Depends(User)) -> User:\n    """Auto-healed placeholder for FastAPI dependency."""\n    return user\n'

    # Placeholder padrão (função)
    return f'\n\ndef {symbol_name}(*args, **kwargs):\n    """Auto-healed placeholder for {symbol_name}."""\n    print(\'Warning: This is an auto-healed function.\')\n    return None\n'


# --- Funções Core ---
def ensure_path_and_init(file_path: Path):
    """Garante que todos os diretórios no caminho existam e tenham um __init__.py."""
    current = file_path.parent
    # Traverse up to the APP_DIR, creating __init__.py files along the way.
    while current != APP_DIR.parent and current != current.parent:
        init_file = current / "__init__.py"
        if not init_file.exists():
            print(f"🌱 Criando __init__.py em: {current}")
            init_file.touch()
        current = current.parent


def heal_missing_module(module_name: str):
    """Cria a estrutura de diretórios e o arquivo .py para um módulo ausente."""
    if not module_name.startswith("app."):
        return

    path_parts = module_name.split(".")[1:]
    file_path = APP_DIR.joinpath(*path_parts).with_suffix(".py")

    if file_path.exists():
        return

    print(f"🩹 Curando módulo ausente: {module_name}")
    ensure_path_and_init(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()
    print(f"📄 Criado arquivo: {file_path}")


def heal_missing_symbol(module_name: str, symbol_name: str):
    """Adiciona um símbolo (classe/função) de placeholder a um módulo existente."""
    if not module_name.startswith("app."):
        return

    path_parts = module_name.split(".")[1:]
    file_path = APP_DIR.joinpath(*path_parts).with_suffix(".py")

    if not file_path.exists():
        heal_missing_module(module_name)  # Cria o módulo primeiro se ele não existir

    content = file_path.read_text()
    if f"class {symbol_name}" in content or f"def {symbol_name}" in content:
        return  # Símbolo já existe

    print(f"🧩 Adicionando símbolo '{symbol_name}' em {module_name}")
    placeholder = get_placeholder_content(file_path, symbol_name)
    with file_path.open("a", encoding="utf-8") as f:
        f.write(placeholder)


def parse_and_heal(log_content: str):
    """Analisa o conteúdo do log e aciona as funções de correção."""
    healed = False
    # Pass 1: Curar todos os módulos ausentes primeiro
    for module_name in MODULE_NOT_FOUND_PATTERN.findall(log_content):
        heal_missing_module(module_name)
        healed = True

    # Pass 2: Curar símbolos ausentes
    for symbol, module in SYMBOL_NOT_FOUND_PATTERN.findall(log_content):
        heal_missing_symbol(module, symbol)
        healed = True

    if not healed:
        print("✅ Nenhum erro de importação detectável encontrado no log.")
    else:
        print("\n✨ Processo de auto-cura concluído.")
        print(
            "💡 Re-execute seus testes para verificar se os erros foram resolvidos ou para encontrar novos."
        )


def main():
    """Ponto de entrada do script."""
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} caminho/para/seu/log.txt")
        sys.exit(1)

    log_path = Path(sys.argv[1])
    if not log_path.is_file():
        print(f"❌ Arquivo de log não encontrado: {log_path}")
        sys.exit(1)

    print(f"🩺 Analisando log de erros: {log_path}\n")
    log_content = log_path.read_text(encoding="utf-8")
    parse_and_heal(log_content)


if __name__ == "__main__":
    main()
