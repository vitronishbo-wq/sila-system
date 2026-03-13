from __future__ import annotations
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.familia.application.ports.projection_repository_port import ProjectionRepositoryPort
from app.modules.society.familia.infrastructure.models.projection_models import FamilyCompositionViewModel

class RedisProjectionRepository(ProjectionRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_family_composition(self, family_id: UUID) -> dict | None:
        model = await self._session.get(FamilyCompositionViewModel, family_id)
        if model is None:
            return None
        return {'id': model.family_id, 'code': model.composition_json.get('code', ''), 'head_citizen_id': model.head_citizen_id, 'status': model.composition_json.get('status', 'ACTIVE'), 'member_count': model.member_count, 'created_at': model.composition_json.get('created_at'), 'updated_at': model.last_updated}

    async def upsert_family_composition(self, payload: dict) -> None:
        family_id = payload['family_id']
        if not isinstance(family_id, UUID):
            family_id = UUID(str(family_id))
        model = await self._session.get(FamilyCompositionViewModel, family_id)
        if model is None:
            model = FamilyCompositionViewModel(family_id=family_id, head_citizen_id=payload['head_citizen_id'], head_name=payload.get('head_name', ''), member_count=int(payload.get('member_count', 0)), dependents_count=int(payload.get('dependents_count', 0)), active_relationships=int(payload.get('active_relationships', 0)), composition_json=payload)
            self._session.add(model)
        else:
            model.head_citizen_id = payload['head_citizen_id']
            model.head_name = payload.get('head_name', '')
            model.member_count = int(payload.get('member_count', 0))
            model.dependents_count = int(payload.get('dependents_count', 0))
            model.active_relationships = int(payload.get('active_relationships', 0))
            model.composition_json = payload