#!/usr/bin/env python3
"""
Script para executar testes de unidade dos serviços e gerar relatório de cobertura.

Este script executa todos os testes de unidade focados na lógica de negócio
dos serviços, com mocking adequado para isolar a camada de persistência.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_unit_tests():
    """Executa todos os testes de unidade dos serviços."""
    print("🧪 Executando Testes de Unidade dos Serviços")
    print("=" * 60)

    # Diretório atual
    unit_tests_dir = Path(__file__).parent

    # Lista de arquivos de teste para executar
    test_files = [
        "test_sanitation_service_simple.py",
        "test_justice_service_simple.py",
        "test_academic_service_simple.py",
    ]

    results = {}

    for test_file in test_files:
        test_path = unit_tests_dir / test_file

        if not test_path.exists():
            print(f"❌ Arquivo de teste não encontrado: {test_file}")
            results[test_file] = {"status": "not_found", "tests": 0}
            continue

        print(f"\n📋 Executando {test_file}...")
        print("-" * 40)

        try:
            # Executa pytest com saída detalhada
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                str(test_path),
                "-v",  # verbose
                "--tb=short",  # traceback curto
            ]

            # Cria diretório de relatórios se não existir
            reports_dir = unit_tests_dir / "reports"
            reports_dir.mkdir(exist_ok=True)

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=unit_tests_dir.parent.parent
            )

            if result.returncode == 0:
                print(f"✅ {test_file}: Todos os testes passaram")

                # Conta número de testes executados
                test_count = result.stdout.count("PASSED")
                results[test_file] = {
                    "status": "passed",
                    "tests": test_count,
                    "output": result.stdout,
                }
            else:
                print(f"❌ {test_file}: Alguns testes falharam")
                print("Erros:")
                print(result.stderr)

                # Tenta extrair informações mesmo com falhas
                test_count = result.stdout.count("PASSED") + result.stdout.count(
                    "FAILED"
                )
                results[test_file] = {
                    "status": "failed",
                    "tests": test_count,
                    "output": result.stdout,
                    "errors": result.stderr,
                }

        except Exception as e:
            print(f"❌ Erro ao executar {test_file}: {str(e)}")
            results[test_file] = {"status": "error", "tests": 0, "error": str(e)}

    return results


def generate_coverage_report():
    """Gera relatório de cobertura dos testes de unidade."""
    print("\n📊 Gerando Relatório de Cobertura")
    print("=" * 60)

    unit_tests_dir = Path(__file__).parent

    try:
        # Executa pytest com cobertura
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(unit_tests_dir),
            "--cov=modules.sanitation.services",
            "--cov=modules.justice.services",
            "--cov=modules.education.services",
            "--cov-report=term-missing",
            "--cov-report=html",
            f"--cov-report=json:{unit_tests_dir / 'reports' / 'coverage.json'}",
            "--cov-fail-under=70",  # mínimo 70% de cobertura
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=unit_tests_dir.parent.parent
        )

        if result.returncode == 0:
            print("✅ Relatório de cobertura gerado com sucesso")
            print("📁 Relatório HTML disponível em: htmlcov/index.html")

            # Extrai informações de cobertura
            coverage_output = result.stdout
            print("\n📈 Resumo da Cobertura:")
            print(coverage_output)

            return True
        else:
            print("❌ Falha na geração do relatório de cobertura")
            print("Erro:")
            print(result.stderr)

            # Verifica se é problema de dependência
            if "pytest-cov" in result.stderr:
                print("💡 Dica: Instale pytest-cov com: pip install pytest-cov")

            return False

    except Exception as e:
        print(f"❌ Erro ao gerar relatório de cobertura: {str(e)}")
        return False


def analyze_test_functions():
    """Analisa as funções de teste criadas."""
    print("\n🔍 Analisando Funções de Teste")
    print("=" * 60)

    unit_tests_dir = Path(__file__).parent
    test_files = [
        "test_sanitation_service.py",
        "test_justice_service.py",
        "test_academic_service.py",
    ]

    analysis = {}

    for test_file in test_files:
        test_path = unit_tests_dir / test_file

        if not test_path.exists():
            continue

        try:
            with open(test_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Conta diferentes tipos de testes
            test_methods = content.count("def test_")
            async_tests = content.count("@pytest.mark.asyncio")
            mock_tests = content.count("mock_")
            assertion_tests = content.count("assert ")

            analysis[test_file] = {
                "total_tests": test_methods,
                "async_tests": async_tests,
                "mock_usage": mock_tests,
                "assertions": assertion_tests,
                "lines": len(content.splitlines()),
            }

            print(f"\n📋 {test_file}:")
            print(f"  • Total de testes: {test_methods}")
            print(f"  • Testes assíncronos: {async_tests}")
            print(f"  • Uso de mocks: {mock_tests}")
            print(f"  • Asserts: {assertion_tests}")
            print(f"  • Linhas de código: {analysis[test_file]['lines']}")

        except Exception as e:
            print(f"❌ Erro ao analisar {test_file}: {str(e)}")
            analysis[test_file] = {"error": str(e)}

    return analysis


def generate_summary_report(test_results, coverage_success, analysis):
    """Gera relatório resumido."""
    print("\n📋 Relatório Resumido")
    print("=" * 60)

    # Estatísticas dos testes
    total_tests = sum(result.get("tests", 0) for result in test_results.values())
    passed_tests = sum(
        1 for result in test_results.values() if result.get("status") == "passed"
    )
    failed_tests = sum(
        1 for result in test_results.values() if result.get("status") == "failed"
    )

    print(f"\n📊 Estatísticas dos Testes:")
    print(f"  • Total de testes executados: {total_tests}")
    print(f"  • Arquivos com sucesso: {passed_tests}")
    print(f"  • Arquivos com falhas: {failed_tests}")
    print(
        f"  • Taxa de sucesso: {(passed_tests/len(test_results)*100):.1f}%"
        if test_results
        else "N/A"
    )

    # Estatísticas de análise
    total_test_functions = sum(info.get("total_tests", 0) for info in analysis.values())
    total_async_tests = sum(info.get("async_tests", 0) for info in analysis.values())
    total_lines = sum(info.get("lines", 0) for info in analysis.values())

    print(f"\n📈 Análise de Código:")
    print(f"  • Funções de teste: {total_test_functions}")
    print(f"  • Testes assíncronos: {total_async_tests}")
    print(f"  • Linhas totais: {total_lines}")

    # Status da cobertura
    coverage_status = "✅ Sucesso" if coverage_success else "❌ Falha"
    print(f"\n🎯 Cobertura de Código: {coverage_status}")

    # Salva relatório em JSON
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "test_results": test_results,
        "coverage_success": coverage_success,
        "analysis": analysis,
        "summary": {
            "total_tests": total_tests,
            "passed_files": passed_tests,
            "failed_files": failed_tests,
            "total_test_functions": total_test_functions,
            "total_async_tests": total_async_tests,
            "total_lines": total_lines,
        },
    }

    try:
        reports_dir = Path(__file__).parent / "reports"
        reports_dir.mkdir(exist_ok=True)

        report_file = reports_dir / "unit_test_summary.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Relatório salvo em: {report_file}")

    except Exception as e:
        print(f"❌ Erro ao salvar relatório: {str(e)}")

    return report_data


def main():
    """Função principal."""
    print("🚀 Iniciando Execução de Testes de Unidade dos Serviços")
    print("=" * 60)
    print("Foco: Lógica de negócio com mocking da camada de persistência")
    print("=" * 60)

    # Executa testes
    test_results = run_unit_tests()

    # Gera relatório de cobertura
    coverage_success = generate_coverage_report()

    # Analisa funções de teste
    analysis = analyze_test_functions()

    # Gera relatório resumido
    summary = generate_summary_report(test_results, coverage_success, analysis)

    # Status final
    print("\n🏁 Status Final")
    print("=" * 60)

    all_passed = all(
        result.get("status") == "passed" for result in test_results.values()
    )

    if all_passed and coverage_success:
        print("✅ Todos os testes passaram e cobertura OK!")
        return 0
    elif all_passed:
        print("⚠️  Testes OK, mas cobertura abaixo do esperado")
        return 1
    else:
        print("❌ Alguns testes falharam")
        return 2


if __name__ == "__main__":
    sys.exit(main())
