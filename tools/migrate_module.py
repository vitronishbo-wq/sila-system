#!/usr/bin/env python3
"""
🚀 SILA Module Migration Orchestrator
======================================
Orquestra o processo completo de separação models/schemas para um módulo.

Executa automaticamente:
1. Validação inicial
2. Separação de models/schemas
3. Auditoria e correção de imports
4. Validação final
5. Sugestão de testes

Uso:
    python tools/migrate_module.py backend/modules/location
    python tools/migrate_module.py backend/modules/payment --skip-tests
"""

import argparse
import subprocess
import sys
from pathlib import Path


class ModuleMigrator:
    """Orquestrador de migração de módulos."""

    def __init__(self, module_path: str, skip_tests: bool = False):
        self.module_path = Path(module_path)
        self.module_name = self.module_path.name
        self.skip_tests = skip_tests
        self.root = Path(__file__).parent.parent

    def run_tool(self, script: str, args: list = None) -> tuple[bool, str]:
        """Executa uma ferramenta e retorna sucesso e output."""
        cmd = [sys.executable, f"tools/{script}"]
        if args:
            cmd.extend(args)

        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout executando comando"
        except Exception as e:
            return False, str(e)

    def print_step(self, step: int, title: str):
        """Imprime cabeçalho de etapa."""
        print(f"\n{'=' * 60}")
        print(f"📍 ETAPA {step}: {title}")
        print("=" * 60)

    def validate_initial(self) -> bool:
        """Validação inicial do módulo."""
        self.print_step(1, "Validação Inicial")

        if not self.module_path.exists():
            print(f"❌ Módulo não encontrado: {self.module_path}")
            return False

        models_file = self.module_path / "models.py"
        if not models_file.exists():
            print(f"❌ models.py não encontrado em {self.module_path}")
            return False

        print(f"✅ Módulo encontrado: {self.module_name}")
        print("✅ models.py existe")

        return True

    def separate_models_schemas(self) -> bool:
        """Separa models e schemas."""
        self.print_step(2, "Separação Models/Schemas")

        success, output = self.run_tool("split_models_schemas.py", [str(self.module_path)])

        print(output)

        if not success:
            print("❌ Erro na separação")
            return False

        return True

    def audit_imports(self) -> bool:
        """Audita e corrige imports."""
        self.print_step(3, "Auditoria de Importações")

        # Primeiro audita
        print("🔍 Auditando imports...")
        success, output = self.run_tool("audit_imports.py", ["--module", self.module_name])

        if "Nenhum problema encontrado" in output:
            print("✅ Nenhum problema de import encontrado")
            return True

        # Se encontrou problemas, corrige
        print("🔧 Problemas encontrados, corrigindo...")
        success, output = self.run_tool("audit_imports.py", ["--module", self.module_name, "--fix"])

        print(output)

        return success

    def validate_final(self) -> bool:
        """Validação final."""
        self.print_step(4, "Validação Final")

        success, output = self.run_tool("validate_separation.py", [str(self.module_path)])

        print(output)

        if not success or "erro" in output.lower():
            print("❌ Validação falhou")
            return False

        return True

    def suggest_tests(self):
        """Sugere comandos de teste."""
        self.print_step(5, "Testes Sugeridos")

        test_path = self.root / "tests" / "modules" / self.module_name

        if test_path.exists():
            print(f"✅ Testes encontrados em: {test_path}")
            print("\n🧪 Execute os testes:")
            print(f"   pytest tests/modules/{self.module_name}/ -v")
            print(f"   pytest tests/modules/{self.module_name}/ --cov")
        else:
            print(f"⚠️  Nenhum teste encontrado em: {test_path}")
            print("\n💡 Considere criar testes para o módulo")

        print("\n🔍 Verificações manuais recomendadas:")
        print(f"   1. Revisar {self.module_path}/models.py")
        print(f"   2. Revisar {self.module_path}/schemas.py")
        print(f"   3. Verificar {self.module_path}/__init__.py")
        print("   4. Testar endpoints relacionados")

    def migrate(self) -> bool:
        """Executa migração completa."""
        print("🚀 SILA Module Migration Orchestrator")
        print(f"📦 Módulo: {self.module_name}")
        print(f"📂 Caminho: {self.module_path}")

        # Etapa 1: Validação inicial
        if not self.validate_initial():
            return False

        # Etapa 2: Separação
        if not self.separate_models_schemas():
            print("\n❌ Migração falhou na separação")
            return False

        # Etapa 3: Auditoria de imports
        if not self.audit_imports():
            print("\n⚠️  Aviso: Problemas na auditoria de imports")
            print("   Revise manualmente os imports")

        # Etapa 4: Validação final
        if not self.validate_final():
            print("\n❌ Migração falhou na validação final")
            return False

        # Etapa 5: Sugestões de teste
        if not self.skip_tests:
            self.suggest_tests()

        # Resumo final
        print("\n" + "=" * 60)
        print("✨ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print(f"\n📦 Módulo {self.module_name} migrado com sucesso!")
        print("\n📋 Arquivos modificados:")
        print(f"   • {self.module_path}/models.py (limpo)")
        print(f"   • {self.module_path}/schemas.py (atualizado)")
        print("   • Backups criados (.py.bak)")

        print("\n🎯 Próximos passos:")
        print("   1. Revisar as mudanças")
        print("   2. Executar testes")
        print("   3. Commit das alterações")
        print("   4. Code review")

        return True


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Orquestra migração completa de um módulo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tools/migrate_module.py backend/modules/location
  python tools/migrate_module.py backend/modules/payment --skip-tests
        """,
    )

    parser.add_argument("module_path", help="Caminho do módulo (ex: backend/modules/location)")

    parser.add_argument("--skip-tests", action="store_true", help="Pula sugestões de testes")

    args = parser.parse_args()

    migrator = ModuleMigrator(args.module_path, args.skip_tests)
    success = migrator.migrate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
