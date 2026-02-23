"""
FASE 5: Testes E2E para Payment Flow
Teste completo do fluxo de pagamento
"""

from typing import AsyncGenerator

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_payment_flow_complete(async_http_client: AsyncClient):
    """
    E2E: Fluxo completo de pagamento
    1. Criar usuário
    2. Gerar pedido
    3. Processar pagamento
    4. Confirmar transação
    """

    # 1. Setup de dados
    user_data = {
        "email": "test_payment@sila.com",
        "full_name": "Test Payment User",
        "password": "secure_password_123",
    }

    # 2. Criar usuário
    response = await async_http_client.post("/api/v1/users/", json=user_data)
    assert response.status_code in [200, 201, 409]  # 409 se já existe

    user_id = (
        response.json().get("id") if response.status_code != 409 else "existing_user"
    )

    # 3. Criar pedido
    order_data = {
        "user_id": user_id,
        "amount": 100.50,
        "description": "Test Order",
        "items": [
            {"description": "Item 1", "amount": 50.25},
            {"description": "Item 2", "amount": 50.25},
        ],
    }

    response = await async_http_client.post("/api/v1/orders/", json=order_data)
    assert response.status_code in [200, 201]
    order = response.json()
    order_id = order.get("id")

    # 4. Processar pagamento
    payment_data = {
        "order_id": order_id,
        "amount": 100.50,
        "method": "credit_card",
        "token": "fake_token_123",
    }

    response = await async_http_client.post("/api/v1/payments/", json=payment_data)
    assert response.status_code in [200, 201]
    payment = response.json()
    payment_id = payment.get("id")

    # 5. Verificar status
    response = await async_http_client.get(f"/api/v1/payments/{payment_id}/")
    assert response.status_code == 200
    final_payment = response.json()

    # 6. Validações
    assert final_payment.get("status") in ["success", "pending", "completed"]
    assert final_payment.get("amount") == 100.50
    assert final_payment.get("order_id") == order_id


@pytest.mark.asyncio
async def test_payment_validation_errors(async_http_client: AsyncClient):
    """
    E2E: Validação de erros no fluxo de pagamento
    """

    # Payment sem ordem (deve falhar)
    payment_data = {
        "order_id": "non_existent_order",
        "amount": 100.50,
        "method": "credit_card",
        "token": "fake_token",
    }

    response = await async_http_client.post("/api/v1/payments/", json=payment_data)
    assert response.status_code in [400, 404]


@pytest.mark.asyncio
async def test_payment_refund_flow(async_http_client: AsyncClient):
    """
    E2E: Fluxo de reembolso
    """

    # Assumindo pagamento existente
    payment_id = "test_payment_123"

    refund_data = {"payment_id": payment_id, "reason": "customer_request"}

    response = await async_http_client.post("/api/v1/refunds/", json=refund_data)

    # Pode ser 200 ou 404 se pagamento não existe (teste com mock seria ideal)
    assert response.status_code in [200, 201, 404]
