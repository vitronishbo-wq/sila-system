"""
Testes dos endpoints principais do SILA Backend
Testes completos para /ping, /health e endpoints raiz
"""

import json

import httpx
import pytest
from jsonschema import ValidationError as JsonSchemaValidationError
from jsonschema import validate
from pydantic import BaseModel, ValidationError


class PingResponseSchema(BaseModel):
    """Schema Pydantic para resposta do endpoint /ping"""

    status: str
    message: str
    timestamp: str
    service: str


class HealthResponseSchema(BaseModel):
    """Schema Pydantic para resposta do endpoint /health"""

    status: str
    service: str
    version: str
    environment: str
    timestamp: str


class InfoResponseSchema(BaseModel):
    """Schema Pydantic para resposta do endpoint /info"""

    system: dict
    database: dict
    features: dict


# JSON Schema para validação adicional
ping_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["success", "ok"]},
        "message": {"type": "string"},
        "timestamp": {"type": "string"},
        "service": {"type": "string"},
    },
    "required": ["status", "message", "timestamp", "service"],
    "additionalProperties": True,
}

health_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["healthy", "ok"]},
        "service": {"type": "string"},
        "version": {"type": "string"},
        "environment": {"type": "string"},
        "timestamp": {"type": "string"},
    },
    "required": ["status", "service", "version", "environment", "timestamp"],
    "additionalProperties": True,
}


@pytest.mark.asyncio
class TestMainEndpoints:
    """Classe de testes para endpoints principais"""

    async def test_health_endpoint_async(
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

        # Validação JSON Schema
        try:
            validate(instance=data, schema=health_schema)
        except JsonSchemaValidationError as e:
            pytest.fail(f"Validação JSON Schema falhou: {e}")

    def test_health_endpoint_sync(self, client: httpx.Client, test_settings):
        """
        Testa o endpoint /health de forma síncrona

        Args:
            client: Cliente HTTP síncrono
            test_settings: Configurações de teste
        """
        response = client.get("/health", timeout=test_settings["health_timeout"])

        # Validação básica
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Validação de conteúdo
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "environment" in data

        # Validação de valores esperados
        assert data["status"] == "healthy"
        assert data["environment"] == "development"
        assert "SILA" in data["service"]

    def test_ping_endpoint(self, client: httpx.Client, test_settings):
        """
        Testa o endpoint /ping

        Args:
            client: Cliente HTTP síncrono
            test_settings: Configurações de teste
        """
        response = client.get("/ping", timeout=test_settings["ping_timeout"])

        # Validação básica
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Validação de conteúdo
        data = response.json()
        assert isinstance(data, dict)

        # Validação Pydantic
        try:
            ping_response = PingResponseSchema(**data)
            assert ping_response.status in ["success", "ok"]
            assert ping_response.message == "pong"
        except ValidationError as e:
            pytest.fail(f"Validação Pydantic falhou: {e}")

        # Validação JSON Schema
        try:
            validate(instance=data, schema=ping_schema)
        except JsonSchemaValidationError as e:
            pytest.fail(f"Validação JSON Schema falhou: {e}")

    def test_root_endpoint(self, client: httpx.Client):
        """
        Testa o endpoint raiz /

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/")

        # Validação básica
        assert response.status_code == 200

        # Validação de conteúdo (pode variar conforme implementação)
        content = response.text
        assert len(content) > 0, "Endpoint raiz deve retornar conteúdo"

    def test_info_endpoint(self, client: httpx.Client, test_settings):
        """
        Testa o endpoint /info

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

        # Validação Pydantic
        try:
            info_response = InfoResponseSchema(**data)
            assert "system" in info_response.dict()
            assert "database" in info_response.dict()
            assert "features" in info_response.dict()
        except ValidationError as e:
            pytest.fail(f"Validação Pydantic falhou: {e}")

        # Validações específicas dos dados
        assert "system" in data
        assert "database" in data

        # Verificar informações do sistema
        system = data["system"]
        assert system["environment"] == "development"
        assert system["debug"] is True

        # Verificar informações do database
        database = data["database"]
        assert database["host"] == "localhost"
        assert database["database"] == "sila_db"

    def test_docs_endpoint(self, client: httpx.Client):
        """
        Testa o endpoint /docs (Swagger UI)

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/docs")

        # Validação básica
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]

    def test_redoc_endpoint(self, client: httpx.Client):
        """
        Testa o endpoint /redoc (ReDoc)

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/redoc")

        # Validação básica
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]

    def test_openapi_schema(self, client: httpx.Client):
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

    @pytest.mark.parametrize("endpoint", ["/health", "/ping", "/info", "/"])
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

    def test_invalid_endpoint_returns_404(self, client: httpx.Client):
        """
        Testa que endpoints inválidos retornam 404

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.get("/endpoint-inexistente")
        assert response.status_code == 404

    def test_cors_headers(self, client: httpx.Client):
        """
        Testa headers CORS nos endpoints

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.options("/health")

        # Deve ter headers CORS presentes
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers


@pytest.mark.asyncio
class TestErrorHandling:
    """Testes para tratamento de erros"""

    async def test_invalid_method_health(self, async_client: httpx.AsyncClient):
        """
        Testa método inválido no endpoint /health

        Args:
            async_client: Cliente HTTP assíncrono
        """
        response = await async_client.post("/health")
        assert response.status_code == 405  # Method Not Allowed

    def test_invalid_method_ping(self, client: httpx.Client):
        """
        Testa método inválido no endpoint /ping

        Args:
            client: Cliente HTTP síncrono
        """
        response = client.post("/ping")
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
