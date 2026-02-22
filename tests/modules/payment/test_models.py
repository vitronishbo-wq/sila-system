# tests/modules/payment/test_models.py
import os
import pytest
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from modules.payment.models import (
    Payment,
    PaymentTransaction,
    Refund,
    PaymentStatus,
    PaymentMethod,
    TransactionStatus,
    TransactionType,
)
from core.db.base_class import Base


# Get database URL from env or use localhost for local testing
DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv(
        "DATABASE_URL",
        # Use localhost for local tests (not Docker 'db' hostname)
        "postgresql://sila_user:Truman1*Marcelo1*@localhost:5432/sila_test"
    )
).replace("+asyncpg", "")  # Use sync driver for tests


@pytest.fixture(scope="function")
def db_session():
    """Create a PostgreSQL session for tests."""
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        Base.metadata.create_all(bind=engine)
        connection = engine.connect()
        transaction = connection.begin()
        session = Session(bind=connection)

        yield session

        session.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=engine)
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


def test_payment_model(db_session):
    """Test Payment model creation and basic properties."""
    payment = Payment(
        amount=Decimal("1000.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-001",
        description="Test payment",
        metadata_={"order_id": "123"},
    )
    db_session.add(payment)
    db_session.commit()

    fetched = db_session.query(Payment).filter_by(reference="PAY-001").first()
    assert fetched is not None
    assert fetched.amount == Decimal("1000.0")
    assert fetched.status == PaymentStatus.PENDING
    assert fetched.method == PaymentMethod.BNA
    assert fetched.description == "Test payment"
    assert fetched.metadata_ == {"order_id": "123"}
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
        metadata_={},
    )

    db_session.add(payment)
    db_session.commit()

    assert str(payment) == f"<Payment PAY-002 - {PaymentStatus.PROCESSING.value}>"
    assert repr(
        payment) == f"<Payment(id={payment.id}, reference='PAY-002', status='{PaymentStatus.PROCESSING.value}')>"


def test_payment_transaction_model(db_session):
    """Test PaymentTransaction model creation and relationships."""
    payment = Payment(
        amount=Decimal("500.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.M_PESA,
        reference="PAY-002",
        description="Payment for transaction test",
        metadata_={},
    )
    db_session.add(payment)
    db_session.commit()

    transaction = PaymentTransaction(
        payment_id=payment.id,
        amount=Decimal("500.0"),
        currency="AOA",
        type=TransactionType.PAYMENT,
        status=TransactionStatus.PENDING,
        reference="TX-001",
        provider_reference="PROV-123",
        metadata_data={},
    )
    db_session.add(transaction)
    db_session.commit()

    fetched_tx = db_session.query(PaymentTransaction).filter_by(reference="TX-001").first()
    assert fetched_tx is not None
    assert fetched_tx.payment_id == payment.id
    assert fetched_tx.type == TransactionType.PAYMENT
    assert fetched_tx.status == TransactionStatus.PENDING
    assert fetched_tx.provider_reference == "PROV-123"
    assert fetched_tx.payment == payment
    assert transaction in payment.transactions


def test_refund_model_and_methods(db_session):
    """Test Refund model creation and business methods."""
    payment = Payment(
        amount=Decimal("800.0"),
        currency="AOA",
        status=PaymentStatus.COMPLETED,
        method=PaymentMethod.UNITEL_MONEY,
        reference="PAY-003",
        description="Payment for refund test",
        metadata_={},
    )
    db_session.add(payment)
    db_session.commit()

    refund = Refund(
        payment_id=payment.id,
        amount=Decimal("200.0"),
        currency="AOA",
        reason="Customer request",
        status=TransactionStatus.PENDING,
        reference="REF-001",
        metadata_data={},
    )
    db_session.add(refund)
    db_session.commit()

    fetched_refund = db_session.query(Refund).filter_by(reference="REF-001").first()
    assert fetched_refund is not None
    assert fetched_refund.amount == Decimal("200.0")
    assert fetched_refund.status == TransactionStatus.PENDING
    assert fetched_refund.reason == "Customer request"
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
        metadata_={},
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
        metadata_data={},
    )
    db_session.add(refund)
    db_session.commit()

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
        metadata_={},
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
        metadata_data={},
    )
    db_session.add(refund)
    db_session.commit()

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
        metadata_={},
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
        metadata_data={},
    )
    db_session.add(refund)
    db_session.commit()

    refund.process()

    assert refund.cancel() is False
    assert refund.status == TransactionStatus.COMPLETED


def test_payment_reference_unique_constraint(db_session):
    """Test that payment reference must be unique."""
    payment1 = Payment(
        amount=Decimal("100.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.BNA,
        reference="PAY-UNIQUE",
        description="First payment",
        metadata_={},
    )

    payment2 = Payment(
        amount=Decimal("200.0"),
        currency="AOA",
        status=PaymentStatus.PENDING,
        method=PaymentMethod.MULTICAIXA,
        reference="PAY-UNIQUE",
        description="Second payment",
        metadata_={},
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
        metadata_={},
    )
    db_session.add(payment)
    db_session.commit()

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
        metadata_={},
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
        metadata_data={},
    )
    db_session.add(transaction)
    db_session.commit()

    assert transaction.created_at is not None
    assert transaction.updated_at is not None
    assert isinstance(transaction.created_at, datetime)
    assert isinstance(transaction.updated_at, datetime)
