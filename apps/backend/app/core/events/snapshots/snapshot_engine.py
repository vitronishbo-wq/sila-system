"""Snapshot Engine - Phase 20: Event Log Optimization"""
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.base_aggregate import BaseAggregate
from app.core.events.store.repositories import SnapshotRepository

class SnapshotEngine:
    """
    Manages snapshotting strategy: saves aggregate state every N events.
    This accelerates replay by avoiding reprocessing thousands of old events.
    """
    SNAPSHOT_INTERVAL = 100

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SnapshotRepository(session)

    async def should_snapshot(self, aggregate_id: UUID, event_count: int) -> bool:
        """Determine if a snapshot should be taken."""
        return event_count > 0 and event_count % self.SNAPSHOT_INTERVAL == 0

    async def save_snapshot(self, aggregate: BaseAggregate, aggregate_type: str) -> None:
        """Save aggregate state as snapshot."""
        state = self._serialize_aggregate(aggregate)
        await self.repository.save_snapshot(aggregate_id=aggregate.id, aggregate_type=aggregate_type, version=aggregate.version, state=state)

    async def restore_from_snapshot(self, aggregate_id: UUID) -> Optional[tuple]:
        """Return (snapshot_version, snapshot_state) or None."""
        snapshot = await self.repository.get_snapshot(aggregate_id)
        if snapshot:
            return (snapshot.version, snapshot.state)
        return None

    def _serialize_aggregate(self, aggregate: BaseAggregate) -> dict:
        """Convert aggregate to JSON-serializable dict."""
        return {'id': str(aggregate.id), 'version': aggregate.version, **self._get_aggregate_state(aggregate)}

    def _get_aggregate_state(self, aggregate: BaseAggregate) -> dict:
        """Extract state from aggregate (override in subclasses)."""
        return {k: v for k, v in aggregate.__dict__.items() if not k.startswith('_')}

    async def cleanup_old_snapshots(self, aggregate_id: UUID) -> int:
        """Remove old snapshots, keeping only the latest."""
        return await self.repository.delete_old_snapshots(aggregate_id, keep_count=1)