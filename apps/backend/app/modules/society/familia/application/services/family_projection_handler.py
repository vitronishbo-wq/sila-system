from __future__ import annotations
from uuid import UUID
from app.modules.society.familia.application.ports.family_aggregate_repository_port import FamilyAggregateRepositoryPort
from app.modules.society.familia.application.ports.projection_repository_port import ProjectionRepositoryPort
from app.modules.society.familia.infrastructure.projections.family_composition_projector import FamilyCompositionProjector

class FamilyProjectionHandler:

    def __init__(self, *, projection_repository: ProjectionRepositoryPort, family_repository: FamilyAggregateRepositoryPort) -> None:
        self._projection_repository = projection_repository
        self._family_repository = family_repository
        self._composition_projector = FamilyCompositionProjector()

    async def on_family_created(self, event: object) -> None:
        await self._refresh_family_projection(event)

    async def on_family_member_added(self, event: object) -> None:
        await self._refresh_family_projection(event)

    async def on_family_changed(self, payload: dict) -> None:
        await self._projection_repository.upsert_family_composition(payload)

    async def _refresh_family_projection(self, event: object) -> None:
        aggregate_id = getattr(event, 'aggregate_id', None)
        if aggregate_id is None and hasattr(event, 'to_payload'):
            try:
                aggregate_id = (event.to_payload() or {}).get('aggregate_id')
            except Exception:
                aggregate_id = None
        if aggregate_id is None and hasattr(event, 'payload'):
            aggregate_id = getattr(event, 'payload', {}).get('aggregate_id')
        if aggregate_id is None:
            return
        aggregate_uuid = aggregate_id if isinstance(aggregate_id, UUID) else UUID(str(aggregate_id))
        aggregate = await self._family_repository.get_by_id(aggregate_uuid)
        if aggregate is None:
            return
        payload = self._composition_projector.project_from_aggregate(aggregate)
        await self._projection_repository.upsert_family_composition(payload)