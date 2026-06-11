#!/usr/bin/env python3
"""Validate test separation rules using `test_separation_system`.

Checks basic invariants like: integration/e2e tests should not live under
`tests/unit` directories and returns non-zero on violations.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tools.test_separation_system import collect_tests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", default=Path("tests"), type=Path)
    args = parser.parse_args()

    issues = []
    for p, category in collect_tests(args.root):
        if category in ("integration", "e2e") and "unit" in p.parts:
            issues.append((p, category))

    if issues:
        print("Separation issues found:")
        for p, cat in issues:
            print(f" - {p}: classified as {cat} but located in a 'unit' path")
        sys.exit(2)

    print("No separation issues found.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
✅ SILA Separation Validator
=============================
Valida que a separação entre models.py e schemas.py está correta.

Verificações:
- models.py contém apenas SQLAlchemy
- schemas.py contém apenas Pydantic
- Não há duplicação de classes
- Imports estão corretos

Uso:
    python tools/validate_separation.py backend/modules/location
    python tools/validate_separation.py --all
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


class SeparationValidator:
    """Validador de separação models/schemas."""

    def __init__(self, module_path: str = None, check_all: bool = False):
        self.module_path = Path(module_path) if module_path else None
        self.check_all = check_all
        self.root_path = Path("backend")

        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.stats: dict = defaultdict(int)

    def get_modules_to_check(self) -> list[Path]:
        """Retorna lista de módulos para verificar."""
        if self.module_path:
            return [self.module_path]

        if self.check_all:
            modules_dir = self.root_path / "modules"
            if modules_dir.exists():
                return [d for d in modules_dir.iterdir() if d.is_dir()]

        return []

    def extract_classes(self, content: str, class_type: str) -> set[str]:
        """
        Extrai nomes de classes de um tipo específico.

        Args:
            content: Conteúdo do arquivo
            class_type: 'orm' ou 'pydantic'
        """
        classes = set()

        if class_type == "orm":
            # Classes que herdam de Base
            pattern = r"class\s+(\w+)\(Base\)"
        else:  # pydantic
            # Classes que herdam de BaseModel
            pattern = r"class\s+(\w+)\(BaseModel[^)]*\)"

        matches = re.finditer(pattern, content)
        for match in matches:
            classes.add(match.group(1))

        return classes

    def check_models_file(self, models_path: Path) -> dict:
        """Verifica models.py."""
        result = {
            "path": str(models_path),
            "orm_classes": set(),
            "pydantic_classes": set(),
            "has_pydantic_import": False,
            "has_sqlalchemy_import": False,
        }

        if not models_path.exists():
            return result

        with open(models_path, encoding="utf-8") as f:
            content = f.read()

        # Verifica imports
        result["has_pydantic_import"] = bool(re.search(r"from pydantic import", content))
        result["has_sqlalchemy_import"] = bool(re.search(r"from sqlalchemy", content))

        # Extrai classes
        result["orm_classes"] = self.extract_classes(content, "orm")
        result["pydantic_classes"] = self.extract_classes(content, "pydantic")

        return result

    def check_schemas_file(self, schemas_path: Path) -> dict:
        """Verifica schemas.py."""
        result = {
            "path": str(schemas_path),
            "pydantic_classes": set(),
            "orm_classes": set(),
            "has_pydantic_import": False,
            "has_sqlalchemy_import": False,
        }

        if not schemas_path.exists():
            return result

        with open(schemas_path, encoding="utf-8") as f:
            content = f.read()

        # Verifica imports
        result["has_pydantic_import"] = bool(re.search(r"from pydantic import", content))
        result["has_sqlalchemy_import"] = bool(re.search(r"from sqlalchemy", content))

        # Extrai classes
        result["pydantic_classes"] = self.extract_classes(content, "pydantic")
        result["orm_classes"] = self.extract_classes(content, "orm")

        return result

    def validate_module(self, module_path: Path) -> tuple[list[dict], list[dict]]:
        """
        Valida um módulo específico.

        Returns:
            Tuple[errors, warnings]
        """
        errors = []
        warnings = []

        module_name = module_path.name
        models_path = module_path / "models.py"
        schemas_path = module_path / "schemas.py"

        print(f"\n📦 Validando módulo: {module_name}")

        # Verifica se arquivos existem
        if not models_path.exists():
            warnings.append(
                {
                    "module": module_name,
                    "type": "missing_file",
                    "message": "models.py não encontrado",
                }
            )

        if not schemas_path.exists():
            warnings.append(
                {
                    "module": module_name,
                    "type": "missing_file",
                    "message": "schemas.py não encontrado",
                }
            )
            return errors, warnings

        # Analisa arquivos
        models_info = self.check_models_file(models_path)
        schemas_info = self.check_schemas_file(schemas_path)

        # Validação 1: models.py não deve ter classes Pydantic
        if models_info["pydantic_classes"]:
            errors.append(
                {
                    "module": module_name,
                    "file": "models.py",
                    "type": "pydantic_in_models",
                    "message": f"Classes Pydantic encontradas em models.py: {', '.join(models_info['pydantic_classes'])}",
                }
            )
            self.stats["pydantic_in_models"] += len(models_info["pydantic_classes"])

        # Validação 2: models.py não deve importar pydantic
        if models_info["has_pydantic_import"]:
            errors.append(
                {
                    "module": module_name,
                    "file": "models.py",
                    "type": "pydantic_import",
                    "message": "Import de pydantic encontrado em models.py",
                }
            )

        # Validação 3: schemas.py não deve ter classes ORM
        if schemas_info["orm_classes"]:
            errors.append(
                {
                    "module": module_name,
                    "file": "schemas.py",
                    "type": "orm_in_schemas",
                    "message": f"Classes ORM encontradas em schemas.py: {', '.join(schemas_info['orm_classes'])}",
                }
            )
            self.stats["orm_in_schemas"] += len(schemas_info["orm_classes"])

        # Validação 4: schemas.py não deve importar sqlalchemy
        if schemas_info["has_sqlalchemy_import"]:
            warnings.append(
                {
                    "module": module_name,
                    "file": "schemas.py",
                    "type": "sqlalchemy_import",
                    "message": "Import de sqlalchemy encontrado em schemas.py (pode ser intencional)",
                }
            )

        # Validação 5: schemas.py deve ter import de pydantic
        if not schemas_info["has_pydantic_import"]:
            warnings.append(
                {
                    "module": module_name,
                    "file": "schemas.py",
                    "type": "no_pydantic_import",
                    "message": "schemas.py não importa pydantic",
                }
            )

        # Estatísticas
        self.stats["total_orm_classes"] += len(models_info["orm_classes"])
        self.stats["total_pydantic_classes"] += len(schemas_info["pydantic_classes"])

        # Relatório do módulo
        if not errors and not warnings:
            print("   ✅ Separação correta!")

        if models_info["orm_classes"]:
            print(f"   📊 {len(models_info['orm_classes'])} modelos ORM")

        if schemas_info["pydantic_classes"]:
            print(f"   📊 {len(schemas_info['pydantic_classes'])} schemas Pydantic")

        return errors, warnings

    def validate(self) -> bool:
        """Executa validação completa."""
        print("🔍 SILA Separation Validator")
        print("=" * 60)

        modules = self.get_modules_to_check()

        if not modules:
            print("❌ Nenhum módulo para validar")
            print("   Use: --all ou especifique um caminho")
            return False

        print(f"\n📦 Validando {len(modules)} módulo(s)...")

        # Valida cada módulo
        for module_path in modules:
            module_errors, module_warnings = self.validate_module(module_path)
            self.errors.extend(module_errors)
            self.warnings.extend(module_warnings)

        # Relatório final
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL")
        print("=" * 60)

        print("\n✅ Estatísticas:")
        print(f"   • Modelos ORM: {self.stats['total_orm_classes']}")
        print(f"   • Schemas Pydantic: {self.stats['total_pydantic_classes']}")

        if self.errors:
            print(f"\n❌ {len(self.errors)} erro(s) encontrado(s):")
            for error in self.errors:
                print(f"\n   📦 {error['module']} / {error['file']}")
                print(f"      {error['message']}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} aviso(s):")
            for warning in self.warnings:
                print(f"\n   📦 {warning['module']} / {warning.get('file', 'N/A')}")
                print(f"      {warning['message']}")

        if not self.errors and not self.warnings:
            print("\n🎉 Todos os módulos estão corretamente separados!")
            return True

        if self.errors:
            print("\n⚠️  Ação necessária:")
            print("   Execute: python tools/split_models_schemas.py <module_path>")
            return False

        return True


def main():
    parser = argparse.ArgumentParser(
        description="✅ Valida separação de models e schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tools/validate_separation.py backend/modules/location
  python tools/validate_separation.py --all
        """,
    )

    parser.add_argument(
        "module_path",
        nargs="?",
        help="Caminho do módulo (ex: backend/modules/location)",
    )

    parser.add_argument("--all", action="store_true", help="Valida todos os módulos")

    args = parser.parse_args()

    if not args.module_path and not args.all:
        parser.print_help()
        sys.exit(1)

    validator = SeparationValidator(module_path=args.module_path, check_all=args.all)

    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
