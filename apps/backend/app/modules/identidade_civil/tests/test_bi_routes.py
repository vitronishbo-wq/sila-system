"""
Testes de Rotas de BI - Módulo Identidade Civil

Testes de integração para endpoints de ciclo de vida do BI.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from app.core.iam.models.user import User

client = TestClient(app)


@pytest.mark.usefixtures("mock_user")
class TestBIRoutes:
    """Testes do endpoint de BI."""

    def test_get_supported_events_returns_list(self):
        """Deve retornar lista de tipos de evento suportados."""
        response = client.get("/api/v1/identidade/bi/tipos-evento")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    def test_emit_bi_requires_citizen_fuc_id(self):
        """Deve exigir citizen_fuc_id para emissão."""
        response = client.post(
            "/api/v1/identidade/bi/emit",
            json={}
        )
        assert response.status_code == 400
        assert "citizen_fuc_id" in response.json()["detail"].lower()

    def test_emit_bi_with_invalid_citizen_returns_error(self):
        """Deve retornar erro para cidadão inexistente."""
        response = client.post(
            "/api/v1/identidade/bi/emit",
            json={"citizen_fuc_id": "INEXISTENT-FUC-ID-12345"}
        )
        # Pode ser 400 (business rule) ou 404 (not found)
        assert response.status_code in (400, 404)

    def test_cancel_bi_requires_reason(self):
        """Deve exigir motivo para cancelamento."""
        response = client.post(
            "/api/v1/identidade/bi/cancel/001234567LA001",
            json={}
        )
        assert response.status_code == 400
        assert "motivo" in response.json()["detail"].lower()


@pytest.mark.usefixtures("mock_user")
class TestRenewalRoute:
    """Testes do endpoint de renovação."""

    def test_renew_bi_with_invalid_citizen(self):
        """Deve retornar erro para cidadão inexistente."""
        response = client.post(
            "/api/v1/identidade/bi/renew/001234567LA001",
            json={"citizen_fuc_id": "INVALID-ID"}
        )
        assert response.status_code == 404
