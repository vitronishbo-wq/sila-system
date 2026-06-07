"""
PostgreSQL Models for Event Sourcing
Persistence layer for domain events
"""

import json
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StoredEvent(Base):
    """
    Persistent storage for domain events in PostgreSQL.

    Attributes:
        event_id: Unique event identifier (PK)
        aggregate_id: ID of the aggregate that produced the event
        aggregate_type: Type of aggregate (e.g., Citizen, Payment)
        event_type: Type of event (e.g., CitizenCreated, PaymentProcessed)
        version: Event version for schema evolution
        timestamp: When the event occurred (UTC)
        event_data: Full event payload as JSON
        metadata: Event metadata (user_id, request_id, etc.) as JSON
        created_at: When the event was stored
    """

    __tablename__ = "event_store"
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    aggregate_type = Column(String(255), nullable=False, index=True)
    event_type = Column(String(255), nullable=False, index=True)
    version = Column(Integer, default=1)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )
    event_data = Column(Text, nullable=False)
    event_metadata = Column("event_metadata", Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    __table_args__ = (
        Index("ix_aggregate_id_timestamp", "aggregate_id", "timestamp"),
        Index("ix_event_type_timestamp", "event_type", "timestamp"),
        Index("ix_aggregate_type_timestamp", "aggregate_type", "timestamp"),
        Index("ix_timestamp", "timestamp"),
    )

    def __repr__(self):
        return f"<StoredEvent(event_id={self.event_id}, aggregate_id={self.aggregate_id}, event_type={self.event_type}, timestamp={self.timestamp})>"

    def to_dict(self):
        """Convert stored event to dictionary."""
        return {
            "event_id": str(self.event_id),
            "aggregate_id": str(self.aggregate_id),
            "aggregate_type": self.aggregate_type,
            "event_type": self.event_type,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "event_data": json.loads(self.event_data),
            "event_metadata": json.loads(self.event_metadata) if self.event_metadata else {},
            "created_at": self.created_at.isoformat(),
        }
