from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime
import enum

Base = declarative_base()

class DocumentTypeEnum(str, enum.Enum):
    BI = "BI"
    PASSPORT = "PASSPORT"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    PHOTO = "PHOTO"

class CitizenDocumentModel(Base):
    __tablename__ = "citizen_documents"
    __table_args__ = (
        Index("ix_citizen_documents_citizen_id", "citizen_id"),
        Index("ix_citizen_documents_type", "type"),
        Index("ix_citizen_documents_version", "version"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    citizen_id = Column(UUID(as_uuid=True), ForeignKey('citizen.id'), nullable=False)
    type = Column(Enum(DocumentTypeEnum), nullable=False)
    file_path = Column(String(256), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
