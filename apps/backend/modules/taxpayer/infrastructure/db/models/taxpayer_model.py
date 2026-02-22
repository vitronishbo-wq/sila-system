"""Taxpayer SQLAlchemy Model"""

from sqlalchemy import Column, String, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

# NEEDS: from ....core.database import Base
# Assuming base is imported from core

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxpayerModel(Base):
    """SQLAlchemy model for taxpayers"""
    __tablename__ = "taxpayers"
    __table_args__ = (
        Index("ix_taxpayers_nif_status", "nif", "status"),
        Index("ix_taxpayers_email_status", "email", "status"),
        Index("ix_taxpayers_registered_at", "registered_at"),
        Index("ix_taxpayers_agt_sync", "agt_last_sync"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nif = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)
    tax_regime = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)
    
    # Metadata
    registered_by = Column(UUID(as_uuid=True), nullable=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    # AGT data
    agt_status = Column(String(50), nullable=True)
    agt_last_sync = Column(DateTime(timezone=True), nullable=True)
    agt_data = Column(JSONB, nullable=True)
    
    # Additional metadata
    metadata = Column(JSONB, nullable=True)
    tags = Column(JSONB, nullable=True)
    
    # Relationships
    declarations = relationship("TaxDeclarationModel", back_populates="taxpayer", cascade="all, delete-orphan")
    debts = relationship("TaxDebtModel", back_populates="taxpayer", cascade="all, delete-orphan")
    payments = relationship("TaxPaymentModel", back_populates="taxpayer", cascade="all, delete-orphan")
    certificates = relationship("TaxCertificateModel", back_populates="taxpayer", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "nif": self.nif,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "tax_regime": self.tax_regime,
            "status": self.status,
            "registered_by": str(self.registered_by) if self.registered_by else None,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": str(self.updated_by) if self.updated_by else None,
            "agt_status": self.agt_status,
            "agt_last_sync": self.agt_last_sync.isoformat() if self.agt_last_sync else None
        }
