"""Event Store Models - Phase 20: Immutable Event Log"""

from datetime import datetime
from uuid import uuid4

from apps.backend.app.core.db.base_class import Base
from sqlalchemy import JSON, Column, DateTime, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


class EventStoreEntry(Base):
    """
    Immutable append-only log of all domain events.
    This is the single source of truth for all state changes in the system.
    """

    __tablename__ = "event_store"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    aggregate_type = Column(String(100), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    payload = Column(JSON, nullable=False)
    event_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    __table_args__ = (
        Index("ix_event_store_aggregate_version", "aggregate_id", "version", unique=True),
        Index("ix_event_store_type_created", "event_type", "created_at"),
        Index("ix_event_store_aggregate_type", "aggregate_type"),
        UniqueConstraint("aggregate_id", "version", name="uq_event_store_version"),
    )

    def __repr__(self):
        return f"<EventStoreEntry {self.aggregate_type}:{self.aggregate_id} v{self.version}>"


class SnapshotEntry(Base):
    """
    Snapshot of aggregate state at a specific version.
    Reduces replay time: instead of replaying 10,000 events, replay last 100.
    """

    __tablename__ = "event_store_snapshots"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    aggregate_type = Column(String(100), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    state = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    __table_args__ = (Index("ix_snapshot_aggregate_version", "aggregate_id", "version"),)

    def __repr__(self):
        return f"<SnapshotEntry {self.aggregate_type}:{self.aggregate_id} v{self.version}>"


class ProjectionEntry(Base):
    """
    Read model for CQRS - denormalized, optimized for queries.
    Projections are built from the event store and fast to query.
    """

    __tablename__ = "event_store_projections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    projection_name = Column(String(100), nullable=False, index=True)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False)
    data = Column(JSON, nullable=False)
    last_event_version = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    __table_args__ = (Index("ix_projection_name_aggregate", "projection_name", "aggregate_id"),)

    def __repr__(self):
        return f"<ProjectionEntry {self.projection_name}:{self.aggregate_id}>"
