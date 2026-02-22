"""Payment model for the payment module."""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import JSON, Column, DateTime, Enum as SQLEnum, Numeric, Integer, String
from sqlalchemy.orm import relationship

from core.db.base_class import Base

from .enums import PaymentMethod, PaymentStatus


class Payment(Base):
    """Payment model representing a payment transaction."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(precision=18, scale=2), nullable=False)
    currency = Column(String(10), nullable=False, default="AOA")
    status = Column(
        SQLEnum(PaymentStatus, native_enum=False),
        default=PaymentStatus.PENDING,
        nullable=False,
    )
    method = Column(SQLEnum(PaymentMethod, native_enum=False), nullable=False)
    description = Column(String(255), nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    transactions = relationship(
        "PaymentTransaction", back_populates="payment", cascade="all, delete-orphan"
    )
    refunds = relationship(
        "Refund", back_populates="payment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, reference='{self.reference}', status='{self.status.value}')>"

    def __str__(self) -> str:
        return f"<Payment {self.reference} - {self.status.value}>"
