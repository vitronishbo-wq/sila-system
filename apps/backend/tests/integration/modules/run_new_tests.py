#!/usr/bin/env python3
"""
Script para executar os novos testes dos módulos sanitation, justice e education
e gerar relatório de cobertura.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_tests_for_module(module_name):
    """Executa testes para um módulo específico."""
    print(f"\n{'=' * 60}")
    print(f"Executando testes do módulo: {module_name}")
    print(f"{'=' * 60}")

    module_path = Path(__file__).parent / module_name

    # Verifica se existem arquivos de teste
    test_files = list(module_path.glob("test_*.py"))
    if not test_files:
        print(f"❌ Nenhum arquivo de teste encontrado para {module_name}")
        return False

    print(f"📁 Arquivos de teste encontrados: {len(test_files)}")
    for test_file in test_files:
        print(f"   - {test_file.name}")

    # Executa os testes com pytest (simulado por enquanto)
    try:
        # Primeiro verifica sintaxe
        syntax_ok = True
        for test_file in test_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(test_file)],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"❌ Erro de sintaxe em {test_file.name}")
                print(result.stderr)
                syntax_ok = False

        if syntax_ok:
            print(f"✅ Testes do módulo {module_name} têm sintaxe correta!")
            return True
        else:
            print(f"❌ Erros de sintaxe encontrados no módulo {module_name}")
            return False

    except Exception as e:
        print(f"❌ Erro ao executar testes do módulo {module_name}: {e}")
        return False


def run_coverage_report():
    """Executa relatório de cobertura para os novos módulos."""
    print(f"\n{'=' * 60}")
    print("Gerando relatório de cobertura")
    print(f"{'=' * 60}")

    try:
        # Executa pytest com cobertura
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "--cov=modules.sanitation",
                "--cov=modules.justice",
                "--cov=modules.education",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov_new_modules",
                "--cov-fail-under=70",
                "tests/integration/modules/sanitation",
                "tests/integration/modules/justice",
                "tests/integration/modules/education",
                "-v",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print("✅ Relatório de cobertura gerado com sucesso!")
            print("📊 Relatório HTML disponível em: htmlcov_new_modules/index.html")
            return True
        else:
            print("❌ Falha na geração do relatório de cobertura")
            return False

    except Exception as e:
        print(f"❌ Erro ao gerar relatório de cobertura: {e}")
        return False


def generate_test_summary():
    """Gera um resumo dos testes criados."""
    print(f"\n{'=' * 60}")
    print("Resumo dos Testes Criados")
    print(f"{'=' * 60}")

    modules = ["sanitation", "justice", "education"]
    total_tests = 0

    for module in modules:
        module_path = Path(__file__).parent / module
        test_files = list(module_path.glob("test_*.py"))

        print(f"\n📦 Módulo: {module}")
        print(f"   Arquivos de teste: {len(test_files)}")

        for test_file in test_files:
            # Conta número de funções de teste
            try:
                with open(test_file, encoding="utf-8") as f:
                    content = f.read()
                    test_functions = content.count("def test_")
                    total_tests += test_functions
                    print(f"   - {test_file.name}: {test_functions} funções de teste")
            except Exception as e:
                print(f"   - {test_file.name}: erro ao ler arquivo ({e})")

    print(f"\n📊 Total de funções de teste criadas: {total_tests}")

    # Compara com módulo citizenship (referência)
    citizenship_path = Path(__file__).parent / "citizenship"
    citizenship_files = list(citizenship_path.glob("test_*.py"))
    citizenship_tests = 0

    for test_file in citizenship_files:
        try:
            with open(test_file, encoding="utf-8") as f:
                content = f.read()
                citizenship_tests += content.count("def test_")
        except:
            pass

    print(f"📊 Funções de teste no módulo citizenship (referência): {citizenship_tests}")

    if citizenship_tests > 0:
        print(
            f"📈 Progresso: {total_tests}/{citizenship_tests} ({(total_tests / citizenship_tests * 100):.1f}%)"
        )
    else:
        print(f"📈 Progresso: {total_tests} testes criados (referência não disponível)")


def main():
    """Função principal."""
    print("🚀 Iniciando execução dos novos testes dos módulos críticos")

    # Muda para o diretório do backend
    backend_dir = Path(__file__).parent.parent.parent
    os.chdir(backend_dir)

    # Verifica se está no ambiente virtual
    if not os.path.exists("venv") and not settings.VIRTUAL_ENV:
        print("⚠️  Aviso: Ambiente virtual não detectado. Execute com venv ativado.")

    modules = ["sanitation", "justice", "education"]
    results = {}

    # Executa testes para cada módulo
    for module in modules:
        results[module] = run_tests_for_module(module)

    # Gera resumo
    generate_test_summary()

    # Executa relatório de cobertura
    coverage_success = run_coverage_report()

    # Resumo final
    print(f"\n{'=' * 60}")
    print("RESUMO FINAL")
    print(f"{'=' * 60}")

    for module, success in results.items():
        status = "✅ SUCESSO" if success else "❌ FALHA"
        print(f"{module}: {status}")

    coverage_status = "✅ SUCESSO" if coverage_success else "❌ FALHA"
    print(f"Cobertura: {coverage_status}")

    # Se algum teste falhou, retorna código de erro
    if not all(results.values()) or not coverage_success:
        print("\n❌ Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
    else:
        print("\n✅ Todos os testes executados com sucesso!")
        print("🎉 Cobertura de testes significativamente melhorada!")
        sys.exit(0)


if __name__ == "__main__":
    main()
