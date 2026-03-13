"""Outbox Model for transactional event storage - Phase 19"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean, TIMESTAMP, Integer
from datetime import datetime
from uuid import uuid4
from app.core.db.base_class import Base

class OutboxEvent(Base):
    """Outbox table for guaranteed event publishing (transactional)"""
    __tablename__ = 'event_outbox'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    event_name = Column(String(255), nullable=False, index=True)
    event_id = Column(String(36), nullable=False, unique=True)
    payload = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True)
    processed_at = Column(TIMESTAMP, nullable=True)
    processed = Column(Boolean, default=False, nullable=False, index=True)
    retry_count = Column(Integer, default=0)

    def __repr__(self):
        return f'<OutboxEvent {self.event_name}:{self.id}>'