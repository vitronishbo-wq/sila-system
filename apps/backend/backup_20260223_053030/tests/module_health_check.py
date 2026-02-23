"""
🛡️ Sistema de Teste de Saúde de Módulos (Module Health Check)

Este módulo implementa verificações automatizadas de integridade funcional
e comunicação entre os módulos do sistema SILA, simulando o fluxo de dados
do frontend para garantir que cada módulo está devidamente "encaixado".

Funcionalidades:
- Autenticação automática para testes protegidos
- Geração dinâmica de testes por módulo
- Verificação de rotas principais e integração entre módulos
- Relatórios detalhados de saúde do sistema
"""

import asyncio
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx
import pytest
from fastapi.testclient import TestClient

# Configurações do sistema
BASE_URL = settings.API_BASE_URL
TEST_TIMEOUT = 10.0
AUTH_USERNAME = settings.TEST_USERNAME
AUTH_PASSWORD = settings.TEST_PASSWORD

# Adiciona o diretório backend ao path para imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from app.main import app
    from config import settings
except ImportError as e:
    print(f"⚠️ Aviso: Não foi possível importar a aplicação FastAPI: {e}")
    app = None


@dataclass
class ModuleHealthResult:
    """Resultado do teste de saúde de um módulo."""

    module_name: str
    is_healthy: bool
    status_code: Optional[int]
    response_time: float
    error_message: Optional[str] = None
    endpoint_tested: Optional[str] = None
    integration_status: Optional[Dict[str, bool]] = None


@dataclass
class AuthCredentials:
    """Credenciais de autenticação para testes."""

    access_token: Optional[str] = None
    token_type: str = "bearer"
    is_authenticated: bool = False


