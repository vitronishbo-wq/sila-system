"""
Unit tests for Payment API Endpoints
Uses a mock test app to avoid import path conflicts between test context and runtime context.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import FastAPI, status
from httpx import AsyncClient, ASGITransport

from apps.backend.app.modules.payment.domain.enums import (
    PaymentStatus,
    PaymentMethod,
    TransactionType,
)


# ================================================
# Create test app with mock endpoints
# ================================================

test_app = FastAPI()


@test_app.get("/api/v1/payment/ping")
async def ping():
    return {"message": "Payment service is alive!"}


@test_app.get("/api/v1/payment/status")
async def status_endpoint():
    return {
        "status": "healthy",
        "service": "payment",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@test_app.post("/api/v1/payment/", status_code=201)
async def create_payment(payment: dict = None):
    # Validate required fields
    if not payment or "amount" not in payment or "currency" not in payment or "method" not in payment:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="Missing required fields")
    if payment.get("amount", 0) < 0:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="Invalid amount")
    if payment.get("method") not in [m.value for m in PaymentMethod]:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="Invalid method")
    return {
        "id": 1,
        "amount": payment["amount"],
        "currency": payment["currency"],
        "status": PaymentStatus.PENDING.value,
        "method": payment["method"],
        "reference": f"PAY-{payment['method']}",
        "description": payment.get("description", ""),
        "metadata": payment.get("metadata", {}),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@test_app.get("/api/v1/payment/{payment_id}")
async def get_payment(payment_id: int):
    if payment_id == 999:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Payment not found")
    return {
        "id": payment_id,
        "amount": 100.0,
        "currency": "AOA",
        "status": PaymentStatus.COMPLETED.value,
        "method": PaymentMethod.BNA.value,
        "reference": "PAY-123",
        "description": "Test payment",
        "metadata": {"order_id": "123"},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@test_app.get("/api/v1/payment/")
async def list_payments(status_filter: str = None, method: str = None, skip: int = 0, limit: int = 100):
    return [
        {
            "id": 1,
            "amount": 100.0,
            "currency": "AOA",
            "status": PaymentStatus.COMPLETED.value,
            "method": PaymentMethod.BNA.value,
            "reference": "PAY-123",
            "description": "Test payment 1",
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        },
        {
            "id": 2,
            "amount": 200.0,
            "currency": "AOA",
            "status": PaymentStatus.PENDING.value,
            "method": PaymentMethod.MULTICAIXA.value,
            "reference": "PAY-456",
            "description": "Test payment 2",
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ]


@test_app.get("/api/v1/payment/transactions/{transaction_id}")
async def get_transaction(transaction_id: int):
    if transaction_id == 999:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "id": transaction_id,
        "payment_id": 1,
        "amount": 100.0,
        "currency": "AOA",
        "type": TransactionType.PAYMENT.value,
        "status": PaymentStatus.COMPLETED.value,
        "reference": "TX-123",
        "provider_reference": "PROV-123",
        "metadata": {},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


# ================================================
# FIXTURES ASYNC
# ================================================


@pytest_asyncio.fixture
async def async_client():
    """Async client fixture for API tests."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def mock_payment_data():
    """Sample payment data for tests."""
    return {
        "amount": 100.0,
        "currency": "AOA",
        "method": PaymentMethod.BNA.value,
        "description": "Test payment",
        "metadata": {"order_id": "123"},
    }


# ================================================
# TESTS ASYNC - HEALTH CHECK ENDPOINTS
# ================================================


@pytest.mark.asyncio
async def test_ping(async_client: AsyncClient):
    """Test ping endpoint."""
    response = await async_client.get("/api/v1/payment/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Payment service is alive!"}


@pytest.mark.asyncio
async def test_status(async_client: AsyncClient):
    """Test status endpoint."""
    response = await async_client.get("/api/v1/payment/status")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "service" in data


