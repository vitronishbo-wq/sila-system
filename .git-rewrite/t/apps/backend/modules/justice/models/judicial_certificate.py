"""Judicial Certificate model for the justice module."""

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db.base_class import Base


class CertificateType(str, Enum):
    """Types of judicial certificates."""

    CRIMINAL_RECORD = "criminal_record"
    CIVIL_RECORD = "civil_record"
    MARRIAGE_CERTIFICATE = "marriage_certificate"
    DIVORCE_CERTIFICATE = "divorce_certificate"
    BIRTH_CERTIFICATE = "birth_certificate"
    DEATH_CERTIFICATE = "death_certificate"
    PROPERTY_CERTIFICATE = "property_certificate"
    BUSINESS_CERTIFICATE = "business_certificate"


class CertificateStatus(str, Enum):
    """Status of judicial certificates."""

    PENDING = "pending"
    ISSUED = "issued"
    REJECTED = "rejected"
    EXPIRED = "expired"


class JudicialCertificate(Base):
    """Model for judicial certificates."""

    __tablename__ = "justice_judicial_certificates"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    # Citizen reference
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=False, index=True)

    # Certificate details
    type = Column(SQLEnum(CertificateType), nullable=False, index=True)
    status = Column(
        SQLEnum(CertificateStatus), default=CertificateStatus.PENDING, index=True
    )
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    # Issuance details
    issued_by = Column(Integer, ForeignKey("justice_users.id"), nullable=True)
    issued_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    citizen = relationship(
        "Citizen", foreign_keys=[citizen_id], back_populates="judicial_certificates"
    )
    issuer = relationship("User", foreign_keys=[issued_by])

    def __repr__(self):
        return f"<JudicialCertificate(id={self.id}, citizen_id={self.citizen_id}, type={self.type})>"

    @property
    def is_expired(self) -> bool:
        """Check if the certificate is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if the certificate is valid."""
        return self.status == CertificateStatus.ISSUED and not self.is_expired
