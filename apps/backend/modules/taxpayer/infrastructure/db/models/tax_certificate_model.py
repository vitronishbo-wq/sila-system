"""Tax Certificate SQLAlchemy Model"""

from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class TaxCertificateModel(Base):
    """SQLAlchemy model for tax certificates"""
    __tablename__ = "tax_certificates"
    __table_args__ = (
        Index("ix_certificates_taxpayer_type", "taxpayer_id", "certificate_type"),
        Index("ix_certificates_expires", "expires_at"),
        Index("ix_certificates_status", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxpayer_id = Column(UUID(as_uuid=True), ForeignKey("taxpayers.id", ondelete="CASCADE"), nullable=False)
    
    certificate_number = Column(String(50), unique=True, nullable=False, index=True)
    certificate_type = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=True)
    
    status = Column(String(50), nullable=False, default="PENDING", index=True)
    
    # Dates
    issued_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(Date, nullable=True)
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Who
    requested_by = Column(UUID(as_uuid=True), nullable=False)
    issued_by = Column(UUID(as_uuid=True), nullable=True)
    
    # File
    file_url = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_hash = Column(String(128), nullable=True)
    
    # AGT
    agt_reference = Column(String(100), nullable=True)
    
    # Purpose
    purpose = Column(String(500), nullable=True)
    
    # Metadata
    metadata = Column(JSONB, nullable=True)
    error_message = Column(String(500), nullable=True)
    
    # Relationships
    taxpayer = relationship("TaxpayerModel", back_populates="certificates")
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "taxpayer_id": str(self.taxpayer_id),
            "certificate_number": self.certificate_number,
            "certificate_type": self.certificate_type,
            "year": self.year,
            "status": self.status,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "requested_by": str(self.requested_by) if self.requested_by else None,
            "issued_by": str(self.issued_by) if self.issued_by else None,
            "file_url": self.file_url,
            "purpose": self.purpose
        }
