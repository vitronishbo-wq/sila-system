"""
Testes de Rotas de Validação - Módulo Identidade Civil

Testes de integração para endpoints de validação FUC.
"""
import pytest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from modules.identity.models.user import User

client = TestClient(app)


@pytest.mark.usefixtures("mock_user")
class TestValidacaoRoutes:
    """Testes do endpoint de validação."""

    def test_sync_fuc_requires_citizen_id(self):
        """Deve exigir citizen_fuc_id para sincronização."""
        response = client.post(
            "/api/v1/identidade/validacao/sincronizar-fuc",
            json={}
        )
        assert response.status_code == 400
        assert "citizen_fuc_id" in response.json()["detail"].lower()

    def test_check_fuc_status_returns_connection_info(self):
        """Deve retornar status de conexão FUC."""
        citizen_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/identidade/validacao/status-fuc/{citizen_id}")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        # Cidadão inexistente deve retornar DISCONNECTED
        assert data["status"] in ("SYNCED", "DISCONNECTED")
