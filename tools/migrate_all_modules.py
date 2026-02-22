#!/usr/bin/env python3
"""
🌍 SILA Batch Module Migration
================================
Migra TODOS os módulos do SILA de uma vez.

Uso:
    python tools/migrate_all_modules.py                # Migra tudo
    python tools/migrate_all_modules.py --dry-run      # Simula apenas
    python tools/migrate_all_modules.py --exclude payment,billing  # Exclui módulos
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict
import subprocess


class BatchMigrator:
    """Migrador em lote de módulos."""

    def __init__(self, dry_run: bool = False, exclude: List[str] = None):
        self.root = Path(__file__).parent.parent
        self.modules_dir = self.root / "backend" / "modules"
        self.dry_run = dry_run
        self.exclude = exclude or []

        self.results: Dict[str, bool] = {}
        self.skipped: List[str] = []

    def discover_modules(self) -> List[Path]:
        """Descobre todos os módulos disponíveis."""
        if not self.modules_dir.exists():
            print(f"❌ Diretório de módulos não encontrado: {self.modules_dir}")
            return []

        modules = []
        for item in self.modules_dir.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                # Verifica se tem models.py
                if (item / "models.py").exists():
                    if item.name not in self.exclude:
                        modules.append(item)
                    else:
                        self.skipped.append(item.name)

        return sorted(modules)

    def check_module_needs_migration(self, module_path: Path) -> bool:
        """Verifica se módulo precisa de migração."""
        models_file = module_path / "models.py"

        if not models_file.exists():
            return False

        with open(models_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verifica se tem classes Pydantic
        has_pydantic = "from pydantic import" in content or "BaseModel" in content

        return has_pydantic

    def migrate_module(self, module_path: Path) -> bool:
        """Migra um módulo específico."""
        module_name = module_path.name

        print(f"\n{'='*60}")
        print(f"📦 Migrando: {module_name}")
        print("=" * 60)

        if self.dry_run:
            needs_migration = self.check_module_needs_migration(module_path)
            if needs_migration:
                print(f"   ✅ Módulo precisa de migração")
            else:
                print(f"   ⏭️  Módulo já está limpo")
            return needs_migration

        # Executa migração real
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/migrate_module.py",
                    str(module_path),
                    "--skip-tests",
                ],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            success = result.returncode == 0

            if success:
                print(f"✅ {module_name} migrado com sucesso")
            else:
                print(f"❌ {module_name} falhou")
                print(result.stderr)

            return success

        except subprocess.TimeoutExpired:
            print(f"⏱️  {module_name} timeout")
            return False
        except Exception as e:
            print(f"❌ {module_name} erro: {e}")
            return False

    def run(self) -> bool:
        """Executa migração em lote."""
        print("🌍 SILA Batch Module Migration")
        print("=" * 60)

        if self.dry_run:
            print("🔍 DRY RUN - Nenhuma modificação será feita")

        # Descobre módulos
        modules = self.discover_modules()

        if not modules:
            print("❌ Nenhum módulo encontrado")
            return False

        print(f"\n📦 Encontrados {len(modules)} módulos:")
        for module in modules:
            print(f"   • {module.name}")

        if self.skipped:
            print(f"\n⏭️  Excluídos {len(self.skipped)} módulos:")
            for name in self.skipped:
                print(f"   • {name}")

        # Confirma se não for dry-run
        if not self.dry_run:
            print("\n⚠️  ATENÇÃO: Esta operação irá modificar múltiplos arquivos!")
            response = input("Continuar? (s/N): ")
            if response.lower() not in ["s", "sim", "y", "yes"]:
                print("❌ Operação cancelada")
                return False

        # Migra cada módulo
        print("\n🚀 Iniciando migração...")

        for module in modules:
            success = self.migrate_module(module)
            self.results[module.name] = success

        # Relatório final
        self.print_summary()

        return all(self.results.values())

    def print_summary(self):
        """Imprime resumo da migração."""
        print("\n" + "=" * 60)
        print("📊 RESUMO DA MIGRAÇÃO")
        print("=" * 60)

        successful = [name for name, success in self.results.items() if success]
        failed = [name for name, success in self.results.items() if not success]

        print(f"\n✅ Sucesso: {len(successful)}/{len(self.results)}")
        if successful:
            for name in successful:
                print(f"   • {name}")

        if failed:
            print(f"\n❌ Falhas: {len(failed)}")
            for name in failed:
                print(f"   • {name}")

        if self.skipped:
            print(f"\n⏭️  Excluídos: {len(self.skipped)}")
            for name in self.skipped:
                print(f"   • {name}")

        if not self.dry_run:
            print("\n🎯 Próximos passos:")
            print("   1. Executar testes: pytest tests/")
            print("   2. Validar todos: python tools/validate_separation.py --all")
            print("   3. Revisar mudanças: git diff")
            print(
                "   4. Commit: git add . && git commit -m 'refactor: separate models and schemas'"
            )


def main():
    parser = argparse.ArgumentParser(
        description="🌍 Migra todos os módulos do SILA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tools/migrate_all_modules.py --dry-run
  python tools/migrate_all_modules.py
  python tools/migrate_all_modules.py --exclude payment,billing
        """,
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Simula migração sem modificar arquivos"
    )

    parser.add_argument(
        "--exclude", help="Módulos para excluir (separados por vírgula)"
    )

    args = parser.parse_args()

    exclude = args.exclude.split(",") if args.exclude else []

    migrator = BatchMigrator(dry_run=args.dry_run, exclude=exclude)

    success = migrator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
