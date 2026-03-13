from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.db import Base

class WorkflowInstanceModel(Base):
    """Modelo SQLAlchemy para instâncias do workflow"""
    __tablename__ = 'wf_instances'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('wf_definitions.id'), nullable=False)
    current_state_id = Column(UUID(as_uuid=True), ForeignKey('wf_states.id'), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    citizen_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), nullable=True, index=True)
    status = Column(String(50), nullable=False, default='ACTIVE')
    variables = Column(JSON, nullable=True)
    context = Column(JSON, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    timeout_hours = Column(Integer, nullable=True)
    instance_metadata = Column('metadata', JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    workflow = relationship('WorkflowDefinitionModel', back_populates='instances')
    current_state = relationship('WorkflowStateModel')
    tasks = relationship('WorkflowTaskModel', back_populates='instance', cascade='all, delete-orphan')
    history = relationship('WorkflowHistoryModel', back_populates='instance', cascade='all, delete-orphan')
    __table_args__ = (Index('ix_wf_instances_entity', 'entity_type', 'entity_id'), Index('ix_wf_instances_citizen', 'citizen_id'), Index('ix_wf_instances_assigned', 'assigned_to'), Index('ix_wf_instances_status', 'status'), Index('ix_wf_instances_deadline', 'deadline'))