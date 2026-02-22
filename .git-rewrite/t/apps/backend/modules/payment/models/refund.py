"""Refund model for the payment module."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Numeric,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from core.db.base_class import Base
from .enums import TransactionStatus


class Refund(Base):
    """Refund model representing a refund transaction."""

    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    reference = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(precision=18, scale=2), nullable=False)
    currency = Column(String(10), nullable=False, default="AOA")
    reason = Column(String(255), nullable=True)
    status = Column(
        SQLEnum(TransactionStatus, native_enum=False),
        default=TransactionStatus.PENDING,
        nullable=False,
    )
    metadata_data = Column("metadata", JSON, nullable=True, default={})
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    payment = relationship("Payment", back_populates="refunds")

    def __repr__(self) -> str:
        return (
            f"<Refund {self.reference} - {self.amount} {self.currency} ({self.status})>"
        )

    def process(self) -> bool:
        """Process refund: mark as completed if pending."""
        if self.status != TransactionStatus.PENDING:
            return False
        self.status = TransactionStatus.COMPLETED
        self.processed_at = datetime.utcnow()
        return True

    def cancel(self) -> bool:
        """Cancel refund if not yet processed."""
        if self.status != TransactionStatus.PENDING:
            return False
        self.status = TransactionStatus.CANCELLED
        self.processed_at = None
        return True
