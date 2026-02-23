"""
Testes de Autenticação e Autorização - Módulo Identidade Civil

⚠️ CONSOLIDADO: Todos os testes de autenticação foram movidos para:
   tests/test_auth_consolidated.py

Este arquivo agora serve apenas como referência histórica.
Veja test_all_endpoints_require_authentication() para validação unificada.

ECONOMIA: -60 linhas duplicadas, -6 testes redundantes
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# NOTA: Todos os testes _requires_auth foram consolidados.
# Adicione novos testes de autenticação em: tests/test_auth_consolidated.py



class TestPublicEndpoints:
    """Testes de endpoints públicos (sem autenticação)."""

    def test_get_event_types_is_public(self):
        """Catálogo de tipos de evento deve ser público."""
        response = client.get("/api/v1/identidade/bi/tipos-evento")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_history_types_catalog_is_public(self):
        """Catálogo de tipos para histórico deve ser público."""
        response = client.get("/api/v1/identidade/historico/tipos/catalogo")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
