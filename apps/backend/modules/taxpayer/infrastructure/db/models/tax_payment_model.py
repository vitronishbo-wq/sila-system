"""Tax Payment SQLAlchemy Model"""

from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxPaymentModel(Base):
    """SQLAlchemy model for tax payments"""
    __tablename__ = "tax_payments"
    __table_args__ = (
        Index("ix_payments_taxpayer_date", "taxpayer_id", "payment_date"),
        Index("ix_payments_debt", "debt_id"),
        Index("ix_payments_reference", "reference"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxpayer_id = Column(UUID(as_uuid=True), ForeignKey("taxpayers.id", ondelete="CASCADE"), nullable=False)
    debt_id = Column(UUID(as_uuid=True), ForeignKey("tax_debts.id", ondelete="CASCADE"), nullable=False)
    
    payment_number = Column(String(50), unique=True, nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    status = Column(String(50), nullable=False, default="COMPLETED", index=True)
    reference = Column(String(255), nullable=True)
    
    paid_by = Column(UUID(as_uuid=True), nullable=False)
    
    # Metadata
    metadata = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    taxpayer = relationship("TaxpayerModel", back_populates="payments")
    debt = relationship("TaxDebtModel", back_populates="payments")
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "taxpayer_id": str(self.taxpayer_id),
            "debt_id": str(self.debt_id),
            "payment_number": self.payment_number,
            "amount": float(self.amount),
            "payment_method": self.payment_method,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "status": self.status,
            "reference": self.reference,
            "paid_by": str(self.paid_by) if self.paid_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
