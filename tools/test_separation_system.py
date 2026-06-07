#!/usr/bin/env python3
"""
🧪 Test Suite - Sistema de Separação Models/Schemas
====================================================
Testa todas as ferramentas do sistema de separação.

Uso:
    python tools/test_separation_system.py
"""

import subprocess
import sys
from pathlib import Path


class SeparationSystemTester:
    """Testador do sistema de separação."""

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.tools = [
            "split_models_schemas.py",
            "audit_imports.py",
            "validate_separation.py",
            "migrate_module.py",
            "migrate_all_modules.py",
        ]
        self.passed = 0
        self.failed = 0

    def run_command(self, cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
        """Executa comando e retorna resultado."""
        try:
            result = subprocess.run(
                cmd, cwd=self.root, capture_output=True, text=True, timeout=timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)

    def test_tool_exists(self, tool: str) -> bool:
        """Testa se ferramenta existe."""
        tool_path = self.root / "tools" / tool
        exists = tool_path.exists()

        if exists:
            print(f"   ✅ {tool} existe")
            self.passed += 1
        else:
            print(f"   ❌ {tool} não encontrado")
            self.failed += 1

        return exists

    def test_tool_help(self, tool: str) -> bool:
        """Testa se ferramenta tem --help."""
        success, output = self.run_command([sys.executable, f"tools/{tool}", "--help"])

        if success and ("usage:" in output.lower() or "uso:" in output.lower()):
            print(f"   ✅ {tool} --help funciona")
            self.passed += 1
            return True
        else:
            print(f"   ❌ {tool} --help falhou")
            self.failed += 1
            return False

    def test_validator_on_location(self) -> bool:
        """Testa validador no módulo location."""
        print("\n🧪 Testando validador no módulo location...")

        success, output = self.run_command(
            [sys.executable, "tools/validate_separation.py", "backend/modules/location"]
        )

        if success and "Separação correta" in output:
            print("   ✅ Validador funcionou corretamente")
            self.passed += 1
            return True
        else:
            print("   ❌ Validador falhou")
            print(f"   Output: {output[:200]}")
            self.failed += 1
            return False

    def test_auditor(self) -> bool:
        """Testa auditor de imports."""
        print("\n🧪 Testando auditor de imports...")

        success, output = self.run_command(
            [sys.executable, "tools/audit_imports.py", "--module", "location"]
        )

        if success:
            print("   ✅ Auditor executou sem erros")
            self.passed += 1
            return True
        else:
            print("   ❌ Auditor falhou")
            print(f"   Output: {output[:200]}")
            self.failed += 1
            return False

    def test_documentation_exists(self) -> bool:
        """Testa se documentação existe."""
        print("\n📚 Verificando documentação...")

        docs = [
            "tools/README_SEPARATION.md",
            "tools/QUICKSTART_SEPARATION.md",
            "tools/SEPARATION_SYSTEM_INDEX.md",
        ]

        all_exist = True
        for doc in docs:
            doc_path = self.root / doc
            if doc_path.exists():
                print(f"   ✅ {doc} existe")
                self.passed += 1
            else:
                print(f"   ❌ {doc} não encontrado")
                self.failed += 1
                all_exist = False

        return all_exist

    def run_tests(self) -> bool:
        """Executa todos os testes."""
        print("🧪 SILA Separation System - Test Suite")
        print("=" * 60)

        # Teste 1: Ferramentas existem
        print("\n📦 Teste 1: Verificando existência das ferramentas...")
        for tool in self.tools:
            self.test_tool_exists(tool)

        # Teste 2: Help funciona
        print("\n📖 Teste 2: Verificando --help das ferramentas...")
        for tool in self.tools:
            self.test_tool_help(tool)

        # Teste 3: Validador funciona
        self.test_validator_on_location()

        # Teste 4: Auditor funciona
        self.test_auditor()

        # Teste 5: Documentação existe
        self.test_documentation_exists()

        # Relatório final
        print("\n" + "=" * 60)
        print("📊 RESULTADO DOS TESTES")
        print("=" * 60)
        print(f"\n✅ Passou: {self.passed}")
        print(f"❌ Falhou: {self.failed}")
        print(f"📊 Total: {self.passed + self.failed}")

        success_rate = (
            (self.passed / (self.passed + self.failed)) * 100
            if (self.passed + self.failed) > 0
            else 0
        )
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")

        if self.failed == 0:
            print("\n🎉 Todos os testes passaram!")
            return True
        else:
            print(f"\n⚠️  {self.failed} teste(s) falharam")
            return False


def main():
    tester = SeparationSystemTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
