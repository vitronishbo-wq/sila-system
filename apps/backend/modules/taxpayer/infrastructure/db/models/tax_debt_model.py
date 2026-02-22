"""Tax Debt SQLAlchemy Model"""

from sqlalchemy import Column, String, Date, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxDebtModel(Base):
    """SQLAlchemy model for tax debts"""
    __tablename__ = "tax_debts"
    __table_args__ = (
        Index("ix_debts_taxpayer_status", "taxpayer_id", "status"),
        Index("ix_debts_due_date_status", "due_date", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxpayer_id = Column(UUID(as_uuid=True), ForeignKey("taxpayers.id", ondelete="CASCADE"), nullable=False)
    
    debt_number = Column(String(50), unique=True, nullable=False, index=True)
    tax_type = Column(String(50), nullable=False, index=True)
    
    # Values
    original_amount = Column(Numeric(15, 2), nullable=False)
    current_amount = Column(Numeric(15, 2), nullable=False)
    interest = Column(Numeric(15, 2), nullable=True, default=0)
    fines = Column(Numeric(15, 2), nullable=True, default=0)
    
    # Dates
    created_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    
    # Description
    description = Column(String(500), nullable=True)
    
    # Metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    taxpayer = relationship("TaxpayerModel", back_populates="debts")
    payments = relationship("TaxPaymentModel", back_populates="debt", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "taxpayer_id": str(self.taxpayer_id),
            "debt_number": self.debt_number,
            "tax_type": self.tax_type,
            "original_amount": float(self.original_amount),
            "current_amount": float(self.current_amount),
            "interest": float(self.interest) if self.interest else 0,
            "fines": float(self.fines) if self.fines else 0,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "status": self.status,
            "description": self.description
        }
