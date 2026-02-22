"""
Unit tests for Payment API Endpoints
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import status
from httpx import AsyncClient, ASGITransport

from apps.backend.modules.payment.models.enums import (
    PaymentStatus,
    PaymentMethod,
    TransactionType,
)
from apps.backend.modules.payment.schemas.payment import PaymentCreate, PaymentResponse


# ================================================
# FIXTURES ASYNC
# ================================================


@pytest_asyncio.fixture
async def async_client():
    """Async client fixture for API tests."""
    # Import inside fixture to avoid circular imports
    from apps.backend.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
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


@pytest_asyncio.fixture
async def sample_payment_response():
    """Sample payment response data."""
    return {
        "id": 1,
        "amount": 100.0,
        "currency": "AOA",
        "status": PaymentStatus.PENDING.value,
        "method": PaymentMethod.BNA.value,
        "reference": "PAY-123",
        "description": "Test payment",
        "metadata": {"order_id": "123"},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
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
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.create_payment"
    ) as mock_create:
        # Mock the service response
        mock_payment = MagicMock()
        mock_payment.id = 1
        mock_payment.amount = Decimal("100.0")
        mock_payment.currency = "AOA"
        mock_payment.status = PaymentStatus.PENDING
        mock_payment.method = PaymentMethod.BNA
        mock_payment.reference = "PAY-123"
        mock_payment.description = "Test payment"
        mock_payment.metadata = {"order_id": "123"}
        mock_payment.created_at = datetime.now(timezone.utc)
        mock_payment.updated_at = datetime.now(timezone.utc)

        mock_create.return_value = mock_payment

        response = await async_client.post("/payments/", json=mock_payment_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 1
        assert data["amount"] == 100.0
        assert data["status"] == PaymentStatus.PENDING.value
        assert data["reference"] == "PAY-123"


@pytest.mark.asyncio
async def test_create_payment_validation_error(async_client: AsyncClient):
    """Test payment creation with invalid data."""
    invalid_data = {
        "amount": -100.0,  # Invalid negative amount
        "currency": "AOA",
        "method": "INVALID_METHOD",
    }

    response = await async_client.post("/payments/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_payment_missing_required_fields(async_client: AsyncClient):
    """Test payment creation with missing required fields."""
    incomplete_data = {
        "amount": 100.0,
        # Missing currency, method, etc.
    }

    response = await async_client.post("/payments/", json=incomplete_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ================================================
# TESTS ASYNC - PAYMENT RETRIEVAL
# ================================================


@pytest.mark.asyncio
async def test_get_payment_success(async_client: AsyncClient):
    """Test getting a specific payment successfully."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.get_payment"
    ) as mock_get:
        # Mock the service response
        mock_payment = MagicMock()
        mock_payment.id = 1
        mock_payment.amount = Decimal("100.0")
        mock_payment.currency = "AOA"
        mock_payment.status = PaymentStatus.COMPLETED
        mock_payment.method = PaymentMethod.BNA
        mock_payment.reference = "PAY-123"
        mock_payment.description = "Test payment"
        mock_payment.metadata = {"order_id": "123"}
        mock_payment.created_at = datetime.now(timezone.utc)
        mock_payment.updated_at = datetime.now(timezone.utc)

        mock_get.return_value = mock_payment

        response = await async_client.get("/payments/1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["reference"] == "PAY-123"
        assert data["status"] == PaymentStatus.COMPLETED.value


@pytest.mark.asyncio
async def test_get_payment_not_found(async_client: AsyncClient):
    """Test getting a non-existent payment."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.get_payment"
    ) as mock_get:
        mock_get.return_value = None

        response = await async_client.get("/payments/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ================================================
# TESTS ASYNC - PAYMENT LISTING
# ================================================


@pytest.mark.asyncio
async def test_list_payments(async_client: AsyncClient):
    """Test listing payments with results."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.list_payments"
    ) as mock_list:
        # Mock the service response
        mock_payment1 = MagicMock()
        mock_payment1.id = 1
        mock_payment1.amount = Decimal("100.0")
        mock_payment1.currency = "AOA"
        mock_payment1.status = PaymentStatus.COMPLETED
        mock_payment1.method = PaymentMethod.BNA
        mock_payment1.reference = "PAY-123"
        mock_payment1.description = "Test payment 1"
        mock_payment1.metadata = {}
        mock_payment1.created_at = datetime.now(timezone.utc)
        mock_payment1.updated_at = datetime.now(timezone.utc)

        mock_payment2 = MagicMock()
        mock_payment2.id = 2
        mock_payment2.amount = Decimal("200.0")
        mock_payment2.currency = "AOA"
        mock_payment2.status = PaymentStatus.PENDING
        mock_payment2.method = PaymentMethod.MULTICAIXA
        mock_payment2.reference = "PAY-456"
        mock_payment2.description = "Test payment 2"
        mock_payment2.metadata = {}
        mock_payment2.created_at = datetime.now(timezone.utc)
        mock_payment2.updated_at = datetime.now(timezone.utc)

        mock_list.return_value = [mock_payment1, mock_payment2]

        response = await async_client.get("/payments/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2


@pytest.mark.asyncio
async def test_list_payments_empty(async_client: AsyncClient):
    """Test listing payments when no payments exist."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.list_payments"
    ) as mock_list:
        mock_list.return_value = []

        response = await async_client.get("/payments/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []


# ================================================
# TESTS ASYNC - TRANSACTION ENDPOINTS
# ================================================


@pytest.mark.asyncio
async def test_get_transaction_success(async_client: AsyncClient):
    """Test getting a specific transaction successfully."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.get_transaction"
    ) as mock_get:
        # Mock the service response
        mock_transaction = MagicMock()
        mock_transaction.id = 1
        mock_transaction.payment_id = 1
        mock_transaction.amount = Decimal("100.0")
        mock_transaction.currency = "AOA"
        mock_transaction.type = TransactionType.PAYMENT
        mock_transaction.status = PaymentStatus.COMPLETED
        mock_transaction.reference = "TX-123"
        mock_transaction.provider_reference = "PROV-123"
        mock_transaction.metadata = {}
        mock_transaction.created_at = datetime.now(timezone.utc)
        mock_transaction.updated_at = datetime.now(timezone.utc)

        mock_get.return_value = mock_transaction

        response = await async_client.get("/payments/transactions/1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["reference"] == "TX-123"
        assert data["type"] == TransactionType.PAYMENT.value


@pytest.mark.asyncio
async def test_get_transaction_not_found(async_client: AsyncClient):
    """Test getting a non-existent transaction."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.get_transaction"
    ) as mock_get:
        mock_get.return_value = None

        response = await async_client.get("/payments/transactions/999")
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

        with patch(
            "apps.backend.modules.payment.services.payment_service.PaymentService.create_payment"
        ) as mock_create:
            mock_payment = MagicMock()
            mock_payment.id = 1
            mock_payment.amount = Decimal("100.0")
            mock_payment.currency = "AOA"
            mock_payment.status = PaymentStatus.PENDING
            mock_payment.method = PaymentMethod(method)
            mock_payment.reference = f"PAY-{method}"
            mock_payment.description = f"Test payment with {method}"
            mock_payment.metadata = {}
            mock_payment.created_at = datetime.now(timezone.utc)
            mock_payment.updated_at = datetime.now(timezone.utc)

            mock_create.return_value = mock_payment

            response = await async_client.post("/payments/", json=payment_data)
            assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_payment_with_query_params(async_client: AsyncClient):
    """Test listing payments with query parameters."""
    with patch(
        "apps.backend.modules.payment.services.payment_service.PaymentService.list_payments"
    ) as mock_list:
        mock_list.return_value = []

        # Test with status filter
        response = await async_client.get("/payments/?status=completed")
        assert response.status_code == status.HTTP_200_OK

        # Test with method filter
        response = await async_client.get("/payments/?method=bna")
        assert response.status_code == status.HTTP_200_OK

        # Test with multiple filters
        response = await async_client.get("/payments/?status=pending&method=multicaixa")
        assert response.status_code == status.HTTP_200_OK


# ================================================
# TESTS ASYNC - ROUTE EXISTENCE
# ================================================


@pytest.mark.asyncio
async def test_payment_routes_exist(async_client: AsyncClient):
    """Test that all payment routes exist and return proper status codes."""
    # Test GET routes
    routes_to_test = [
        "/payments/ping",
        "/payments/status",
        "/payments/",
    ]

    for route in routes_to_test:
        response = await async_client.get(route)
        # These should not return 404 Not Found
        assert response.status_code != status.HTTP_404_NOT_FOUND

    # Test POST route
    response = await async_client.post("/payments/", json={})
    # Should be 422 (validation error) not 404
    assert response.status_code != status.HTTP_404_NOT_FOUND
