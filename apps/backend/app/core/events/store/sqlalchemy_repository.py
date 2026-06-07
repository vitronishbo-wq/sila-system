"""Event Store Repository - Phase 20"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import EventStoreEntry, ProjectionEntry, SnapshotEntry


class EventStoreRepository:
    """Repository for immutable event log operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def append(
        self,
        aggregate_id: UUID,
        aggregate_type: str,
        event_type: str,
        version: int,
        payload: dict,
        event_metadata: dict = None,
    ) -> EventStoreEntry:
        """Append a new event to the store (write-only)."""
        event = EventStoreEntry(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            event_type=event_type,
            version=version,
            payload=payload,
            event_metadata=event_metadata,
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def get_events(self, aggregate_id: UUID, from_version: int = 0) -> list[EventStoreEntry]:
        """Retrieve all events for an aggregate (for replay)."""
        stmt = (
            select(EventStoreEntry)
            .where(
                and_(
                    EventStoreEntry.aggregate_id == aggregate_id,
                    EventStoreEntry.version > from_version,
                )
            )
            .order_by(EventStoreEntry.version.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_events_since(self, aggregate_type: str, since: datetime) -> list[EventStoreEntry]:
        """Get all events of a type since a given time (for projections)."""
        stmt = (
            select(EventStoreEntry)
            .where(
                and_(
                    EventStoreEntry.aggregate_type == aggregate_type,
                    EventStoreEntry.created_at >= since,
                )
            )
            .order_by(EventStoreEntry.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_latest_version(self, aggregate_id: UUID) -> int:
        """Get the latest version number for an aggregate."""
        stmt = select(func.max(EventStoreEntry.version)).where(
            EventStoreEntry.aggregate_id == aggregate_id
        )
        result = await self.session.execute(stmt)
        version = result.scalar()
        return version if version is not None else 0

    async def get_event_count(self, aggregate_id: UUID) -> int:
        """Count events for an aggregate."""
        stmt = select(func.count(EventStoreEntry.id)).where(
            EventStoreEntry.aggregate_id == aggregate_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0


class SnapshotRepository:
    """Repository for snapshot operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_snapshot(
        self, aggregate_id: UUID, aggregate_type: str, version: int, state: dict
    ) -> SnapshotEntry:
        """Save/update snapshot for an aggregate."""
        stmt = select(SnapshotEntry).where(SnapshotEntry.aggregate_id == aggregate_id)
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            existing.version = version
            existing.state = state
            existing.created_at = datetime.utcnow()
        else:
            existing = SnapshotEntry(
                aggregate_id=aggregate_id,
                aggregate_type=aggregate_type,
                version=version,
                state=state,
            )
            self.session.add(existing)
        await self.session.flush()
        return existing

    async def get_snapshot(self, aggregate_id: UUID) -> SnapshotEntry | None:
        """Retrieve latest snapshot for an aggregate."""
        stmt = select(SnapshotEntry).where(SnapshotEntry.aggregate_id == aggregate_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_old_snapshots(self, aggregate_id: UUID, keep_count: int = 1) -> int:
        """Delete old snapshots, keeping only the latest."""
        stmt = (
            select(SnapshotEntry)
            .where(SnapshotEntry.aggregate_id == aggregate_id)
            .order_by(SnapshotEntry.created_at.desc())
            .offset(keep_count)
        )
        result = await self.session.execute(stmt)
        old_snapshots = result.scalars().all()
        for snapshot in old_snapshots:
            await self.session.delete(snapshot)
        return len(old_snapshots)


class ProjectionRepository:
    """Repository for CQRS read models."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_projection(
        self, projection_name: str, aggregate_id: UUID, data: dict, version: int
    ) -> ProjectionEntry:
        """Create or update a projection."""
        stmt = select(ProjectionEntry).where(
            and_(
                ProjectionEntry.projection_name == projection_name,
                ProjectionEntry.aggregate_id == aggregate_id,
            )
        )
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            existing.data = data
            existing.last_event_version = version
        else:
            existing = ProjectionEntry(
                projection_name=projection_name,
                aggregate_id=aggregate_id,
                data=data,
                last_event_version=version,
            )
            self.session.add(existing)
        await self.session.flush()
        return existing

    async def get_projection(self, projection_name: str, aggregate_id: UUID) -> dict | None:
        """Retrieve a projection's data."""
        stmt = select(ProjectionEntry.data).where(
            and_(
                ProjectionEntry.projection_name == projection_name,
                ProjectionEntry.aggregate_id == aggregate_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def list_projections(self, projection_name: str) -> list[dict]:
        """List all projections of a specific type."""
        stmt = select(ProjectionEntry.data).where(
            ProjectionEntry.projection_name == projection_name
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
