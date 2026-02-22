#!/usr/bin/env python3
"""
🧠 SILA Model/Schema Separator
================================
Separa automaticamente modelos ORM (SQLAlchemy) de schemas Pydantic.

Uso:
    python tools/split_models_schemas.py backend/modules/location
    python tools/split_models_schemas.py backend/modules/payment --dry-run
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict


class ModelSchemaSeparator:
    """Separador cirúrgico de modelos ORM e schemas Pydantic."""

    def __init__(self, module_path: str, dry_run: bool = False):
        self.module_path = Path(module_path)
        self.models_file = self.module_path / "models.py"
        self.schemas_file = self.module_path / "schemas.py"
        self.dry_run = dry_run

        self.pydantic_classes: List[str] = []
        self.pydantic_imports: set = set()
        self.orm_content: str = ""

    def validate_paths(self) -> bool:
        """Valida se os caminhos existem."""
        if not self.module_path.exists():
            print(f"❌ Módulo não encontrado: {self.module_path}")
            return False

        if not self.models_file.exists():
            print(f"❌ Arquivo models.py não encontrado: {self.models_file}")
            return False

        return True

    def extract_pydantic_classes(self, content: str) -> Tuple[List[str], set]:
        """
        Extrai classes Pydantic do conteúdo.

        Returns:
            Tuple[List[str], set]: (lista de classes, set de imports necessários)
        """
        classes = []
        imports = set()

        # Padrão para detectar classes Pydantic (herdam de BaseModel)
        # Captura a classe completa incluindo docstrings e métodos internos
        pattern = r'(class\s+\w+\(BaseModel[^)]*\):(?:\s*"""[^"]*""")?\s*(?:.*?\n(?:    .*\n|\n))*)'

        matches = re.finditer(pattern, content, re.MULTILINE)

        for match in matches:
            class_text = match.group(1)
            classes.append(class_text)

            # Detecta imports necessários dentro da classe
            if "Optional[" in class_text:
                imports.add("Optional")
            if "List[" in class_text:
                imports.add("List")
            if "Dict[" in class_text:
                imports.add("Dict")
            if "Field(" in class_text:
                imports.add("Field")
            if "validator" in class_text:
                imports.add("validator")
            if "ConfigDict" in class_text or "model_config" in class_text:
                imports.add("ConfigDict")
            if "datetime" in class_text:
                imports.add("datetime")

        return classes, imports

    def build_schemas_content(self, classes: List[str], imports: set) -> str:
        """Constrói o conteúdo do arquivo schemas.py."""
        header = '"""\nLocation Schemas - Auto-generated\n\nPydantic schemas for API validation and serialization.\n"""\n\n'

        # Imports base
        import_lines = ["from pydantic import BaseModel"]

        # Adiciona imports opcionais detectados
        if "ConfigDict" in imports:
            import_lines[0] += ", ConfigDict"
        if "Field" in imports:
            import_lines[0] += ", Field"
        if "validator" in imports:
            import_lines[0] += ", validator"

        # Imports de typing
        typing_imports = []
        if "Optional" in imports:
            typing_imports.append("Optional")
        if "List" in imports:
            typing_imports.append("List")
        if "Dict" in imports:
            typing_imports.append("Dict")

        if typing_imports:
            import_lines.append(f"from typing import {', '.join(typing_imports)}")

        if "datetime" in imports:
            import_lines.append("from datetime import datetime")

        imports_block = "\n".join(import_lines) + "\n\n"

        # Junta as classes
        classes_block = "\n\n".join(classes)

        return header + imports_block + classes_block + "\n"

    def remove_pydantic_from_models(self, content: str, classes: List[str]) -> str:
        """Remove classes Pydantic do models.py."""
        cleaned = content

        # Remove cada classe encontrada
        for class_text in classes:
            cleaned = cleaned.replace(class_text, "")

        # Remove import de BaseModel se existir
        cleaned = re.sub(r"from pydantic import.*\n", "", cleaned)

        # Remove linhas vazias excessivas (mais de 2 seguidas)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        # Remove comentário de schemas se existir
        cleaned = re.sub(r"#\s*✅\s*SCHEMAS.*\n", "", cleaned)

        return cleaned.strip() + "\n"

    def process(self) -> bool:
        """Executa o processo de separação."""
        print(f"\n🔍 Analisando módulo: {self.module_path}")

        if not self.validate_paths():
            return False

        # Lê o arquivo models.py
        with open(self.models_file, "r", encoding="utf-8") as f:
            models_content = f.read()

        # Extrai classes Pydantic
        self.pydantic_classes, self.pydantic_imports = self.extract_pydantic_classes(
            models_content
        )

        if not self.pydantic_classes:
            print("✅ Nenhum schema Pydantic encontrado em models.py")
            print("   O arquivo já está limpo!")
            return True

        print(f"\n📦 Encontrados {len(self.pydantic_classes)} schemas Pydantic:")
        for cls in self.pydantic_classes:
            class_name = re.search(r"class\s+(\w+)", cls).group(1)
            print(f"   • {class_name}")

        # Constrói novo schemas.py
        schemas_content = self.build_schemas_content(
            self.pydantic_classes, self.pydantic_imports
        )

        # Remove Pydantic de models.py
        self.orm_content = self.remove_pydantic_from_models(
            models_content, self.pydantic_classes
        )

        if self.dry_run:
            print("\n🔍 DRY RUN - Nenhum arquivo será modificado")
            print("\n" + "=" * 60)
            print("PREVIEW: schemas.py")
            print("=" * 60)
            print(
                schemas_content[:500] + "..."
                if len(schemas_content) > 500
                else schemas_content
            )
            print("\n" + "=" * 60)
            print("PREVIEW: models.py (limpo)")
            print("=" * 60)
            print(
                self.orm_content[:500] + "..."
                if len(self.orm_content) > 500
                else self.orm_content
            )
            return True

        # Backup do models.py original
        backup_path = self.models_file.with_suffix(".py.bak")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(models_content)
        print(f"\n💾 Backup criado: {backup_path}")

        # Escreve schemas.py
        # Se já existe, faz backup também
        if self.schemas_file.exists():
            schemas_backup = self.schemas_file.with_suffix(".py.bak")
            with open(self.schemas_file, "r", encoding="utf-8") as f:
                with open(schemas_backup, "w", encoding="utf-8") as fb:
                    fb.write(f.read())
            print(f"💾 Backup do schemas.py existente: {schemas_backup}")

        with open(self.schemas_file, "w", encoding="utf-8") as f:
            f.write(schemas_content)
        print(f"✅ Schemas extraídos para: {self.schemas_file}")

        # Escreve models.py limpo
        with open(self.models_file, "w", encoding="utf-8") as f:
            f.write(self.orm_content)
        print(f"✅ Models limpo: {self.models_file}")

        print("\n✨ Separação concluída com sucesso!")
        print("\n⚠️  Próximos passos:")
        print("   1. Execute: python tools/audit_imports.py")
        print("   2. Execute: python tools/validate_separation.py")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="🧠 Separa modelos ORM de schemas Pydantic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tools/split_models_schemas.py backend/modules/location
  python tools/split_models_schemas.py backend/modules/payment --dry-run
        """,
    )

    parser.add_argument(
        "module_path", help="Caminho do módulo (ex: backend/modules/location)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a separação sem modificar arquivos",
    )

    args = parser.parse_args()

    separator = ModelSchemaSeparator(args.module_path, args.dry_run)
    success = separator.process()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
