from sqlalchemy import Column, String, Text, Boolean, Integer, JSON, ForeignKey, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class WorkflowStateModel(Base):
    """Modelo SQLAlchemy para estados do workflow"""
    __tablename__ = "wf_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("wf_definitions.id", ondelete="CASCADE"), nullable=False)
    
    code = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    is_initial = Column(Boolean, nullable=False, default=False)
    is_final = Column(Boolean, nullable=False, default=False)
    is_auto_forward = Column(Boolean, nullable=False, default=False)
    
    timeout_hours = Column(Integer, nullable=True)
    form_schema = Column(JSON, nullable=True)
    
    state_metadata = Column("metadata", JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    workflow = relationship("WorkflowDefinitionModel", back_populates="states")
    transitions_from = relationship("WorkflowTransitionModel", foreign_keys="WorkflowTransitionModel.from_state_id", back_populates="from_state")
    transitions_to = relationship("WorkflowTransitionModel", foreign_keys="WorkflowTransitionModel.to_state_id", back_populates="to_state")
    
    __table_args__ = (
        Index("ix_wf_states_workflow_code", "workflow_id", "code", unique=True),
    )
