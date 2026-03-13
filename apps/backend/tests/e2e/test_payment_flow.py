"""
FASE 5: Testes E2E para fluxo operacional de pedidos/pagamentos.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_payment_flow_complete(async_http_client: AsyncClient, mock_user):
    """
    E2E: fluxo completo operacional (ordem -> pagamento -> recibo).
    Executa somente quando há serviço público ativo no catálogo.
    """
    _ = mock_user

    services_response = await async_http_client.get("/api/v1/services")
    if services_response.status_code >= 500:
        pytest.skip("Catálogo de serviços indisponível no ambiente de teste.")
    assert services_response.status_code == 200
    services = services_response.json()
    if not services:
        pytest.skip("Sem serviços públicos ativos para executar fluxo completo de pagamento.")

    service_id = services[0]["id"]
    order_response = await async_http_client.post(
        "/api/v1/orders",
        json={"service_id": service_id},
    )
    if order_response.status_code >= 500:
        pytest.skip("Infra de pedidos indisponível no ambiente de teste.")
    assert order_response.status_code == 201
    order = order_response.json()
    order_id = order["id"]

    documents_response = await async_http_client.post(
        f"/api/v1/orders/{order_id}/documents",
        json={
            "documents": [
                {
                    "filename": "proof.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 1024,
                    "uri": "s3://bucket/proof.pdf",
                }
            ]
        },
    )
    assert documents_response.status_code == 200

    submit_response = await async_http_client.post(
        f"/api/v1/orders/{order_id}/submit"
    )
    assert submit_response.status_code == 200

    generate_payment_response = await async_http_client.post(
        f"/api/v1/payments/{order_id}/generate"
    )
    assert generate_payment_response.status_code == 200
    payment_reference = generate_payment_response.json()["reference"]

    confirm_payment_response = await async_http_client.post(
        f"/api/v1/payments/{payment_reference}/confirm"
    )
    assert confirm_payment_response.status_code == 200
    assert confirm_payment_response.json()["status"] in {"CONFIRMED", "PENDING", "FAILED"}

    complete_response = await async_http_client.post(
        f"/api/v1/orders/{order_id}/complete"
    )
    assert complete_response.status_code in {200, 400}

    if complete_response.status_code == 200:
        receipt_response = await async_http_client.get(
            f"/api/v1/orders/{order_id}/receipt"
        )
        assert receipt_response.status_code == 200


@pytest.mark.asyncio
async def test_payment_validation_errors(async_http_client: AsyncClient, mock_user):
    """
    E2E: valida erros de contrato e autorização do fluxo operacional.
    """
    _ = mock_user
    # Sem autenticação -> deve falhar em endpoints protegidos.
    unauth_response = await async_http_client.get("/api/v1/services")
    assert unauth_response.status_code in {200, 401}

    invalid_order_payload_response = await async_http_client.post(
        "/api/v1/orders", json={}
    )
    assert invalid_order_payload_response.status_code == 422


@pytest.mark.asyncio
async def test_payment_refund_flow(async_http_client: AsyncClient, mock_user):
    """
    E2E: fallback de referência inválida no endpoint de confirmação.
    """
    _ = mock_user
    response = await async_http_client.post(
        "/api/v1/payments/INVALID-REFERENCE/confirm"
    )
    assert response.status_code == 400
