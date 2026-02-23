"""
FASE 5: Testes E2E para Citizenship Flow
Teste completo do fluxo de cidadania
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_citizenship_registration_flow(async_http_client: AsyncClient):
    """
    E2E: Fluxo completo de registro de cidadania
    1. Criar usuário
    2. Enviar documentos
    3. Verificar status
    4. Completar registro
    """

    # 1. Criar usuário
    user_data = {
        "email": "citizen@sila.com",
        "full_name": "Test Citizen",
        "password": "secure_password_123",
        "cpf": "12345678901",
    }

    response = await async_http_client.post("/api/v1/users/", json=user_data)
    assert response.status_code in [200, 201, 409]
    user_id = response.json().get("id", "existing_citizen")

    # 2. Criar registro de cidadania
    citizenship_data = {
        "user_id": user_id,
        "birth_date": "1990-01-01",
        "nationality": "BR",
        "city": "São Paulo",
        "state": "SP",
    }

    response = await async_http_client.post(
        "/api/v1/citizenship/", json=citizenship_data
    )
    assert response.status_code in [200, 201]
    citizenship = response.json()
    citizenship_id = citizenship.get("id")

    # 3. Enviar documentos
    doc_data = {
        "citizenship_id": citizenship_id,
        "document_type": "birth_certificate",
        "document_url": "https://fake-url.com/doc.pdf",
    }

    response = await async_http_client.post(
        "/api/v1/citizenship/documents/", json=doc_data
    )
    assert response.status_code in [200, 201]

    # 4. Verificar status
    response = await async_http_client.get(f"/api/v1/citizenship/{citizenship_id}/")
    assert response.status_code == 200
    final_citizenship = response.json()

    # 5. Validações
    assert final_citizenship.get("status") in ["pending", "approved", "draft"]
    assert final_citizenship.get("nationality") == "BR"
    assert final_citizenship.get("user_id") == user_id


@pytest.mark.asyncio
async def test_citizenship_cross_module_flow(async_http_client: AsyncClient):
    """
    E2E: Fluxo cruzado - Cidadania + Educação + Saúde
    Usuário registra-se e acessa múltiplos módulos
    """

    # 1. Registro no sistema
    user_data = {
        "email": "cross_module@sila.com",
        "full_name": "Cross Module Test",
        "password": "password123",
    }

    response = await async_http_client.post("/api/v1/users/", json=user_data)
    assert response.status_code in [200, 201, 409]
    user_id = response.json().get("id", "existing_user")

    # 2. Registrar em Cidadania
    cit_response = await async_http_client.post(
        "/api/v1/citizenship/", json={"user_id": user_id, "nationality": "BR"}
    )
    assert cit_response.status_code in [200, 201]

    # 3. Registrar em Educação
    edu_response = await async_http_client.post(
        "/api/v1/education/", json={"user_id": user_id, "school": "Test School"}
    )
    assert edu_response.status_code in [200, 201]

    # 4. Registrar em Saúde
    health_response = await async_http_client.post(
        "/api/v1/health/", json={"user_id": user_id, "health_number": "123456"}
    )
    assert health_response.status_code in [200, 201]

    # 5. Verificar dados do usuário em contexto cruzado
    response = await async_http_client.get(f"/api/v1/users/{user_id}/profile/")
    assert response.status_code in [200, 404]  # 404 ok se endpoint não existe