class ModuleHealthChecker:
    """
    Verificador de saúde de módulos do sistema SILA.

    Executa testes automatizados para verificar se cada módulo está
    devidamente integrado e funcionando corretamente.
    """

    def __init__(self, base_url: str = BASE_URL, timeout: float = TEST_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.auth = AuthCredentials()

        # Módulos críticos identificados na análise do projeto
        self.critical_modules = [
            "auth",
            "citizenship",
            "commercial",
            "health",
            "reports",
            "finance",
            "urbanism",
            "governance",
            "education",
            "justice",
            "documents",
            "notifications",
            "monitoring",
            "integration",
        ]

        # Rotas principais para cada módulo (baseado na análise do main.py)
        self.module_endpoints = {
            "auth": ["/auth/login/access-token", "/auth/me"],
            "citizenship": ["/citizenship/", "/citizenship/health"],
            "commercial": ["/commercial/", "/commercial/licenses"],
            "health": ["/health/", "/health/check"],
            "reports": ["/reports/", "/reports/dashboard"],
            "finance": ["/finance/", "/finance/transactions"],
            "urbanism": ["/urbanism/", "/urbanism/permits"],
            "governance": ["/governance/", "/governance/policies"],
            "education": ["/education/", "/education/schools"],
            "justice": ["/justice/", "/justice/cases"],
            "documents": ["/documents/", "/documents/upload"],
            "notifications": ["/notifications/", "/notifications/send"],
            "monitoring": ["/monitoring/", "/monitoring/metrics"],
            "integration": ["/integration/", "/integration/status"],
        }

        # Integrações críticas entre módulos
        self.critical_integrations = [
            ("reports", "finance", "/reports/financial"),
            ("citizenship", "documents", "/citizenship/documents"),
            ("commercial", "urbanism", "/commercial/zoning-check"),
            ("health", "notifications", "/health/emergency-alert"),
        ]

    async def authenticate(self) -> bool:
        """
        Autentica e obtém token de acesso para testes protegidos.

        Returns:
            bool: True se autenticação foi bem-sucedida
        """
        try:
            # Primeiro, tenta usar TestClient se disponível
            if app:
                test_client = TestClient(app)
                response = test_client.post(
                    "/auth/login/access-token",
                    data={"username": AUTH_USERNAME, "password": AUTH_PASSWORD},
                )

                if response.status_code == 200:
                    token_data = response.json()
                    self.auth.access_token = token_data.get("access_token")
                    self.auth.is_authenticated = True
                    return True

            # Fallback: requisição HTTP direta
            auth_data = {"username": AUTH_USERNAME, "password": AUTH_PASSWORD}

            response = await self.client.post(
                f"{self.base_url}/auth/login/access-token", data=auth_data
            )

            if response.status_code == 200:
                token_data = response.json()
                self.auth.access_token = token_data.get("access_token")
                self.auth.is_authenticated = True
                return True
            else:
                print(
                    f"⚠️ Falha na autenticação: {response.status_code} - {response.text}"
                )
                return False

        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False

    def get_auth_headers(self) -> Dict[str, str]:
        """Retorna headers de autenticação se disponível."""
        if self.auth.is_authenticated and self.auth.access_token:
            return {"Authorization": f"{self.auth.token_type} {self.auth.access_token}"}
        return {}

    async def test_module_endpoint(
        self, module_name: str, endpoint: str
    ) -> ModuleHealthResult:
        """
        Testa um endpoint específico de um módulo.

        Args:
            module_name: Nome do módulo
            endpoint: Endpoint para testar

        Returns:
            ModuleHealthResult: Resultado do teste
        """
        start_time = datetime.now()

        try:
            headers = self.get_auth_headers()
            url = f"{self.base_url}{endpoint}"

            response = await self.client.get(url, headers=headers)
            response_time = (datetime.now() - start_time).total_seconds()

            # Analisa o status code
            is_healthy = response.status_code != 404  # 404 = módulo não encaixado

            result = ModuleHealthResult(
                module_name=module_name,
                is_healthy=is_healthy,
                status_code=response.status_code,
                response_time=response_time,
                endpoint_tested=endpoint,
            )

            # Adiciona mensagem de erro se necessário
            if not is_healthy:
                result.error_message = f"Módulo não encontrado (404) - Rota não existe"
            elif response.status_code == 401:
                result.error_message = "Não autorizado - Verificar autenticação"
            elif response.status_code == 403:
                result.error_message = "Proibido - Usuário sem permissão"
            elif response.status_code >= 500:
                result.error_message = (
                    f"Erro interno do servidor ({response.status_code})"
                )

            return result

        except httpx.TimeoutException:
            return ModuleHealthResult(
                module_name=module_name,
                is_healthy=False,
                status_code=None,
                response_time=TEST_TIMEOUT,
                error_message="Timeout na requisição",
                endpoint_tested=endpoint,
            )
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            return ModuleHealthResult(
                module_name=module_name,
                is_healthy=False,
                status_code=None,
                response_time=response_time,
                error_message=f"Erro na requisição: {str(e)}",
                endpoint_tested=endpoint,
            )

    async def test_module_integration(
        self, module1: str, module2: str, endpoint: str
    ) -> bool:
        """
        Testa integração entre dois módulos.

        Args:
            module1: Primeiro módulo
            module2: Segundo módulo
            endpoint: Endpoint de integração

        Returns:
            bool: True se integração está funcionando
        """
        try:
            headers = self.get_auth_headers()
            url = f"{self.base_url}{endpoint}"

            response = await self.client.get(url, headers=headers)

            # Integração funciona se não retornar 404
            return response.status_code != 404

        except Exception:
            return False

    async def check_module_health(self, module_name: str) -> ModuleHealthResult:
        """
        Verifica a saúde completa de um módulo.

        Args:
            module_name: Nome do módulo a verificar

        Returns:
            ModuleHealthResult: Resultado completo do teste
        """
        if module_name not in self.module_endpoints:
            return ModuleHealthResult(
                module_name=module_name,
                is_healthy=False,
                status_code=None,
                response_time=0.0,
                error_message="Módulo não configurado para teste",
            )

        # Testa o endpoint principal do módulo
        main_endpoint = self.module_endpoints[module_name][0]
        result = await self.test_module_endpoint(module_name, main_endpoint)

        # Testa integrações se o módulo estiver saudável
        if result.is_healthy:
            integration_status = {}
            for module1, module2, endpoint in self.critical_integrations:
                if module1 == module_name or module2 == module_name:
                    integration_status[f"{module1}-{module2}"] = (
                        await self.test_module_integration(module1, module2, endpoint)
                    )
            result.integration_status = integration_status

        return result

    async def run_health_check(self) -> Dict[str, ModuleHealthResult]:
        """
        Executa verificação de saúde para todos os módulos críticos.

        Returns:
            Dict com resultados de todos os módulos
        """
        print("🔐 Autenticando para testes protegidos...")
        auth_success = await self.authenticate()
        if not auth_success:
            print("⚠️ Continuando sem autenticação (alguns testes podem falhar)")

        print(f"🏥 Iniciando verificação de saúde dos módulos...")
        print(f"📊 Testando {len(self.critical_modules)} módulos críticos")

        results = {}

        # Executa testes em paralelo para melhor performance
        tasks = []
        for module_name in self.critical_modules:
            task = asyncio.create_task(self.check_module_health(module_name))
            tasks.append((module_name, task))

        # Coleta resultados
        for module_name, task in tasks:
            try:
                result = await task
                results[module_name] = result

                # Feedback imediato
                status_icon = "✅" if result.is_healthy else "❌"
                print(
                    f"{status_icon} {module_name}: {result.status_code or 'ERRO'} "
                    f"({result.response_time:.2f}s)"
                )

                if not result.is_healthy and result.error_message:
                    print(f"   └─ {result.error_message}")

            except Exception as e:
                results[module_name] = ModuleHealthResult(
                    module_name=module_name,
                    is_healthy=False,
                    status_code=None,
                    response_time=0.0,
                    error_message=f"Erro no teste: {str(e)}",
                )
                print(f"❌ {module_name}: ERRO - {str(e)}")

        return results

    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()

    def generate_report(self, results: Dict[str, ModuleHealthResult]) -> str:
        """
        Gera relatório detalhado dos resultados.

        Args:
            results: Resultados dos testes

        Returns:
            str: Relatório formatado
        """
        healthy_modules = sum(1 for r in results.values() if r.is_healthy)
        total_modules = len(results)
        health_percentage = (
            (healthy_modules / total_modules) * 100 if total_modules > 0 else 0
        )

        report = f"""
🛡️ RELATÓRIO DE SAÚDE DOS MÓDULOS - SILA SYSTEM
{'='*60}

📊 RESUMO GERAL:
   • Módulos saudáveis: {healthy_modules}/{total_modules} ({health_percentage:.1f}%)
   • Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
   • Base URL: {self.base_url}

📋 DETALHES POR MÓDULO:
"""

        for module_name, result in results.items():
            status_icon = "✅" if result.is_healthy else "❌"
            status_text = "SAUDÁVEL" if result.is_healthy else "PROBLEMA"

            report += f"""
{status_icon} {module_name.upper()}: {status_text}
   • Status: {result.status_code or 'N/A'}
   • Tempo: {result.response_time:.2f}s
   • Endpoint: {result.endpoint_tested or 'N/A'}"""

            if result.error_message:
                report += f"\n   • Erro: {result.error_message}"

            if result.integration_status:
                report += "\n   • Integrações:"
                for integration, status in result.integration_status.items():
                    int_icon = "✅" if status else "❌"
                    report += f"\n     - {int_icon} {integration}"

        report += f"""

🎯 RECOMENDAÇÕES:
"""

        unhealthy_modules = [
            name for name, result in results.items() if not result.is_healthy
        ]
        if unhealthy_modules:
            report += (
                f"   • Verificar módulos com problemas: {', '.join(unhealthy_modules)}"
            )
            report += f"\n   • Verificar se o servidor está rodando em {self.base_url}"
            report += f"\n   • Verificar configuração de autenticação"
        else:
            report += f"   • ✅ Todos os módulos estão funcionando corretamente!"
            report += f"\n   • Sistema pronto para uso em produção"

        report += f"\n\n{'='*60}"
        return report


# Fixtures para pytest
@pytest.fixture(scope="session")
async def health_checker():
    """Fixture para o verificador de saúde."""
    checker = ModuleHealthChecker()
    yield checker
    await checker.close()


@pytest.fixture(scope="session")
async def auth_headers(health_checker):
    """Fixture para headers de autenticação."""
    await health_checker.authenticate()
    return health_checker.get_auth_headers()


# Testes parametrizados por módulo
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "module_name",
    [
        "auth",
        "citizenship",
        "commercial",
        "health",
        "reports",
        "finance",
        "urbanism",
        "governance",
        "education",
        "justice",
        "documents",
        "notifications",
        "monitoring",
        "integration",
    ],
)
async def test_module_health(module_name: str, health_checker: ModuleHealthChecker):
    """
    Testa se a rota principal de cada módulo crítico está acessível
    e retorna um status de sucesso (200, 204 ou 403, indicando que a rota existe).
    """
    result = await health_checker.check_module_health(module_name)

    # Verificação principal: módulo deve estar "encaixado" (não 404)
    assert (
        result.status_code != 404
    ), f"❌ Módulo '{module_name}' NÃO ENCAIXADO. Rota principal retornou 404."

    # Verificação de status esperado
    assert result.status_code in [
        200,
        204,
        403,
        401,
    ], f"⚠️ Módulo '{module_name}' retornou código inesperado {result.status_code}."

    # Verificação de tempo de resposta
    assert (
        result.response_time < health_checker.timeout
    ), f"⚠️ Módulo '{module_name}' muito lento: {result.response_time:.2f}s"


