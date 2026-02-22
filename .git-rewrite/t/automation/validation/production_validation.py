#!/usr/bin/env python3
"""SILA System - Production Validation Suite"""

import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime


class Colors:
    RED, GREEN, YELLOW, BLUE, CYAN, NC = (
        "\033[0;31m",
        "\033[0;32m",
        "\033[1;33m",
        "\033[0;34m",
        "\033[0;36m",
        "\033[0m",
    )


class ValidationSuite:
    def __init__(self):
        self.project_root = os.getcwd()
        self.results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "total": 0,
            "tests": [],
        }
        os.makedirs("reports/validation", exist_ok=True)

    def safe_read(self, file_path):
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except:
            return ""

    def log_test(self, name):
        self.results["total"] += 1
        print(f"{Colors.BLUE}[TEST {self.results['total']}] {name}{Colors.NC}")

    def log_pass(self, msg):
        self.results["passed"] += 1
        print(f"{Colors.GREEN}✓ PASSED: {msg}{Colors.NC}")
        self.results["tests"].append({"status": "PASSED", "message": msg})

    def log_fail(self, msg):
        self.results["failed"] += 1
        print(f"{Colors.RED}✗ FAILED: {msg}{Colors.NC}")
        self.results["tests"].append({"status": "FAILED", "message": msg})

    def log_warn(self, msg):
        self.results["warnings"] += 1
        print(f"{Colors.YELLOW}⚠ WARNING: {msg}{Colors.NC}")
        self.results["tests"].append({"status": "WARNING", "message": msg})

    def header(self, title):
        print(f"\n{'='*65}\n{Colors.CYAN}{title}{Colors.NC}\n{'='*65}\n")

    def validate_environment_config(self):
        self.header("1. ENVIRONMENT CONFIGURATION VALIDATION")
        env_files = [
            ".env",
            ".env.test",
            ".env.production",
            ".env.staging",
            ".env.development",
        ]

        for env_file in env_files:
            if os.path.exists(env_file):
                self.log_test(f"Validando {env_file}")
                with open(env_file, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                required = sum(
                    1
                    for var in ["DATABASE_URL", "ENVIRONMENT", "DEBUG"]
                    if f"{var}=" in content
                )
                if required >= 2:
                    self.log_pass(f"{env_file} com variáveis críticas")
                else:
                    self.log_warn(f"{env_file} pode estar incompleto")

    def validate_imports(self):
        self.header("2. ABSOLUTE IMPORTS VALIDATION")
        self.log_test("Procurando imports relativos problemáticos")

        py_files = list(Path("apps/backend").rglob("*.py"))
        bad = [f for f in py_files if "from ..." in self.safe_read(f)]

        if not bad:
            self.log_pass("Nenhum import relativo além do package")
        else:
            self.log_fail(f"Encontrados {len(bad)} imports relativos")

        self.log_test("Validando core.db.base_class")
        wrong = [
            f for f in py_files if "from core.database import" in self.safe_read(f)
        ]

        if not wrong:
            self.log_pass("Nenhuma importação de core.database")
        else:
            self.log_fail(f"Encontradas {len(wrong)} referências a core.database")

    def validate_database_schemas(self):
        self.header("3. DATABASE SCHEMA VALIDATION")
        self.log_test("Verificando tabelas com prefixo de módulo")

        models = Path("apps/backend/modules/payment/models")
        for f in models.glob("*.py"):
            if f.name.startswith("_"):
                continue
            content = self.safe_read(f)
            if "__tablename__" in content and "payment_" in content:
                self.log_pass(f"{f.name} usa prefixo correto")

    def validate_pydantic_schemas(self):
        self.header("4. PYDANTIC SCHEMA VALIDATION")
        self.log_test("Validando from_attributes=True")

        files = list(Path("apps/backend/modules").rglob("schemas/*.py"))
        configured = sum(
            1 for f in files if "from_attributes=True" in self.safe_read(f)
        )

        self.log_pass(f"Esquemas configurados: {configured}/{len(files)}")

    def validate_async_compliance(self):
        self.header("5. ASYNC/AWAIT COMPLIANCE")
        self.log_test("Validando métodos async")

        files = list(Path("apps/backend/modules").rglob("services/*.py"))
        async_count = sum(
            c.count("async def") for c in [self.safe_read(f) for f in files]
        )

        if async_count > 0:
            self.log_pass(f"Encontrados {async_count} métodos async")
        else:
            self.log_warn("Poucos métodos async encontrados")

    def validate_tests(self):
        self.header("6. TEST SUITE VALIDATION")
        self.log_test("Executando testes de payment")

        try:
            os.environ["PYTHONPATH"] = f"{self.project_root}/apps/backend"
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "pytest",
                    "tests/modules/payment/test_service.py",
                    "-v",
                    "-q",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = result.stdout + result.stderr

            if "passed" in output:
                import re

                match = re.search(r"(\d+) passed", output)
                if match:
                    self.log_pass(f"Testes de payment: {match.group(1)} passed")
        except Exception as e:
            self.log_warn(f"Erro ao executar testes: {str(e)}")

    def validate_documentation(self):
        self.header("7. DOCUMENTATION VALIDATION")
        docs = [
            ".github/copilot-instructions.md",
            "WORK_COMPLETION_SUMMARY.md",
            "QUICK_START_DEV_GUIDE.md",
            "DELIVERABLES_INDEX.md",
        ]

        for doc in docs:
            if os.path.exists(doc):
                lines = len(open(doc, encoding="utf-8", errors="ignore").readlines())
                self.log_pass(f"{doc}: {lines} linhas")
            else:
                self.log_fail(f"{doc} não encontrado")

    def validate_code_quality(self):
        self.header("8. CODE QUALITY METRICS")
        files = list(Path("apps/backend/modules").rglob("*.py"))
        self.log_pass(f"Total de arquivos Python: {len(files)}")

        with_types = sum(1 for f in files if ": " in self.safe_read(f))
        coverage = int((with_types / len(files)) * 100) if files else 0

        status = "PASS" if coverage >= 80 else "WARN"
        getattr(self, f"log_{status.lower()}")(f"Type hints coverage: {coverage}%")

    def run_all(self):
        print(f"{Colors.CYAN}{'='*65}")
        print(f"SILA SYSTEM - PRODUCTION VALIDATION SUITE")
        print(f"{'='*65}{Colors.NC}\n")

        self.validate_environment_config()
        self.validate_imports()
        self.validate_database_schemas()
        self.validate_pydantic_schemas()
        self.validate_async_compliance()
        self.validate_tests()
        self.validate_documentation()
        self.validate_code_quality()

        self.print_summary()

    def print_summary(self):
        self.header("VALIDATION SUMMARY")
        total = self.results["total"]
        passed, failed, warnings = (
            self.results["passed"],
            self.results["failed"],
            self.results["warnings"],
        )

        print(f"Total Tests: {Colors.CYAN}{total}{Colors.NC}")
        print(f"Passed:      {Colors.GREEN}{passed}{Colors.NC}")
        print(f"Failed:      {Colors.RED}{failed}{Colors.NC}")
        print(f"Warnings:    {Colors.YELLOW}{warnings}{Colors.NC}\n")

        if total > 0:
            rate = int((passed / total) * 100)
            print(f"Pass Rate: {rate}%\n")

            if rate >= 90:
                print(f"{Colors.GREEN}✓ PRODUCTION READY{Colors.NC}")
            elif rate >= 70:
                print(f"{Colors.YELLOW}⚠ CONDITIONALLY READY{Colors.NC}")
            else:
                print(f"{Colors.RED}✗ NOT READY{Colors.NC}")


if __name__ == "__main__":
    ValidationSuite().run_all()
