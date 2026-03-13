from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.core.db import Base

class WorkflowTaskModel(Base):
    """Modelo SQLAlchemy para tarefas do workflow"""
    __tablename__ = 'wf_tasks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instance_id = Column(UUID(as_uuid=True), ForeignKey('wf_instances.id', ondelete='CASCADE'), nullable=False)
    state_id = Column(UUID(as_uuid=True), ForeignKey('wf_states.id'), nullable=False)
    transition_id = Column(UUID(as_uuid=True), ForeignKey('wf_transitions.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to = Column(UUID(as_uuid=True), nullable=True, index=True)
    assigned_role = Column(String(100), nullable=True)
    assignment_type = Column(String(50), nullable=False, default='ROLE')
    status = Column(String(50), nullable=False, default='PENDING', index=True)
    priority = Column(String(20), nullable=False, default='MEDIUM')
    form_data = Column(JSON, nullable=True)
    result_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    due_at = Column(DateTime(timezone=True), nullable=True)
    timeout_hours = Column(Integer, nullable=True)
    task_metadata = Column('metadata', JSON, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    instance = relationship('WorkflowInstanceModel', back_populates='tasks')
    state = relationship('WorkflowStateModel')
    transition = relationship('WorkflowTransitionModel')
    __table_args__ = (Index('ix_wf_tasks_assigned', 'assigned_to', 'status'), Index('ix_wf_tasks_due', 'due_at'))