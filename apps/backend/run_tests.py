#!/usr/bin/env python3
"""
Script para executar suíte de testes do SILA Backend
Opções configuradas para diferentes tipos de testes
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> int:
    """
    Executa um comando e retorna o exit code

    Args:
        cmd: Lista com comando e argumentos
        description: Descrição do que está sendo executado

    Returns:
        int: Exit code do comando
    """
    print(f"\n🚀 {description}")
    print(f"📝 Comando: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode
    except KeyboardInterrupt:
        print("\n❌ Testes interrompidos pelo usuário")
        return 1
    except Exception as e:
        print(f"\n❌ Erro ao executar testes: {e}")
        return 1


def check_server_running():
    """
    Verifica se o servidor está rodando na porta 8003
    """
    try:
        import httpx

        response = httpx.get("http://localhost:8003/health", timeout=5.0)
        return response.status_code == 200
    except:
        return False


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Executar testes do SILA Backend")
    parser.add_argument(
        "--type",
        choices=["smoke", "full", "endpoints", "modules", "coverage", "performance"],
        default="smoke",
        help="Tipo de teste a ser executado",
    )
    parser.add_argument("--port", type=int, default=8003, help="Porta do servidor a ser testada")
    parser.add_argument("--verbose", "-v", action="store_true", help="Saída detalhada dos testes")
    parser.add_argument(
        "--skip-server-check",
        action="store_true",
        help="Pular verificação de servidor rodando",
    )

    args = parser.parse_args()

    print("🧪 SILA Backend - Suíte de Testes Automatizados")
    print("=" * 60)

    # Verificar se o servidor está rodando
    if not args.skip_server_check:
        print(f"🔍 Verificando servidor na porta {args.port}...")
        if not check_server_running():
            print(f"❌ Servidor não está rodando na porta {args.port}")
            print("💡 Inicie o servidor com:")
            print(
                f"   cd /opt/sila-system/backend && uvicorn main:app --host 0.0.0.0 --port {args.port}"
            )
            return 1
        else:
            print(f"✅ Servidor está rodando na porta {args.port}")

    # Base command
    base_cmd = ["python", "-m", "pytest"]

    if args.verbose:
        base_cmd.extend(["-v", "-s"])

    # Adicionar configuração de porta
    base_cmd.extend(["--override-invio", f"TEST_PORT={args.port}"])

    # Selecionar tipo de teste
    if args.type == "smoke":
        # Testes rápidos de verificação básica
        cmd = base_cmd + [
            "tests/test_main_endpoints.py::TestMainEndpoints::test_health_endpoint_sync",
            "tests/test_main_endpoints.py::TestMainEndpoints::test_ping_endpoint",
            "-m",
            "not slow",
        ]
        description = "Testes de Fumaça (Smoke Tests)"

    elif args.type == "endpoints":
        # Testes completos dos endpoints principais
        cmd = base_cmd + ["tests/test_main_endpoints.py", "-m", "api"]
        description = "Testes de Endpoints Principais"

    elif args.type == "modules":
        # Testes de ping dos módulos
        cmd = base_cmd + ["tests/test_modules_ping.py", "-m", "modules"]
        description = "Testes de Módulos"

    elif args.type == "coverage":
        # Testes com relatório de cobertura
        cmd = base_cmd + [
            "--cov=backend",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml",
            "--cov-fail-under=70",
        ]
        description = "Testes com Relatório de Cobertura"

    elif args.type == "performance":
        # Testes de performance
        cmd = base_cmd + [
            "tests/test_main_endpoints.py::TestMainEndpoints::test_endpoints_response_time",
            "tests/test_modules_ping.py::TestModulePingEndpoints::test_module_ping_performance",
            "-m",
            "performance",
        ]
        description = "Testes de Performance"

    else:  # full
        # Executar todos os testes
        cmd = base_cmd + [
            "tests/",
            "--cov=backend",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
        ]
        description = "Suite Completa de Testes"

    # Executar testes
    exit_code = run_command(cmd, description)

    # Exibir resultado
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ Todos os testes passaram com sucesso!")

        # Exibir informações de cobertura se disponível
        if args.type in ["coverage", "full"] and Path("htmlcov/index.html").exists():
            print("📊 Relatório de cobertura gerado: htmlcov/index.html")

    else:
        print(f"❌ Alguns testes falharam (exit code: {exit_code})")
        print("💡 Verifique o log acima para detalhes dos erros")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
