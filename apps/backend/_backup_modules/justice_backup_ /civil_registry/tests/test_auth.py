from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

class TestPublicEndpoints:
    """Testes de endpoints públicos (sem autenticação)."""

    def test_get_event_types_is_public(self):
        """Catálogo de tipos de evento deve ser público."""
        response = client.get('/api/v1/identidade/bi/tipos-evento')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_history_types_catalog_is_public(self):
        """Catálogo de tipos para histórico deve ser público."""
        response = client.get('/api/v1/identidade/historico/tipos/catalogo')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)