"""
Unit tests for Payment Service

These tests focus on business logic validation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from decimal import Decimal

from modules.payment.services.payment_service import PaymentService
from modules.payment.models.enums import (
    PaymentStatus,
    TransactionStatus,
    PaymentMethod,
    TransactionType,
)
from modules.payment.schemas.payment import (
    PaymentCreate,
    RefundCreate,
    RefundResponse,
)


# ================================================
# MOCK MODELS
# ================================================


class MockPayment:
    """Mock Payment ORM model."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", 1)
        self.amount = kwargs.get("amount", Decimal("100.00"))
        self.currency = kwargs.get("currency", "AOA")
        self.status = kwargs.get("status", PaymentStatus.PENDING)
        self.method = kwargs.get("method", PaymentMethod.BNA)
        self.reference = kwargs.get("reference", f"PAY-{self.id}")
        self.description = kwargs.get("description", "Test payment")
        self.metadata_ = kwargs.get("metadata_", {})
        self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
        self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))


class MockTransaction:
    """Mock Transaction ORM model."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", 1)
        self.payment_id = kwargs.get("payment_id", 1)
        self.amount = kwargs.get("amount", Decimal("100.00"))
        self.currency = kwargs.get("currency", "AOA")
        self.type = kwargs.get("type", TransactionType.PAYMENT)
        self.status = kwargs.get("status", TransactionStatus.PENDING)
        self.reference = kwargs.get("reference", f"TXN-{self.id}")
        self.provider_reference = kwargs.get("provider_reference", None)
        self.metadata_ = kwargs.get("metadata_", {})
        self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))


# ================================================
# FIXTURES
# ================================================


@pytest.fixture
def mock_db_session():
    """Mock async database session."""
    session = AsyncMock()

    # Mock result for session.execute().scalars().first()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    session.execute = AsyncMock(return_value=mock_result)

    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()

    async def mock_refresh(obj):
        """Populate basic fields on mock objects if missing."""
        if hasattr(obj, "id") and (obj.id is None or isinstance(obj.id, MagicMock)):
            obj.id = 1
        if hasattr(obj, "created_at") and (
            obj.created_at is None or isinstance(obj.created_at, MagicMock)
        ):
            obj.created_at = datetime.now(timezone.utc)
        if hasattr(obj, "updated_at") and (
            obj.updated_at is None or isinstance(obj.updated_at, MagicMock)
        ):
            obj.updated_at = datetime.now(timezone.utc)

    session.refresh = AsyncMock(side_effect=mock_refresh)
    session.add = MagicMock()
    session.flush = AsyncMock()

    # Expose scalars for easy mocking in tests
    session._mock_result = mock_result
    session._mock_scalars = mock_scalars

    return session


@pytest.fixture
def payment_service(mock_db_session):
    """PaymentService instance with mocked DB."""
    return PaymentService(db=mock_db_session)


# ================================================
# TESTS
# ================================================


def test_service_initialization():
    """Test that PaymentService initializes correctly."""
    db_mock = MagicMock()
    service = PaymentService(db=db_mock)
    assert service.db is db_mock


def test_service_has_required_methods():
    """Test that PaymentService has all required methods."""
    required_methods = [
        "create_payment",
        "get_payment",
        "update_payment_status",
        "create_refund",
        "delete_payment",
        "_is_valid_status_transition",
    ]

    for method_name in required_methods:
        assert hasattr(PaymentService, method_name), f"Missing method: {method_name}"


def test_valid_status_transitions(payment_service: PaymentService):
    """Test status transition validation logic."""
    # Valid transitions
    assert payment_service._is_valid_status_transition(
        PaymentStatus.PENDING, PaymentStatus.PROCESSING
    )
    assert payment_service._is_valid_status_transition(
        PaymentStatus.PROCESSING, PaymentStatus.COMPLETED
    )
    assert payment_service._is_valid_status_transition(
        PaymentStatus.COMPLETED, PaymentStatus.REFUNDED
    )
    assert payment_service._is_valid_status_transition(
        PaymentStatus.PENDING, PaymentStatus.CANCELLED
    )
    assert payment_service._is_valid_status_transition(
        PaymentStatus.PROCESSING, PaymentStatus.CANCELLED
    )

    # Invalid transitions
    assert not payment_service._is_valid_status_transition(
        PaymentStatus.COMPLETED, PaymentStatus.PENDING
    )
    assert not payment_service._is_valid_status_transition(
        PaymentStatus.CANCELLED, PaymentStatus.COMPLETED
    )
    assert not payment_service._is_valid_status_transition(
        PaymentStatus.REFUNDED, PaymentStatus.PROCESSING
    )


@pytest.mark.asyncio
async def test_create_payment_success(payment_service: PaymentService, mock_db_session):
    """Test creating a payment successfully."""
    payment_data = PaymentCreate(
        amount=Decimal("100.50"),
        currency="AOA",
        method=PaymentMethod.BNA,
        description="Test payment",
        metadata={"order_id": "123"},
    )

    # Mock the reference generation
    payment_service._generate_reference = AsyncMock(return_value="PAY-TEST-123")

    with (
        patch("modules.payment.services.payment_service.Payment", MockPayment),
        patch("modules.payment.services.payment_service.PaymentTransaction", MockTransaction),
    ):
        result = await payment_service.create_payment(payment_data, user_id=1)

    assert result is not None
    assert result.amount == float(Decimal("100.50"))
    assert result.currency == "AOA"
    assert result.method == PaymentMethod.BNA
    assert result.status == PaymentStatus.PENDING
    assert result.reference == "PAY-TEST-123"
    assert mock_db_session.add.call_count == 2  # Payment and Transaction
    mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_payment_success(payment_service: PaymentService, mock_db_session):
    """Test getting a payment by ID."""
    mock_payment = MockPayment(
        id=1,
        amount=Decimal("100.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.BNA,
        reference="PAY-123",
        description="Test payment",
        metadata_={"order_id": "123"},
    )

    mock_db_session._mock_scalars.first.return_value = mock_payment

    result = await payment_service.get_payment(1)

    assert result is mock_payment
    mock_db_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_payment_not_found(payment_service: PaymentService, mock_db_session):
    """Test getting a non-existent payment."""
    mock_db_session._mock_scalars.first.return_value = None

    result = await payment_service.get_payment(999)

    assert result is None


@pytest.mark.asyncio
async def test_update_payment_status_valid_transition(
    payment_service: PaymentService, mock_db_session
):
    """Test updating payment to a valid status."""
    mock_payment = MockPayment(
        id=1,
        status=PaymentStatus.PROCESSING,
        amount=Decimal("100.0"),
    )

    mock_db_session._mock_scalars.first.return_value = mock_payment

    # Mock latest transaction
    mock_transaction = MockTransaction(payment_id=1)
    payment_service._get_latest_transaction = AsyncMock(return_value=mock_transaction)

    result = await payment_service.update_payment_status(
        payment_id=1, status=PaymentStatus.COMPLETED, provider_reference="PROV-XYZ"
    )

    assert result is not None
    assert mock_payment.status == PaymentStatus.COMPLETED
    assert mock_transaction.status == TransactionStatus.COMPLETED
    mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_payment_status_invalid_transition(
    payment_service: PaymentService, mock_db_session
):
    """Test that invalid status transition raises ValueError."""
    mock_payment = MockPayment(id=1, status=PaymentStatus.CANCELLED)

    mock_db_session._mock_scalars.first.return_value = mock_payment

    with pytest.raises(ValueError, match="Invalid status transition"):
        await payment_service.update_payment_status(
            payment_id=1, status=PaymentStatus.COMPLETED
        )


@pytest.mark.asyncio
async def test_update_payment_status_payment_not_found(
    payment_service: PaymentService, mock_db_session
):
    """Test updating status of non-existent payment."""
    mock_db_session._mock_scalars.first.return_value = None

    result = await payment_service.update_payment_status(
        payment_id=999, status=PaymentStatus.COMPLETED
    )

    assert result is None


@pytest.mark.asyncio
async def test_create_refund_full_refund(
    payment_service: PaymentService, mock_db_session
):
    """Test creating a full refund."""
    payment_amount = Decimal("200.00")
    now = datetime.now(timezone.utc)

    mock_payment = MockPayment(
        id=1,
        status=PaymentStatus.COMPLETED,
        amount=payment_amount,
        created_at=now,
        updated_at=now
    )

    mock_db_session._mock_scalars.first.return_value = mock_payment
    payment_service._generate_reference = AsyncMock(return_value="RFD-ABC123")

    # Mock transaction creation
    mock_transaction = MockTransaction(
        id=2,
        reference="RFD-ABC123",
        amount=payment_amount,
        type=TransactionType.REFUND,
        created_at=now
    )

    with patch(
        "modules.payment.services.payment_service.PaymentTransaction",
        return_value=mock_transaction,
    ):
        refund_data = RefundCreate(reason="Test refund")

        refund_response = await payment_service.create_refund(
            payment_id=1, refund_data=refund_data, user_id=10
        )

        assert mock_payment.status == PaymentStatus.REFUNDED
        assert isinstance(refund_response, RefundResponse)
        assert refund_response.amount == float(payment_amount)
        assert refund_response.status == TransactionStatus.PENDING
        assert refund_response.reference == "RFD-ABC123"
        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()


@pytest.mark.asyncio
async def test_create_refund_partial_refund(
    payment_service: PaymentService, mock_db_session
):
    """Test creating a partial refund."""
    payment_amount = Decimal("200.00")
    refund_amount = Decimal("50.00")
    now = datetime.now(timezone.utc)

    mock_payment = MockPayment(
        id=1,
        status=PaymentStatus.COMPLETED,
        amount=payment_amount,
        created_at=now,
        updated_at=now
    )

    mock_db_session._mock_scalars.first.return_value = mock_payment
    payment_service._generate_reference = AsyncMock(return_value="RFD-PARTIAL-123")

    mock_transaction = MockTransaction(
        id=2,
        reference="RFD-PARTIAL-123",
        amount=refund_amount,
        type=TransactionType.REFUND,
        created_at=now
    )

    with patch(
        "modules.payment.services.payment_service.PaymentTransaction",
        return_value=mock_transaction,
    ):
        refund_data = RefundCreate(amount=float(refund_amount), reason="Partial refund")

        refund_response = await payment_service.create_refund(
            payment_id=1, refund_data=refund_data, user_id=10
        )

        assert (
            mock_payment.status == PaymentStatus.PARTIALLY_REFUNDED
        )  # Status should be partially_refunded
        assert isinstance(refund_response, RefundResponse)
        assert refund_response.amount == float(refund_amount)
        assert refund_response.status == TransactionStatus.PENDING


@pytest.mark.asyncio
async def test_create_refund_exceeds_amount(
    payment_service: PaymentService, mock_db_session
):
    """Test that refund amount exceeding payment amount raises error."""
    payment_amount = Decimal("100.00")

    mock_payment = MockPayment(
        id=1,
        status=PaymentStatus.COMPLETED,
        amount=payment_amount,
    )

    mock_db_session._mock_scalars.first.return_value = mock_payment

    refund_data = RefundCreate(amount=100.01, reason="Test")

    with pytest.raises(ValueError, match=".*exceed.*payment.*amount.*"):
        await payment_service.create_refund(
            payment_id=1, refund_data=refund_data, user_id=10
        )


@pytest.mark.asyncio
async def test_create_refund_invalid_payment_status(
    payment_service: PaymentService, mock_db_session
):
    """Test that refund cannot be created for non-completed payment."""
    mock_payment = MockPayment(id=1, status=PaymentStatus.PENDING)

    mock_db_session._mock_scalars.first.return_value = mock_payment

    refund_data = RefundCreate(amount=50.00, reason="Test")

    with pytest.raises(ValueError, match=".*only refund completed payments.*"):
        await payment_service.create_refund(
            payment_id=1, refund_data=refund_data, user_id=10
        )


@pytest.mark.asyncio
async def test_delete_payment_success(payment_service: PaymentService, mock_db_session):
    """Test deleting a payment."""
    mock_payment = MockPayment(id=1, status=PaymentStatus.PENDING)

    mock_db_session._mock_scalars.first.return_value = mock_payment

    result = await payment_service.delete_payment(1, user_id=1)

    assert result is True
    mock_db_session.delete.assert_called_once_with(mock_payment)
    mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_payment_not_found(
    payment_service: PaymentService, mock_db_session
):
    """Test deleting a non-existent payment."""
    mock_db_session._mock_scalars.first.return_value = None

    result = await payment_service.delete_payment(999, user_id=1)

    assert result is False
