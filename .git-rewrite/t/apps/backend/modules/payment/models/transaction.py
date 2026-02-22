"""Transaction model for the payment module."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum as SQLEnum,
    Numeric,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from core.db.base_class import Base
from .enums import TransactionStatus, TransactionType


class PaymentTransaction(Base):
    """Transaction model representing a single transaction within a payment."""

    __tablename__ = "payment_transactions"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    reference = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(precision=18, scale=2), nullable=False)
    currency = Column(String(10), nullable=False, default="AOA")
    type = Column(SQLEnum(TransactionType, native_enum=False), nullable=False)
    status = Column(
        SQLEnum(TransactionStatus, native_enum=False),
        default=TransactionStatus.PENDING,
        nullable=False,
    )
    provider_reference = Column(String(50), nullable=True)
    metadata_data = Column("metadata", JSON, nullable=True, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    payment = relationship("Payment", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction {self.reference} - {self.amount} {self.currency} ({self.status})>"
