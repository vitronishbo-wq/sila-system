# modules/payment/models/payment.py
"""Payment model."""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum as SQLEnum, Numeric, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from config.database import Base
from .enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    # Changed to PG_UUID to match users.id
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
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
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    transactions = relationship(
        "PaymentTransaction", back_populates="payment", cascade="all, delete-orphan"
    )
    refunds = relationship(
        "Refund", back_populates="payment", cascade="all, delete-orphan"
    )
    owner = relationship("User", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, status='{self.status.value}')>"

    def __str__(self) -> str:
        return f"<Payment {self.reference} - {self.status.value}>"

