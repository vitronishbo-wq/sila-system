"""Attachment SQLAlchemy model"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.domain.db import Base

class AttachmentModel(Base):
    """Attachment model for service requests"""
    __tablename__ = 'service_request_attachments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey('service_requests.id'), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    storage_url = Column(String(2000), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), nullable=False)
    size_bytes = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    request = relationship('ServiceRequestModel', back_populates='attachments')