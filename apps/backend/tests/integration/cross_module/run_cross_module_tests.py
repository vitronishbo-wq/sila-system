#!/usr/bin/env python3
"""
Script para executar todos os testes de Cross-Module Integration

Este script executa testes de integração entre múltiplos módulos do SILA System,
validando o fluxo completo de negócio e a comunicação entre microsserviços.

Fluxos Testados:
1. Sanitation → Monitoring → Notifications
2. Education → Justice → Finance
3. Health → Monitoring → Notifications
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def run_command(cmd, cwd=None):
    """Executa comando e retorna resultado."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def print_header(title):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f"🧪 {title}")
    print("=" * 80)


def print_section(title):
    """Imprime seção formatada."""
    print(f"\n📋 {title}")
    print("-" * 60)


def run_cross_module_tests():
    """Executa todos os testes de cross-module integration."""

    print_header("CROSS-MODULE INTEGRATION TESTS - SILA System")
    print("Validando integração entre microsserviços do monólito")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Diretório base dos testes
    test_dir = Path(__file__).parent
    backend_dir = test_dir.parent.parent

    results = {}
    total_tests = 0
    total_passed = 0
    total_failed = 0

    # Lista de fluxos de integração para testar
    integration_flows = [
        {
            "name": "Sanitation → Monitoring → Notifications",
            "file": "test_sanitation_monitoring_notifications.py",
            "description": "Registro de saneamento → Monitoramento → Notificações stakeholders",
        },
        {
            "name": "Education → Justice → Finance",
            "file": "test_education_justice_finance.py",
            "description": "Certificados acadêmicos → Validação judicial → Pagamento taxas",
        },
        {
            "name": "Health → Monitoring → Notifications",
            "file": "test_health_monitoring_notifications.py",
            "description": "Registros médicos → Alertas saúde → Notificações pacientes",
        },
    ]

    # Executar cada fluxo de integração
    for flow in integration_flows:
        print_section(f"Executando: {flow['name']}")
        print(f"📝 Descrição: {flow['description']}")

        test_file = test_dir / flow["file"]

        if not test_file.exists():
            print(f"❌ Arquivo de teste não encontrado: {flow['file']}")
            results[flow["name"]] = {
                "status": "NOT_FOUND",
                "tests": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0,
                "error": "File not found",
            }
            continue

        print(f"📂 Arquivo: {test_file}")
        print("⏳ Executando testes...")

        start_time = time.time()

        # Executar pytest com opções detalhadas
        cmd = f"python -m pytest {flow['file']} -v --tb=short --json-report-file=/tmp/{flow['file']}.json"

        # Tentar executar no diretório backend
        returncode, stdout, stderr = run_command(cmd, cwd=backend_dir)

        duration = time.time() - start_time

        if returncode == 0:
            print("✅ Todos os testes passaram!")

            # Tentar extrair estatísticas do output
            try:
                lines = stdout.split("\n")
                for line in lines:
                    if "passed in" in line:
                        # Ex: "10 passed in 2.34s"
                        parts = line.split()
                        tests_passed = int(parts[0])
                        total_tests += tests_passed
                        total_passed += tests_passed

                        results[flow["name"]] = {
                            "status": "PASSED",
                            "tests": tests_passed,
                            "passed": tests_passed,
                            "failed": 0,
                            "duration": duration,
                            "output": stdout,
                        }
                        break
                else:
                    # Fallback se não conseguir extrair do output
                    results[flow["name"]] = {
                        "status": "PASSED",
                        "tests": "unknown",
                        "passed": "unknown",
                        "failed": 0,
                        "duration": duration,
                        "output": stdout,
                    }
            except Exception:
                results[flow["name"]] = {
                    "status": "PASSED",
                    "tests": "unknown",
                    "passed": "unknown",
                    "failed": 0,
                    "duration": duration,
                    "output": stdout,
                }

        else:
            print("❌ Alguns testes falharam!")
            print(f"📄 Output:\n{stdout}")
            if stderr:
                print(f"📄 Erros:\n{stderr}")

            # Tentar extrair estatísticas de falha
            try:
                lines = stdout.split("\n")
                for line in lines:
                    if "failed" in line and "passed" in line:
                        # Ex: "8 passed, 2 failed in 3.45s"
                        parts = line.split()
                        passed_idx = next(i for i, p in enumerate(parts) if p == "passed")
                        failed_idx = next(i for i, p in enumerate(parts) if p == "failed")

                        tests_passed = int(parts[passed_idx - 1])
                        tests_failed = int(parts[failed_idx - 1])
                        total_tests_run = tests_passed + tests_failed

                        total_tests += total_tests_run
                        total_passed += tests_passed
                        total_failed += tests_failed

                        results[flow["name"]] = {
                            "status": "FAILED",
                            "tests": total_tests_run,
                            "passed": tests_passed,
                            "failed": tests_failed,
                            "duration": duration,
                            "output": stdout,
                            "error": stderr,
                        }
                        break
                else:
                    results[flow["name"]] = {
                        "status": "FAILED",
                        "tests": "unknown",
                        "passed": "unknown",
                        "failed": "unknown",
                        "duration": duration,
                        "output": stdout,
                        "error": stderr,
                    }
            except Exception:
                results[flow["name"]] = {
                    "status": "FAILED",
                    "tests": "unknown",
                    "passed": "unknown",
                    "failed": "unknown",
                    "duration": duration,
                    "output": stdout,
                    "error": stderr,
                }

    # Gerar relatório final
    print_header("RELATÓRIO FINAL - CROSS-MODULE INTEGRATION")

    print_section("Resultados por Fluxo")
    for flow_name, result in results.items():
        status_icon = (
            "✅" if result["status"] == "PASSED" else "❌" if result["status"] == "FAILED" else "⚠️"
        )
        print(f"{status_icon} {flow_name}")
        print(f"   Status: {result['status']}")
        print(f"   Testes: {result['tests']}")
        print(f"   Passou: {result['passed']}")
        print(f"   Falhou: {result['failed']}")
        print(f"   Duração: {result['duration']:.2f}s")
        if result.get("error"):
            print(f"   Erro: {result['error'][:100]}...")
        print()

    print_section("Estatísticas Gerais")
    print(f"📊 Total de fluxos testados: {len(integration_flows)}")
    print(f"📊 Total de testes executados: {total_tests}")
    print(f"✅ Testes passados: {total_passed}")
    print(f"❌ Testes falhados: {total_failed}")

    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")

    # Salvar relatório em JSON
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_flows": len(integration_flows),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": ((total_passed / total_tests * 100) if total_tests > 0 else 0),
        },
        "flows": results,
        "integration_flows": integration_flows,
    }

    report_file = test_dir / "reports" / "cross_module_integration_report.json"
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Relatório detalhado salvo em: {report_file}")

    # Status final
    print_header("STATUS FINAL")

    if total_failed == 0 and total_tests > 0:
        print("🎉 TODOS OS FLUXOS DE INTEGRAÇÃO PASSARAM!")
        print("✅ A comunicação entre microsserviços está funcionando corretamente")
        return 0
    elif total_tests == 0:
        print("⚠️  NENHUM TESTE FOI EXECUTADO")
        print("❌ Verifique a configuração dos testes")
        return 1
    else:
        print("⚠️  ALGUNS FLUXOS DE INTEGRAÇÃO FALHARAM")
        print("🔧 Revise os erros e corrija as integrações")
        return 1


def main():
    """Função principal."""
    try:
        return run_cross_module_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️  Testes interrompidos pelo usuário")
        return 1
    except Exception as e:
        print(f"\n\n💥 Erro inesperado: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
