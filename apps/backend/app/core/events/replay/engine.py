"""Replay Engine - Phase 20: Event Timeline Reconstruction"""
from typing import Optional, Type, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.base_aggregate import BaseAggregate
from app.core.events.store.repositories import EventStoreRepository, SnapshotRepository
from app.core.events.snapshots.snapshot_engine import SnapshotEngine

class ReplayEngine:
    """
    Reconstructs aggregate state by replaying events from the event store.
    Supports time-based recovery: "Show me the state of User X as it was on March 1st".
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = EventStoreRepository(session)
        self.snapshot_repo = SnapshotRepository(session)
        self.snapshot_engine = SnapshotEngine(session)

    async def replay_aggregate(self, aggregate_class: Type[BaseAggregate], aggregate_id: UUID, up_to_version: Optional[int]=None) -> BaseAggregate:
        """
        Reconstruct an aggregate by replaying its entire event history.
        Optionally replay only up to a specific version (time travel).
        """
        snapshot_data = await self.snapshot_engine.restore_from_snapshot(aggregate_id)
        if snapshot_data:
            snapshot_version, snapshot_state = snapshot_data
            aggregate = aggregate_class(aggregate_id)
            aggregate._version = snapshot_version
            from_version = snapshot_version
        else:
            aggregate = aggregate_class(aggregate_id)
            from_version = 0
        events = await self.event_repo.get_events(aggregate_id, from_version=from_version)
        for event in events:
            if up_to_version and event.version > up_to_version:
                break
            from app.core.domain.base_aggregate import DomainEvent
            domain_event = DomainEvent(aggregate_id=event.aggregate_id, event_type=event.event_type, version=event.version, timestamp=event.created_at, metadata=event.metadata)
            aggregate.apply_event(domain_event)
        aggregate.mark_saved()
        return aggregate

    async def replay_at_timestamp(self, aggregate_class: Type[BaseAggregate], aggregate_id: UUID, timestamp: datetime) -> Optional[BaseAggregate]:
        """Reconstruct aggregate state as it was at a point in time."""
        events = await self.event_repo.get_events(aggregate_id)
        target_version = None
        for event in events:
            if event.created_at <= timestamp:
                target_version = event.version
            else:
                break
        if target_version is None:
            return None
        return await self.replay_aggregate(aggregate_class, aggregate_id, up_to_version=target_version)

    async def get_audit_trail(self, aggregate_id: UUID) -> List[dict]:
        """Get complete audit trail for an aggregate (all state changes)."""
        events = await self.event_repo.get_events(aggregate_id)
        return [{'version': e.version, 'event_type': e.event_type, 'timestamp': e.created_at.isoformat(), 'payload': e.payload, 'metadata': e.metadata} for e in events]

    async def get_event_count(self, aggregate_id: UUID) -> int:
        """Get total number of events for an aggregate."""
        return await self.event_repo.get_event_count(aggregate_id)