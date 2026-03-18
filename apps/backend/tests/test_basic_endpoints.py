"""
Testes básicos dos endpoints reais do SILA Backend
Testes simplificados que funcionam com os endpoints existentes
"""

import httpx
import pytest
from pydantic import BaseModel, ValidationError


class HealthResponseSchema(BaseModel):
    """Schema Pydantic para resposta do endpoint /health"""

    status: str
    service: str
    version: str
    environment: str
    timestamp: float
    database: str


class InfoResponseSchema(BaseModel):
    """Schema Pydantic para resposta do endpoint /info"""

    system: dict
    database: dict
    features: dict


class TestBasicEndpoints:
    """Testes básicos para endpoints existentes"""

    def test_health_endpoint_real(self, client: httpx.Client, test_settings):
        """
        Testa o endpoint /health que realmente existe

        Args:
            client: Cliente HTTP síncrono
            test_settings: Configurações de teste
        """
        response = client.get("/health", timeout=test_settings["health_timeout"])

        # Validação básica
        assert (
            response.status_code == 200
        ), f"Status code esperado 200, recebido {response.status_code}"
        assert response.headers["content-type"] == "application/json"

        # Validação de conteúdo
        data = response.json()
        assert isinstance(data, dict), "Resposta deve ser um dicionário"

        # Validação Pydantic
        try:
            health_response = HealthResponseSchema(**data)
            assert health_response.status in ["healthy", "ok"]
            assert health_response.service == "SILA-System"
            assert health_response.environment == "development"
            assert health_response.database in ["connected", "local"]
        except ValidationError as e:
            pytest.fail(f"Validação Pydantic falhou: {e}")

    def test_info_endpoint_real(self, client: httpx.Client, test_settings):
        """
        Testa o endpoint /info que realmente existe

        Args:
            client: Cliente HTTP síncrono
            test_settings: Configurações de teste
        """
        response = client.get("/info", timeout=test_settings["timeout"])

        # Validação básica
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Validação de conteúdo
        data = response.json()
        assert isinstance(data, dict)

        # Verificar campos obrigatórios
        assert "system" in data
        assert "database" in data
        assert "features" in data

        # Validação Pydantic
        try:
            info_response = InfoResponseSchema(**data)
            assert "system" in info_response.dict()
            assert "database" in info_response.dict()
            assert "features" in info_response.dict()
        except ValidationError as e:
            pytest.fail(f"Validação Pydantic falhou: {e}")

        # Validações específicas dos dados
        system = data["system"]
        assert system["environment"] == "development"
        assert system["debug"] is True

        database = data["database"]
        assert database["host"] == "localhost"
        assert database["database"] == "sila_db"

    def test_docs_endpoint_real(self, client: httpx.Client):
        """
        Testa o endpoint /docs (Swagger UI)

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/docs")

        # Validação básica
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]

    def test_openapi_schema_real(self, client: httpx.Client):
        """
        Testa o endpoint /openapi.json

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/openapi.json")

        # Validação básica
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Validação do schema OpenAPI
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

        # Validações das informações da API
        info = data["info"]
        assert "title" in info
        assert "version" in info
        assert "SILA" in info["title"]

    def test_root_endpoint_real(self, client: httpx.Client):
        """
        Testa o endpoint raiz /

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/")

        # Validação básica
        assert response.status_code == 200

        # Validação de conteúdo
        content = response.text
        assert len(content) > 0, "Endpoint raiz deve retornar conteúdo"

    def test_invalid_endpoint_returns_404(self, client: httpx.Client):
        """
        Testa que endpoints inválidos retornam 404

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/endpoint-inexistente")
        assert response.status_code == 404

    def test_cors_headers_real(self, client: httpx.Client):
        """
        Testa headers CORS nos endpoints

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.options("/health")

        # Deve ter headers CORS presentes
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers

    @pytest.mark.parametrize("endpoint", ["/health", "/info", "/", "/docs"])
    def test_endpoints_response_time(
        self, client: httpx.Client, endpoint, test_settings
    ):
        """
        Testa tempo de resposta dos endpoints principais

        Args:
            client: Cliente HTTP síncrono
            endpoint: Endpoint a ser testado
            test_settings: Configurações de teste
        """
        import time

        start_time = time.time()
        response = client.get(endpoint, timeout=test_settings["timeout"])
        response_time = time.time() - start_time

        # Validação básica
        assert response.status_code == 200

        # Validação de tempo de resposta (deve responder em menos de 5 segundos)
        assert (
            response_time < 5.0
        ), f"Endpoint {endpoint} demorou demais: {response_time:.2f}s"

    @pytest.mark.asyncio
    async def test_health_endpoint_async_real(
        self, async_client: httpx.AsyncClient, test_settings
    ):
        """
        Testa o endpoint /health de forma assíncrona

        Args:
            async_client: Cliente HTTP assíncrono
            test_settings: Configurações de teste
        """
        response = await async_client.get(
            "/health", timeout=test_settings["health_timeout"]
        )

        # Validação básica
        assert (
            response.status_code == 200
        ), f"Status code esperado 200, recebido {response.status_code}"

        # Validação de conteúdo
        data = response.json()
        assert isinstance(data, dict), "Resposta deve ser um dicionário"

        # Validação Pydantic
        try:
            health_response = HealthResponseSchema(**data)
            assert health_response.status in ["healthy", "ok"]
            assert health_response.service == "SILA-System"
            assert health_response.environment == "development"
        except ValidationError as e:
            pytest.fail(f"Validação Pydantic falhou: {e}")


class TestErrorHandling:
    """Testes para tratamento de erros"""

    @pytest.mark.asyncio
    async def test_invalid_method_health(self, async_client: httpx.AsyncClient):
        """
        Testa método inválido no endpoint /health

        Args:
            async_client: Cliente HTTP assíncrono
        """
        response = await async_client.post("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_invalid_method_info(self, client: httpx.Client):
        """
        Testa método inválido no endpoint /info

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.post("/info")
        assert response.status_code == 405  # Method Not Allowed

    def test_large_payload_handling(self, client: httpx.Client):
        """
        Testa tratamento de payload grande

        Args:
            client: Cliente HTTP síncrono
        """
        # Criar payload grande
        large_data = {"data": "x" * 10000}

        response = client.post("/health", json=large_data)
        # Não deveria aceitar POST para /health, mas se aceitar, não deve crashar
        assert response.status_code in [
            405,
            422,
        ]  # Method Not Allowed ou Unprocessable Entity
