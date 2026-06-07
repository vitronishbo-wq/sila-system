"""Attachment SQLAlchemy model"""

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from apps.backend.app.core.db import Base


class AttachmentModel(Base):
    """Attachment model for service requests"""

    __tablename__ = "service_request_attachments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(
        UUID(as_uuid=True), ForeignKey("service_requests.id"), nullable=False, index=True
    )
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    storage_url = Column(String(2000), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), nullable=False)
    size_bytes = Column(Integer, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    request = relationship("ServiceRequestModel", back_populates="attachments")


# Re-assign relationship to use the canonical ServiceRequestModel class when available
try:
    from importlib import import_module

    ServiceRequestModel = import_module(
        "apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model"
    ).ServiceRequestModel
    AttachmentModel.request = relationship(ServiceRequestModel, back_populates="attachments")
except Exception:
    # Leave the string-based relationship as fallback
    pass
