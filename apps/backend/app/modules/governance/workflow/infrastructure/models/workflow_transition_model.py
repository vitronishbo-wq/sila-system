from sqlalchemy import Column, String, Text, JSON, ForeignKey, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.core.db import Base

class WorkflowTransitionModel(Base):
    """Modelo SQLAlchemy para transições do workflow"""
    __tablename__ = 'wf_transitions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('wf_definitions.id', ondelete='CASCADE'), nullable=False)
    from_state_id = Column(UUID(as_uuid=True), ForeignKey('wf_states.id', ondelete='CASCADE'), nullable=False)
    to_state_id = Column(UUID(as_uuid=True), ForeignKey('wf_states.id', ondelete='CASCADE'), nullable=False)
    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    transition_type = Column(String(50), nullable=False, default='USER')
    assignment_type = Column(String(50), nullable=False, default='ROLE')
    assignment_value = Column(String(255), nullable=True)
    condition_expression = Column(Text, nullable=True)
    required_permissions = Column(ARRAY(String), nullable=True)
    required_roles = Column(ARRAY(String), nullable=True)
    pre_actions = Column(JSON, nullable=True)
    post_actions = Column(JSON, nullable=True)
    transition_metadata = Column('metadata', JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    workflow = relationship('WorkflowDefinitionModel', back_populates='transitions')
    from_state = relationship('WorkflowStateModel', foreign_keys=[from_state_id], back_populates='transitions_from')
    to_state = relationship('WorkflowStateModel', foreign_keys=[to_state_id], back_populates='transitions_to')
    __table_args__ = (Index('ix_wf_transitions_workflow_code', 'workflow_id', 'code', unique=True), Index('ix_wf_transitions_from_state', 'from_state_id'))