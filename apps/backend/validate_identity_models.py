from __future__ import annotations

import asyncio
import importlib
import sys
from pathlib import Path

from app.core.db import Base

IDENTITY_DIR = Path(__file__).resolve().parent / "app/modules/identity"


def _is_test_or_init_file(filepath: Path) -> bool:
    name = filepath.name
    if name.startswith("__"):
        return True
    if name.endswith("_test.py") or name.startswith("test_"):
        return True
    return "tests" in filepath.parts


def import_python_file(filepath: Path) -> None:
    """Importa dinamicamente um arquivo Python pelo Path."""
    parts = filepath.with_suffix("").parts
    if "app" not in parts:
        raise ValueError(f"Caminho sem pacote app: {filepath}")

    idx = parts.index("app")
    module_name = ".".join(parts[idx:])

    if module_name in sys.modules:
        print(f"SKIP {module_name} ja carregado")
        return

    importlib.import_module(module_name)
    print(f"OK   {module_name} importado")


async def validate_identity_models() -> None:
    if not IDENTITY_DIR.exists():
        raise FileNotFoundError(f"Diretorio nao encontrado: {IDENTITY_DIR}")

    for filepath in sorted(IDENTITY_DIR.rglob("*.py")):
        if _is_test_or_init_file(filepath):
            continue
        try:
            import_python_file(filepath)
        except Exception as exc:  # pragma: no cover
            print(f"FAIL {filepath}: {exc}")

    tables = Base.metadata.tables
    print(f"\nTotal de tabelas registradas no Base: {len(tables)}\n")
    for name in sorted(tables.keys()):
        print(f"TABLE {name}")

    print("\nValidacao completa dos modelos de Identity concluida!")


if __name__ == "__main__":
    asyncio.run(validate_identity_models())
