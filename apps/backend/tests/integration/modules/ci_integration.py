#!/usr/bin/env python3
"""
Script de integração dos novos testes com o pipeline de CI/CD.
Verifica se os novos módulos atendem aos critérios de qualidade.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class TestQualityChecker:
    """Verificador de qualidade dos testes."""

    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent.parent
        self.modules_dir = Path(__file__).parent
        self.required_modules = ["sanitation", "justice", "education"]
        self.min_tests_per_module = 15
        self.min_coverage = 70.0
        self.results = {}

    def check_test_files_exist(self):
        """Verifica se os arquivos de teste existem."""
        print("🔍 Verificando existência dos arquivos de teste...")

        for module in self.required_modules:
            module_path = self.modules_dir / module
            required_files = [
                "test_endpoints.py",
                "test_services.py",
                "test_schemas.py",
            ]

            self.results[module] = {
                "files_exist": True,
                "missing_files": [],
                "test_count": 0,
                "coverage": 0.0,
            }

            for file_name in required_files:
                file_path = module_path / file_name
                if not file_path.exists():
                    self.results[module]["files_exist"] = False
                    self.results[module]["missing_files"].append(file_name)
                    print(f"❌ {module}: {file_name} não encontrado")
                else:
                    print(f"✅ {module}: {file_name} encontrado")

    def count_test_functions(self):
        """Conta o número de funções de teste por módulo."""
        print("\n🔢 Contando funções de teste...")

        for module in self.required_modules:
            module_path = self.modules_dir / module
            test_count = 0

            for test_file in module_path.glob("test_*.py"):
                try:
                    with open(test_file, encoding="utf-8") as f:
                        content = f.read()
                        test_count += content.count("def test_")
                except Exception as e:
                    print(f"❌ Erro ao ler {test_file}: {e}")

            self.results[module]["test_count"] = test_count

            if test_count >= self.min_tests_per_module:
                print(
                    f"✅ {module}: {test_count} funções de teste (mínimo: {self.min_tests_per_module})"
                )
            else:
                print(
                    f"❌ {module}: {test_count} funções de teste (mínimo: {self.min_tests_per_module})"
                )

    def run_syntax_check(self):
        """Verifica sintaxe dos arquivos de teste."""
        print("\n🔍 Verificando sintaxe dos arquivos...")

        for module in self.required_modules:
            module_path = self.modules_dir / module
            syntax_ok = True

            for test_file in module_path.glob("test_*.py"):
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "py_compile", str(test_file)],
                        capture_output=True,
                        text=True,
                    )

                    if result.returncode == 0:
                        print(f"✅ {module}: {test_file.name} - sintaxe OK")
                    else:
                        print(f"❌ {module}: {test_file.name} - erro de sintaxe")
                        print(f"   {result.stderr}")
                        syntax_ok = False
                except Exception as e:
                    print(f"❌ {module}: {test_file.name} - erro ao verificar sintaxe: {e}")
                    syntax_ok = False

            self.results[module]["syntax_ok"] = syntax_ok

    def check_import_quality(self):
        """Verifica qualidade dos imports nos arquivos de teste."""
        print("\n📦 Verificando qualidade dos imports...")

        for module in self.required_modules:
            module_path = self.modules_dir / module
            import_issues = []

            for test_file in module_path.glob("test_*.py"):
                try:
                    with open(test_file, encoding="utf-8") as f:
                        content = f.read()
                        lines = content.split("\n")

                        # Verifica imports hardcoded
                        for i, line in enumerate(lines, 1):
                            if "from apps.backend.app." in line and "test" not in str(test_file):
                                if "main" not in line:  # main.py é aceitável
                                    import_issues.append(
                                        f"{test_file.name}:{i} - import direto de app"
                                    )

                            # Verifica imports relativos
                            if line.strip().startswith("from .."):
                                import_issues.append(f"{test_file.name}:{i} - import relativo")

                except Exception as e:
                    import_issues.append(f"{test_file.name} - erro ao analisar imports: {e}")

            if not import_issues:
                print(f"✅ {module}: imports OK")
                self.results[module]["imports_ok"] = True
            else:
                print(f"⚠️  {module}: {len(import_issues)} problemas nos imports")
                for issue in import_issues:
                    print(f"   - {issue}")
                self.results[module]["imports_ok"] = False

    def generate_quality_report(self):
        """Gera relatório de qualidade."""
        print("\n📊 Gerando relatório de qualidade...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "modules": self.required_modules,
            "criteria": {
                "min_tests_per_module": self.min_tests_per_module,
                "min_coverage": self.min_coverage,
            },
            "results": self.results,
            "summary": {
                "total_modules": len(self.required_modules),
                "modules_with_files": sum(
                    1 for r in self.results.values() if r.get("files_exist", False)
                ),
                "total_test_functions": sum(r.get("test_count", 0) for r in self.results.values()),
                "modules_with_min_tests": sum(
                    1
                    for r in self.results.values()
                    if r.get("test_count", 0) >= self.min_tests_per_module
                ),
                "modules_syntax_ok": sum(
                    1 for r in self.results.values() if r.get("syntax_ok", False)
                ),
                "modules_imports_ok": sum(
                    1 for r in self.results.values() if r.get("imports_ok", False)
                ),
            },
        }

        # Salva relatório
        report_file = self.backend_dir / "test_quality_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📄 Relatório salvo em: {report_file}")

        # Exibe resumo
        summary = report["summary"]
        print("\n📈 RESUMO:")
        print(f"   Módulos verificados: {summary['total_modules']}")
        print(f"   Módulos com arquivos: {summary['modules_with_files']}")
        print(f"   Total de testes: {summary['total_test_functions']}")
        print(f"   Módulos com testes mínimos: {summary['modules_with_min_tests']}")
        print(f"   Módulos com sintaxe OK: {summary['modules_syntax_ok']}")
        print(f"   Módulos com imports OK: {summary['modules_imports_ok']}")

        return report

    def check_ci_readiness(self):
        """Verifica se os testes estão prontos para CI/CD."""
        print("\n🚀 Verificando prontidão para CI/CD...")

        ready = True
        checks = []

        # Verifica se todos os arquivos existem
        all_files_exist = all(r.get("files_exist", False) for r in self.results.values())
        if all_files_exist:
            checks.append("✅ Todos os arquivos de teste existem")
        else:
            checks.append("❌ Faltam arquivos de teste")
            ready = False

        # Verifica número mínimo de testes
        all_min_tests = all(
            r.get("test_count", 0) >= self.min_tests_per_module for r in self.results.values()
        )
        if all_min_tests:
            checks.append("✅ Todos os módulos têm testes suficientes")
        else:
            checks.append("❌ Módulos com testes insuficientes")
            ready = False

        # Verifica sintaxe
        all_syntax_ok = all(r.get("syntax_ok", False) for r in self.results.values())
        if all_syntax_ok:
            checks.append("✅ Sintaxe de todos os arquivos OK")
        else:
            checks.append("❌ Erros de sintaxe encontrados")
            ready = False

        # Verifica imports
        all_imports_ok = all(r.get("imports_ok", False) for r in self.results.values())
        if all_imports_ok:
            checks.append("✅ Imports de todos os arquivos OK")
        else:
            checks.append("⚠️  Problemas nos imports (revisar)")

        for check in checks:
            print(f"   {check}")

        if ready:
            print("\n🎉 Testes prontos para integração com CI/CD!")
        else:
            print("\n⚠️  Corrija os problemas antes de integrar com CI/CD")

        return ready

    def create_ci_config(self):
        """Cria configuração para CI/CD."""
        print("\n⚙️  Criando configuração para CI/CD...")

        ci_config = {
            "test_modules": self.required_modules,
            "test_command": "python -m pytest tests/integration/modules/sanitation tests/integration/modules/justice tests/integration/modules/education -v --cov=modules.sanitation --cov=modules.justice --cov=modules.education --cov-fail-under=70",
            "quality_gate": {
                "min_tests_per_module": self.min_tests_per_module,
                "min_coverage": self.min_coverage,
                "require_all_files": True,
                "require_syntax_check": True,
            },
        }

        config_file = self.backend_dir / "ci_test_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(ci_config, f, indent=2, ensure_ascii=False)

        print(f"📄 Configuração CI/CD salva em: {config_file}")

        # Cria script para GitHub Actions
        github_actions_dir = self.backend_dir / ".github" / "workflows"
        github_actions_dir.mkdir(parents=True, exist_ok=True)

        workflow_content = f"""name: Test New Modules

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-new-modules:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run quality checks
      run: |
        python tests/integration/modules/ci_integration.py

    - name: Run tests with coverage
      run: |
        python -m pytest tests/integration/modules/sanitation tests/integration/modules/justice tests/integration/modules/education -v --cov=modules.sanitation --cov=modules.justice --cov=modules.education --cov-report=xml --cov-fail-under={self.min_coverage}

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: new-modules
        name: new-modules-coverage
"""

        workflow_file = github_actions_dir / "test-new-modules.yml"
        with open(workflow_file, "w", encoding="utf-8") as f:
            f.write(workflow_content)

        print(f"📄 Workflow GitHub Actions criado: {workflow_file}")

    def run_all_checks(self):
        """Executa todas as verificações."""
        print("🔍 Iniciando verificação de qualidade dos testes...")

        self.check_test_files_exist()
        self.count_test_functions()
        self.run_syntax_check()
        self.check_import_quality()

        self.generate_quality_report()
        ready = self.check_ci_readiness()

        if ready:
            self.create_ci_config()

        return ready


def main():
    """Função principal."""
    checker = TestQualityChecker()

    try:
        ready = checker.run_all_checks()

        if ready:
            print("\n✅ Verificação concluída com sucesso!")
            print("🚀 Os testes estão prontos para produção e CI/CD")
            sys.exit(0)
        else:
            print("\n❌ Verificação falhou!")
            print("🔧 Corrija os problemas identificados antes de prosseguir")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 Erro durante verificação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
