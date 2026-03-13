from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.core.db import Base

class ServiceRequestModel(Base):
    """Modelo SQLAlchemy para pedidos de serviço"""
    __tablename__ = 'service_requests'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_number = Column(String(50), unique=True, nullable=True, index=True)
    citizen_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_by_user_id = Column(UUID(as_uuid=True), nullable=False)
    assigned_to_user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    service_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='RASCUNHO', index=True)
    priority = Column(String(20), nullable=False, default='MEDIA')
    channel = Column(String(20), nullable=False, default='WEB')
    workflow_instance_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    workflow_data = Column(JSON, nullable=True)
    metadata_ = Column('metadata', JSON, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    sla_due_at = Column(DateTime(timezone=True), nullable=True)
    sla_breached = Column(Boolean, default=False, nullable=False)
    attachments = relationship('AttachmentModel', back_populates='request', cascade='all, delete-orphan')
    events = relationship('RequestEventModel', back_populates='request', cascade='all, delete-orphan')
    __table_args__ = (Index('ix_service_requests_citizen_status', 'citizen_id', 'status'), Index('ix_service_requests_assignee_status', 'assigned_to_user_id', 'status'), Index('ix_service_requests_workflow', 'workflow_instance_id'), Index('ix_service_requests_created_at', 'created_at'), Index('ix_service_requests_submitted_at', 'submitted_at'), Index('ix_service_requests_deadline', 'deadline'), Index('ix_service_requests_sla_due', 'sla_due_at'))