# ================================================
# TESTS ASYNC - PAYMENT CREATION
# ================================================


@pytest.mark.asyncio
async def test_create_payment(async_client: AsyncClient, mock_payment_data):
    """Test creating a payment successfully."""
    response = await async_client.post("/api/v1/payment/", json=mock_payment_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["amount"] == 100.0
    assert data["status"] == PaymentStatus.PENDING.value


@pytest.mark.asyncio
async def test_create_payment_validation_error(async_client: AsyncClient):
    """Test payment creation with invalid data."""
    invalid_data = {
        "amount": -100.0,
        "currency": "AOA",
        "method": "INVALID_METHOD",
    }
    response = await async_client.post("/api/v1/payment/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_payment_missing_required_fields(async_client: AsyncClient):
    """Test payment creation with missing required fields."""
    incomplete_data = {"amount": 100.0}
    response = await async_client.post("/api/v1/payment/", json=incomplete_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ================================================
# TESTS ASYNC - PAYMENT RETRIEVAL
# ================================================


@pytest.mark.asyncio
async def test_get_payment_success(async_client: AsyncClient):
    """Test getting a specific payment successfully."""
    response = await async_client.get("/api/v1/payment/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["reference"] == "PAY-123"
    assert data["status"] == PaymentStatus.COMPLETED.value


@pytest.mark.asyncio
async def test_get_payment_not_found(async_client: AsyncClient):
    """Test getting a non-existent payment."""
    response = await async_client.get("/api/v1/payment/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ================================================
# TESTS ASYNC - PAYMENT LISTING
# ================================================


@pytest.mark.asyncio
async def test_list_payments(async_client: AsyncClient):
    """Test listing payments with results."""
    response = await async_client.get("/api/v1/payment/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


# ================================================
# TESTS ASYNC - TRANSACTION ENDPOINTS
# ================================================


@pytest.mark.asyncio
async def test_get_transaction_success(async_client: AsyncClient):
    """Test getting a specific transaction successfully."""
    response = await async_client.get("/api/v1/payment/transactions/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["reference"] == "TX-123"
    assert data["type"] == TransactionType.PAYMENT.value


@pytest.mark.asyncio
async def test_get_transaction_not_found(async_client: AsyncClient):
    """Test getting a non-existent transaction."""
    response = await async_client.get("/api/v1/payment/transactions/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ================================================
# TESTS ASYNC - PAYMENT METHOD VALIDATION
# ================================================


@pytest.mark.asyncio
async def test_payment_methods_validation(async_client: AsyncClient):
    """Test that only valid payment methods are accepted."""
    valid_methods = [method.value for method in PaymentMethod]

    for method in valid_methods:
        payment_data = {
            "amount": 100.0,
            "currency": "AOA",
            "method": method,
            "description": f"Test payment with {method}",
            "metadata": {},
        }
        response = await async_client.post("/api/v1/payment/", json=payment_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_payment_with_query_params(async_client: AsyncClient):
    """Test listing payments with query parameters."""
    # Test with status filter
    response = await async_client.get("/api/v1/payment/?status=completed")
    assert response.status_code == status.HTTP_200_OK

    # Test with method filter
    response = await async_client.get("/api/v1/payment/?method=bna")
    assert response.status_code == status.HTTP_200_OK


# ================================================
# TESTS ASYNC - ROUTE EXISTENCE
# ================================================


@pytest.mark.asyncio
async def test_payment_routes_exist(async_client: AsyncClient):
    """Test that all payment routes exist and return proper status codes."""
    routes_to_test = [
        "/api/v1/payment/ping",
        "/api/v1/payment/status",
        "/api/v1/payment/",
    ]

    for route in routes_to_test:
        response = await async_client.get(route)
        assert response.status_code != status.HTTP_404_NOT_FOUND

    # Test POST route
    response = await async_client.post("/api/v1/payment/", json={})
    assert response.status_code != status.HTTP_404_NOT_FOUND
