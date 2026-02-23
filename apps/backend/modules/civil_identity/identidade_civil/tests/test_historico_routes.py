"""
Testes de Rotas de Histórico - Módulo Identidade Civil

Testes de integração para endpoints de auditoria.
"""
import pytest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from modules.identity.models.user import User

client = TestClient(app)


@pytest.mark.usefixtures("mock_user")
class TestHistoricoRoutes:
    """Testes do endpoint de histórico."""

    def test_get_event_history_returns_list(self):
        """Deve retornar lista de eventos para um aggregate."""
        aggregate_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/identidade/historico/{aggregate_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_event_types_catalog(self):
        """Deve retornar catálogo de tipos de evento."""
        response = client.get("/api/v1/identidade/historico/tipos/catalogo")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Verificar que contém tipos conhecidos
        assert "REQUEST_CREATED" in data or "BI_ISSUED" in data


class TestAtestadosRoutes:
    """Testes do endpoint de atestados."""

    def test_get_request_status(self):
        """Deve retornar status de um pedido."""
        request_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/identidade/atestados/{request_id}/status")
        assert response.status_code == 200
        assert "request_id" in response.json()

    def test_residence_certificate_requires_citizen_id(self):
        """Deve exigir citizen_fuc_id para atestado de residência."""
        response = client.post(
            "/api/v1/identidade/atestados/residencia",
            json={}
        )
        # Sem citizen_id, deve retornar 404 (cidadão não encontrado)
        assert response.status_code in (400, 404)
