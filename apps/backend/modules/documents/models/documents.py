"""
Document models with UUID support and User integration.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base


import enum


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentVersion(Base):
    """
    Version history for documents.
    """
    __tablename__ = "document_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)

    version_number = Column(Integer, nullable=False)  # 1, 2, 3...
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    changelog = Column(String(500), nullable=True)

    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="versions",
                            foreign_keys=[document_id])
    uploaded_by = relationship("User")


class Document(Base):
    """
    Document model for storing file metadata and ownership.
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # e.g. 'pdf', 'docx'
    file_size = Column(Integer, nullable=False)  # in bytes

    # MIME type and Checksum for integrity
    mime_type = Column(String(100), nullable=True)
    checksum = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)

    # Ownership and Organization
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("document_folders.id"), nullable=True)

    # Versão atual (aponta para a mais recente)
    current_version_id = Column(UUID(as_uuid=True), ForeignKey(
        "document_versions.id"), nullable=True)

    # Status and Metadata
    status = Column(String(50), default=DocumentStatus.PENDING, index=True)
    original_filename = Column(String(255), nullable=True)
    content_type = Column(String(100), nullable=True)
    ocr_text = Column(Text, nullable=True)
    ocr_text_path = Column(String(500), nullable=True)
    thumbnail_path = Column(String(500), nullable=True)
    processed_at = Column(DateTime, nullable=True)

    is_public = Column(Boolean, default=False)
    metadata_info = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="documents")
    folder = relationship("DocumentFolder", back_populates="documents")
    versions = relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan",
        foreign_keys="[DocumentVersion.document_id]",
        order_by="desc(DocumentVersion.version_number)"
    )
    current_version = relationship("DocumentVersion", foreign_keys=[current_version_id])


class DocumentFolder(Base):
    """
    Hierarchical folder structure for documents.
    """
    __tablename__ = "document_folders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    parent_id = Column(UUID(as_uuid=True), ForeignKey("document_folders.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="folders")
    parent = relationship("DocumentFolder", remote_side=[id], back_populates="children")
    children = relationship("DocumentFolder", back_populates="parent", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="folder")

