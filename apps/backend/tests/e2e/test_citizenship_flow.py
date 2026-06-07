"""
FASE 5: Testes E2E para Citizenship Flow
Teste completo do fluxo de cidadania
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_citizenship_registration_flow(async_http_client: AsyncClient, mock_user):
    """
    E2E: fluxo de onboarding e validação de cidadania (rotas atuais)
    """
    _ = mock_user
    response = await async_http_client.get("/api/auth/me")
    assert response.status_code == 200
    profile = response.json()
    assert profile.get("email") == "test@example.com"

    # Endpoint de cidadania/identidade pública e estável
    response = await async_http_client.get("/api/v1/identidade/bi/tipos-evento")
    assert response.status_code == 200
    event_types = response.json()
    assert isinstance(event_types, list)
    assert len(event_types) > 0

    # Sanidade sistêmica
    response = await async_http_client.get("/api/health/live")
    assert response.status_code == 200
    assert response.json().get("alive") is True


@pytest.mark.asyncio
async def test_citizenship_cross_module_flow(async_http_client: AsyncClient, mock_user):
    """
    E2E: valida integração mínima entre auth, identidade e observabilidade.
    """
    _ = mock_user

    identity_response = await async_http_client.get("/api/v1/identidade/bi/tipos-evento")
    assert identity_response.status_code == 200

    me_response = await async_http_client.get("/api/auth/me")
    assert me_response.status_code == 200

    health_response = await async_http_client.get("/api/health")
    assert health_response.status_code == 200
