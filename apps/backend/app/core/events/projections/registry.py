"""Projection Registry - Phase 20: CQRS Read Models"""

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.core.domain.base_aggregate import DomainEvent
from apps.backend.app.core.events.store.repositories import ProjectionRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BaseProjection(ABC):
    """Base class for all CQRS projections."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this projection."""
        pass

    @abstractmethod
    async def handle_event(self, event: DomainEvent) -> dict | None:
        """Transform event into projection data."""
        pass


class ProjectionRegistry:
    """
    Registry of all CQRS projections.
    When an event occurs, all registered projections are updated.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProjectionRepository(session)
        self._projections: dict[str, list[BaseProjection]] = {}

    def register_projection(self, event_type: str, projection: BaseProjection) -> None:
        """Register a projection to handle an event type."""
        if event_type not in self._projections:
            self._projections[event_type] = []
        self._projections[event_type].append(projection)

    async def project(self, event: DomainEvent) -> None:
        """
        Apply an event to all relevant projections.
        Projections update their read models asynchronously.
        """
        handlers = self._projections.get(event.event_type, [])
        for projection in handlers:
            try:
                data = await projection.handle_event(event)
                if data:
                    await self.repository.upsert_projection(
                        projection_name=projection.name,
                        aggregate_id=event.aggregate_id,
                        data=data,
                        version=event.version,
                    )
            except Exception as e:
                print(f"Projection {projection.name} failed: {e}")

    async def get_projection(self, projection_name: str, aggregate_id: UUID) -> dict | None:
        """Retrieve a projected read model."""
        return await self.repository.get_projection(projection_name, aggregate_id)

    async def list_projections(self, projection_name: str) -> list[dict]:
        """Retrieve all items in a projection."""
        return await self.repository.list_projections(projection_name)

    def clear_registrations(self) -> None:
        """Clear all registrations (for testing)."""
        self._projections.clear()
