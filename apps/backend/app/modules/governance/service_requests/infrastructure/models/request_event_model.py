"""Request event SQLAlchemy model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.db import Base

class RequestEventModel(Base):
    """Request event model for audit trail"""
    __tablename__ = 'service_request_events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey('service_requests.id'), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=True)
    actor_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    request = relationship('ServiceRequestModel', back_populates='events')
    __table_args__ = (Index('ix_request_events_request_created', 'request_id', 'created_at'),)