@pytest.mark.asyncio
async def test_critical_module_integration(health_checker: ModuleHealthChecker):
    """
    Testa comunicação crítica entre módulos.
    Exemplo: Fazer uma requisição que exige que módulos estejam integrados.
    """
    # Testa integração reports-finance
    integration_works = await health_checker.test_module_integration(
        "reports", "finance", "/reports/financial"
    )

    # Se retornar 404, um dos módulos não está encaixado ou a rota não existe
    assert (
        integration_works
    ), "❌ Falha na integração reports-finance. Verificar se ambos os módulos estão funcionais."


@pytest.mark.asyncio
async def test_system_health_comprehensive(health_checker: ModuleHealthChecker):
    """
    Teste abrangente de saúde do sistema.
    Executa verificação completa e gera relatório.
    """
    results = await health_checker.run_health_check()

    # Gera relatório
    report = health_checker.generate_report(results)
    print(report)

    # Salva relatório em arquivo
    report_file = Path("module_health_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"📄 Relatório salvo em: {report_file.absolute()}")

    # Verifica se pelo menos 80% dos módulos estão saudáveis
    healthy_count = sum(1 for r in results.values() if r.is_healthy)
    total_count = len(results)
    health_percentage = (healthy_count / total_count) * 100

    assert health_percentage >= 80, (
        f"❌ Sistema com baixa saúde: {health_percentage:.1f}% dos módulos saudáveis "
        f"({healthy_count}/{total_count}). Mínimo esperado: 80%"
    )


if __name__ == "__main__":
    """
    Execução standalone do sistema de health check.

    Uso:
        python module_health_check.py
    """

    async def main():
        checker = ModuleHealthChecker()
        try:
            results = await checker.run_health_check()
            report = checker.generate_report(results)
            print(report)

            # Salva relatório
            report_file = Path("module_health_report.txt")
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📄 Relatório salvo em: {report_file.absolute()}")

        finally:
            await checker.close()

    asyncio.run(main())
