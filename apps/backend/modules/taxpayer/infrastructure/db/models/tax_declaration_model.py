"""Tax Declaration SQLAlchemy Model"""

from sqlalchemy import Column, String, Date, DateTime, Numeric, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxDeclarationModel(Base):
    """SQLAlchemy model for tax declarations"""
    __tablename__ = "tax_declarations"
    __table_args__ = (
        Index("ix_declarations_taxpayer_period", "taxpayer_id", "tax_period"),
        Index("ix_declarations_status_date", "status", "declaration_date"),
        Index("ix_declarations_due_date", "due_date"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxpayer_id = Column(UUID(as_uuid=True), ForeignKey("taxpayers.id", ondelete="CASCADE"), nullable=False)
    
    declaration_number = Column(String(50), unique=True, nullable=False, index=True)
    tax_type = Column(String(50), nullable=False, index=True)
    tax_period = Column(String(20), nullable=False, index=True)
    
    # Values
    gross_amount = Column(Numeric(15, 2), nullable=False)
    deductions = Column(Numeric(15, 2), nullable=True, default=0)
    net_amount = Column(Numeric(15, 2), nullable=False)
    
    # Dates
    declaration_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    
    # Status
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    protocol = Column(String(100), nullable=True)
    
    # Processing
    submitted_by = Column(UUID(as_uuid=True), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_by = Column(UUID(as_uuid=True), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Notes
    observations = Column(String(500), nullable=True)
    error_message = Column(String(500), nullable=True)
    
    # Metadata
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    taxpayer = relationship("TaxpayerModel", back_populates="declarations")
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "taxpayer_id": str(self.taxpayer_id),
            "declaration_number": self.declaration_number,
            "tax_type": self.tax_type,
            "tax_period": self.tax_period,
            "gross_amount": float(self.gross_amount),
            "deductions": float(self.deductions) if self.deductions else 0,
            "net_amount": float(self.net_amount),
            "declaration_date": self.declaration_date.isoformat() if self.declaration_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "protocol": self.protocol,
            "submitted_by": str(self.submitted_by) if self.submitted_by else None,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "processed_by": str(self.processed_by) if self.processed_by else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "observations": self.observations
        }
