"""Legal document model for the justice module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db.base_class import Base


class DocumentType(str, Enum):
    """Types of legal documents."""

    PETITION = "petition"
    MOTION = "motion"
    RULING = "ruling"
    SENTENCE = "sentence"
    APPEAL = "appeal"
    CERTIFICATE = "certificate"
    SUBPOENA = "subpoena"
    WARRANT = "warrant"
    EVIDENCE = "evidence"
    EXPERT_REPORT = "expert_report"
    WITNESS_STATEMENT = "witness_statement"
    CONTRACT = "contract"
    POWER_OF_ATTORNEY = "power_of_attorney"
    NOTIFICATION = "notification"


class DocumentStatus(str, Enum):
    """Status of legal documents."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ISSUED = "issued"
    SERVED = "served"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class DocumentCategory(str, Enum):
    """Categories of legal documents."""

    JUDICIAL = "judicial"
    ADMINISTRATIVE = "administrative"
    EVIDENCE = "evidence"
    CORRESPONDENCE = "correspondence"
    CERTIFICATE = "certificate"
    PROCEDURAL = "procedural"


class LegalDocument(Base):
    """Legal document model for storing case-related documents."""

    __tablename__ = "justice_legal_documents"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(
        Integer, ForeignKey("justice_cases.id"), nullable=True, index=True
    )

    # Document identification
    document_number = Column(String(50), unique=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    document_type = Column(SQLEnum(DocumentType), nullable=False, index=True)
    category = Column(SQLEnum(DocumentCategory), nullable=False, index=True)
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.DRAFT, index=True)

    # Content and file information
    content = Column(Text)  # Text content of the document
    file_path = Column(String(500))  # Path to stored file
    file_name = Column(String(200))
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))

    # Legal information
    issuing_authority = Column(String(200))
    recipient = Column(String(200))
    legal_basis = Column(Text)  # Legal foundation for the document
    validity_period_days = Column(Integer)

    # Dates
    issue_date = Column(DateTime, default=func.now())
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    service_date = Column(DateTime)  # When document was served

    # Security and access
    is_confidential = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    requires_signature = Column(Boolean, default=False)
    is_signed = Column(Boolean, default=False)
    digital_signature = Column(Text)  # Digital signature hash

    # Administrative
    created_by = Column(Integer, ForeignKey("justice_users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("justice_users.id"))
    updated_by = Column(Integer, ForeignKey("justice_users.id"))

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    case = relationship("Case", foreign_keys=[case_id], back_populates="documents")

    def __repr__(self):
        return f"<LegalDocument(document_number='{self.document_number}', title='{self.title}', type='{self.document_type}')>"

    @property
    def is_valid(self) -> bool:
        """Check if document is currently valid."""
        if self.status not in [DocumentStatus.APPROVED, DocumentStatus.ISSUED]:
            return False
        if self.expiry_date and self.expiry_date < datetime.utcnow():
            return False
        return True

    @property
    def is_expired(self) -> bool:
        """Check if document has expired."""
        return self.expiry_date and self.expiry_date < datetime.utcnow()

    @property
    def days_until_expiry(self) -> Optional[int]:
        """Calculate days until document expires."""
        if not self.expiry_date:
            return None
        delta = self.expiry_date - datetime.utcnow()
        return delta.days if delta.days > 0 else 0
