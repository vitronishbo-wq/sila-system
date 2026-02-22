#!/usr/bin/env python3
"""
🎯 Demonstração do Sistema de Health Check

Este script demonstra como usar o sistema de verificação de saúde
de módulos em diferentes cenários, simulando situações reais de uso.
"""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório backend ao path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from tests.module_health_check import ModuleHealthChecker, ModuleHealthResult


async def demo_basic_health_check():
    """Demonstração básica do health check."""
    print("🎯 DEMONSTRAÇÃO 1: Health Check Básico")
    print("=" * 50)

    checker = ModuleHealthChecker(base_url="http://127.0.0.1:8000", timeout=5.0)

    try:
        # Autentica
        auth_success = await checker.authenticate()
        print(f"🔐 Autenticação: {'✅ Sucesso' if auth_success else '❌ Falhou'}")

        # Testa alguns módulos específicos
        test_modules = ["auth", "health", "reports"]

        for module in test_modules:
            print(f"\n🏥 Testando módulo: {module}")
            result = await checker.check_module_health(module)

            status_icon = "✅" if result.is_healthy else "❌"
            print(f"   {status_icon} Status: {result.status_code or 'ERRO'}")
            print(f"   ⏱️ Tempo: {result.response_time:.2f}s")
            print(f"   🔗 Endpoint: {result.endpoint_tested or 'N/A'}")

            if result.error_message:
                print(f"   ⚠️ Erro: {result.error_message}")

    finally:
        await checker.close()


async def demo_integration_testing():
    """Demonstração de testes de integração."""
    print("\n\n🎯 DEMONSTRAÇÃO 2: Testes de Integração")
    print("=" * 50)

    checker = ModuleHealthChecker()

    try:
        await checker.authenticate()

        # Testa integrações críticas
        integrations = [
            ("reports", "finance", "/reports/financial"),
            ("citizenship", "documents", "/citizenship/documents"),
            ("commercial", "urbanism", "/commercial/zoning-check"),
        ]

        for module1, module2, endpoint in integrations:
            print(f"\n🔗 Testando integração: {module1} ↔ {module2}")

            integration_works = await checker.test_module_integration(
                module1, module2, endpoint
            )

            status_icon = "✅" if integration_works else "❌"
            print(
                f"   {status_icon} Integração: {'Funcionando' if integration_works else 'Falhou'}"
            )
            print(f"   🔗 Endpoint: {endpoint}")

    finally:
        await checker.close()


async def demo_comprehensive_check():
    """Demonstração de verificação completa."""
    print("\n\n🎯 DEMONSTRAÇÃO 3: Verificação Completa")
    print("=" * 50)

    checker = ModuleHealthChecker()

    try:
        # Executa health check completo
        results = await checker.run_health_check()

        # Gera relatório
        report = checker.generate_report(results)
        print(report)

        # Salva relatório de demonstração
        demo_report_file = Path("demo_health_report.txt")
        with open(demo_report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\n📄 Relatório de demonstração salvo em: {demo_report_file.absolute()}")

    finally:
        await checker.close()


async def demo_error_scenarios():
    """Demonstração de cenários de erro."""
    print("\n\n🎯 DEMONSTRAÇÃO 4: Cenários de Erro")
    print("=" * 50)

    # Simula servidor offline
    print("🔴 Testando com servidor offline...")
    offline_checker = ModuleHealthChecker(
        base_url="http://127.0.0.1:9999", timeout=2.0  # Porta inexistente
    )

    try:
        result = await offline_checker.test_module_endpoint("auth", "/auth/login")
        print(f"   Resultado: {'✅' if result.is_healthy else '❌'}")
        print(f"   Erro: {result.error_message}")

    finally:
        await offline_checker.close()

    # Simula módulo inexistente
    print("\n🔴 Testando módulo inexistente...")
    normal_checker = ModuleHealthChecker()

    try:
        result = await normal_checker.test_module_endpoint(
            "inexistente", "/inexistente/test"
        )
        print(f"   Resultado: {'✅' if result.is_healthy else '❌'}")
        print(f"   Status: {result.status_code}")
        print(f"   Erro: {result.error_message}")

    finally:
        await normal_checker.close()


async def demo_custom_configuration():
    """Demonstração de configuração personalizada."""
    print("\n\n🎯 DEMONSTRAÇÃO 5: Configuração Personalizada")
    print("=" * 50)

    # Cria checker personalizado
    custom_checker = ModuleHealthChecker(base_url="http://localhost:8000", timeout=15.0)

    # Adiciona módulo customizado
    custom_checker.critical_modules.append("custom_module")
    custom_checker.module_endpoints["custom_module"] = [
        "/custom/health",
        "/custom/data",
    ]

    try:
        print("🔧 Configuração personalizada:")
        print(f"   Base URL: {custom_checker.base_url}")
        print(f"   Timeout: {custom_checker.timeout}s")
        print(f"   Módulos: {len(custom_checker.critical_modules)}")
        print(
            f"   Módulo customizado: {'custom_module' in custom_checker.critical_modules}"
        )

        # Testa módulo customizado
        result = await custom_checker.test_module_endpoint(
            "custom_module", "/custom/health"
        )
        print(f"\n🧪 Teste do módulo customizado:")
        print(f"   Resultado: {'✅' if result.is_healthy else '❌'}")
        print(f"   Status: {result.status_code}")

    finally:
        await custom_checker.close()


async def main():
    """Função principal da demonstração."""
    print("🛡️ SILA SYSTEM - Demonstração do Health Check")
    print("=" * 60)
    print("Este script demonstra as funcionalidades do sistema de")
    print("verificação de saúde de módulos em diferentes cenários.")
    print("=" * 60)

    try:
        # Executa todas as demonstrações
        await demo_basic_health_check()
        await demo_integration_testing()
        await demo_comprehensive_check()
        await demo_error_scenarios()
        await demo_custom_configuration()

        print("\n\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print("✅ Todas as funcionalidades foram demonstradas com sucesso.")
        print("📚 Consulte o README_HEALTH_CHECK.md para mais detalhes.")
        print("🚀 Use os scripts em backend/scripts/ para execução real.")

    except KeyboardInterrupt:
        print("\n⏹️ Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante demonstração: {e}")
        print(
            "💡 Certifique-se de que o servidor SILA está rodando em http://127.0.0.1:8000"
        )


if __name__ == "__main__":
    asyncio.run(main())
