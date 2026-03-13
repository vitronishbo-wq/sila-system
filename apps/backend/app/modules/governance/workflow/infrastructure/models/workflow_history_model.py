from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.core.db import Base

class WorkflowHistoryModel(Base):
    """Modelo SQLAlchemy para histórico do workflow"""
    __tablename__ = 'wf_history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instance_id = Column(UUID(as_uuid=True), ForeignKey('wf_instances.id', ondelete='CASCADE'), nullable=False)
    from_state_id = Column(UUID(as_uuid=True), nullable=True)
    to_state_id = Column(UUID(as_uuid=True), nullable=True)
    transition_id = Column(UUID(as_uuid=True), nullable=True)
    task_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(100), nullable=False)
    action_type = Column(String(50), nullable=False)
    performed_by = Column(UUID(as_uuid=True), nullable=True)
    performed_by_role = Column(String(100), nullable=True)
    comment = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    history_metadata = Column('metadata', JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    instance = relationship('WorkflowInstanceModel', back_populates='history')
    __table_args__ = (Index('ix_wf_history_instance', 'instance_id', 'created_at'), Index('ix_wf_history_performed_by', 'performed_by'))