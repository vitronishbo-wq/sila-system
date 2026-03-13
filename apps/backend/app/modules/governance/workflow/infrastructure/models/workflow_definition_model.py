from sqlalchemy import Column, String, Text, Integer, Boolean, JSON, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.domain.db import Base

class WorkflowDefinitionModel(Base):
    """Modelo SQLAlchemy para definição de workflow"""
    __tablename__ = 'wf_definitions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    entity_type = Column(String(50), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_public = Column(Boolean, nullable=False, default=False)
    timeout_hours = Column(Integer, nullable=True)
    definition_metadata = Column('metadata', JSON, nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    states = relationship('WorkflowStateModel', back_populates='workflow', cascade='all, delete-orphan')
    transitions = relationship('WorkflowTransitionModel', back_populates='workflow', cascade='all, delete-orphan')
    instances = relationship('WorkflowInstanceModel', back_populates='workflow')
    __table_args__ = (Index('ix_wf_definitions_code_version', 'code', 'version', unique=True),)