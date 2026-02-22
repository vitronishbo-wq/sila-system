import pytest
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.backend.modules.payment.models import (
    Payment,
    PaymentTransaction,
    Refund,
    PaymentStatus,
    PaymentMethod,
    TransactionStatus,
    TransactionType,
)
from apps.backend.core.db.base_class import Base


@pytest.fixture(scope="function")
def db_session():
    """Create a PostgreSQL session for tests."""
    engine = create_engine("postgresql+asyncpg://localhost/sila_test", echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_payment_model(db_session):
    """Test Payment model creation and basic properties."""
    payment = Payment(
        amount=Decimal("1000.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-001",
        description="Test payment",  # Campo obrigatório adicionado
        metadata={"order_id": "123"},  # Campo obrigatório adicionado
    )
    db_session.add(payment)
    db_session.commit()

    fetched = db_session.query(Payment).filter_by(reference="PAY-001").first()
    assert fetched is not None
    assert fetched.amount == Decimal("1000.0")
    assert fetched.status == PaymentStatus.PENDING
    assert fetched.method == PaymentMethod.BNA
    assert fetched.description == "Test payment"
    assert fetched.metadata_data == {"order_id": "123"}  # Stored as metadata_data in DB
    assert fetched.created_at is not None
    assert fetched.updated_at is not None


def test_payment_string_representation(db_session):
    """Test Payment string representations."""
    payment = Payment(
        amount=Decimal("500.0"),
        currency="AOA",
        status=PaymentStatus.PROCESSING,
        method=PaymentMethod.MULTICAIXA,
        reference="PAY-002",
        description="String representation test",
        metadata={},
    )

    db_session.add(payment)
    db_session.commit()

    assert str(payment) == f"<Payment PAY-002 - {PaymentStatus.PROCESSING.value}>"
    assert (
        repr(payment)
        == f"<Payment(id={payment.id}, reference='PAY-002', status='{PaymentStatus.PROCESSING.value}')>"
    )


def test_payment_transaction_model(db_session):
    """Test PaymentTransaction model creation and relationships."""
    # First create a payment
    payment = Payment(
        amount=Decimal("500.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.M_PESA,
        reference="PAY-002",
        description="Payment for transaction test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    # Create transaction linked to payment
    transaction = PaymentTransaction(
        payment_id=payment.id,
        amount=Decimal("500.0"),
        currency="AOA",
        type=TransactionType.PAYMENT,
        status=TransactionStatus.PENDING,
        reference="TX-001",
        provider_reference="PROV-123",
        metadata={},
    )
    db_session.add(transaction)
    db_session.commit()

    # Test transaction properties
    fetched_tx = (
        db_session.query(PaymentTransaction).filter_by(reference="TX-001").first()
    )
    assert fetched_tx is not None
    assert fetched_tx.payment_id == payment.id
    assert fetched_tx.type == TransactionType.PAYMENT
    assert fetched_tx.status == TransactionStatus.PENDING
    assert fetched_tx.provider_reference == "PROV-123"

    # Test relationship
    assert fetched_tx.payment == payment
    assert transaction in payment.transactions


def test_refund_model_and_methods(db_session):
    """Test Refund model creation and business methods."""
    # Create a completed payment
    payment = Payment(
        amount=Decimal("800.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.UNITEL_MONEY,
        reference="PAY-003",
        description="Payment for refund test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    # Create refund
    refund = Refund(
        payment_id=payment.id,
        amount=Decimal("200.0"),
        currency="AOA",
        reason="Customer request",
        status=TransactionStatus.PENDING,
        reference="REF-001",
        metadata={},
    )
    db_session.add(refund)
    db_session.commit()

    # Test refund properties
    fetched_refund = db_session.query(Refund).filter_by(reference="REF-001").first()
    assert fetched_refund is not None
    assert fetched_refund.amount == Decimal("200.0")
    assert fetched_refund.status == TransactionStatus.PENDING
    assert fetched_refund.reason == "Customer request"

    # Test relationship
    assert fetched_refund.payment == payment
    assert fetched_refund in payment.refunds


def test_refund_process_method(db_session):
    """Test refund process method."""
    payment = Payment(
        amount=Decimal("800.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.BNA,
        reference="PAY-004",
        description="Payment for process test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    refund = Refund(
        payment_id=payment.id,
        amount=Decimal("200.0"),
        currency="AOA",
        reason="Test process",
        status=TransactionStatus.PENDING,
        reference="REF-002",
        metadata={},
    )
    db_session.add(refund)
    db_session.commit()

    # Test successful processing
    assert refund.process() is True
    assert refund.status == TransactionStatus.COMPLETED
    assert refund.processed_at is not None


def test_refund_cancel_method(db_session):
    """Test refund cancel method."""
    payment = Payment(
        amount=Decimal("800.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.BNA,
        reference="PAY-005",
        description="Payment for cancel test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    refund = Refund(
        payment_id=payment.id,
        amount=Decimal("200.0"),
        currency="AOA",
        reason="Test cancel",
        status=TransactionStatus.PENDING,
        reference="REF-003",
        metadata={},
    )
    db_session.add(refund)
    db_session.commit()

    # Test successful cancellation
    assert refund.cancel() is True
    assert refund.status == TransactionStatus.CANCELLED
    assert refund.processed_at is None


def test_refund_cannot_cancel_after_processed(db_session):
    """Test that refund cannot be cancelled after being processed."""
    payment = Payment(
        amount=Decimal("800.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.BNA,
        reference="PAY-006",
        description="Payment for cancel after process test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    refund = Refund(
        payment_id=payment.id,
        amount=Decimal("200.0"),
        currency="AOA",
        reason="Test cancel after process",
        status=TransactionStatus.PENDING,
        reference="REF-004",
        metadata={},
    )
    db_session.add(refund)
    db_session.commit()

    # Process first
    refund.process()

    # Then try to cancel (should fail)
    assert refund.cancel() is False
    assert refund.status == TransactionStatus.COMPLETED  # Should remain completed


def test_payment_reference_unique_constraint(db_session):
    """Test that payment reference must be unique."""
    payment1 = Payment(
        amount=Decimal("100.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-UNIQUE",
        description="First payment",
        metadata={},
    )

    payment2 = Payment(
        amount=Decimal("200.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.MULTICAIXA,
        reference="PAY-UNIQUE",  # Same reference - should fail
        description="Second payment",
        metadata={},
    )

    db_session.add(payment1)
    db_session.commit()

    db_session.add(payment2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_payment_status_flow(db_session):
    """Test payment status transitions."""
    payment = Payment(
        amount=Decimal("300.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-007",
        description="Status flow test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    # Simulate status transitions
    payment.status = PaymentStatus.PROCESSING
    db_session.commit()
    assert payment.status == PaymentStatus.PROCESSING

    payment.status = PaymentStatus.COMPLETED
    db_session.commit()
    assert payment.status == PaymentStatus.COMPLETED


def test_transaction_timestamps(db_session):
    """Test that transactions have proper timestamps."""
    payment = Payment(
        amount=Decimal("400.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-008",
        description="Timestamp test",
        metadata={},
    )
    db_session.add(payment)
    db_session.commit()

    transaction = PaymentTransaction(
        payment_id=payment.id,
        amount=Decimal("400.0"),
        currency="AOA",
        type=TransactionType.PAYMENT,
        status=TransactionStatus.PENDING,
        reference="TX-002",
        metadata={},
    )
    db_session.add(transaction)
    db_session.commit()

    assert transaction.created_at is not None
    assert transaction.updated_at is not None
    assert isinstance(transaction.created_at, datetime)
    assert isinstance(transaction.updated_at, datetime)
