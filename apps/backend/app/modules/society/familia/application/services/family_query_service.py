from __future__ import annotations
from fastapi import HTTPException, status
from app.modules.society.familia.application.ports.family_aggregate_repository_port import FamilyAggregateRepositoryPort
from app.modules.society.familia.application.ports.projection_repository_port import ProjectionRepositoryPort
from app.modules.society.familia.application.ports.citizen_service_port import CitizenServicePort
from app.modules.society.familia.domain.enums import MemberRole

class FamilyQueryService:

    def __init__(self, *, repository: FamilyAggregateRepositoryPort, projection_repository: ProjectionRepositoryPort, citizen_service: CitizenServicePort | None=None) -> None:
        self._repository = repository
        self._projection_repository = projection_repository
        self._citizen_service = citizen_service

    async def get_aggregate(self, family_id):
        projection = await self._projection_repository.get_family_composition(family_id)
        if projection:
            return projection
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}

    async def get_family_tree(self, family_id):
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        members = []
        for m in aggregate.all_members:
            citizen_name = None
            if self._citizen_service:
                try:
                    citizen = await self._citizen_service.get_citizen(m.citizen_id)
                    citizen_name = citizen.get('full_name') or citizen.get('name')
                except Exception:
                    citizen_name = None
            members.append({'citizen_id': m.citizen_id, 'role': m.role, 'joined_at': m.joined_at, 'left_at': m.left_at, 'is_active': m.left_at is None, 'citizen_name': citizen_name})
        dependents = [x for x in members if x['role'] == MemberRole.DEPENDENT and x['is_active']]
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at, 'members': members, 'dependents': dependents}

    async def get_active_family_for_citizen(self, citizen_id):
        family_id = await self._repository.find_active_family_for_citizen(citizen_id)
        if not family_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhuma familia ativa encontrada para o cidadao')
        return await self.get_aggregate(family_id)

    async def list_families_for_citizen(self, citizen_id, *, limit: int=100, offset: int=0) -> list[dict]:
        family_ids = await self._repository.list_family_ids_for_citizen(citizen_id, limit=limit, offset=offset)
        results: list[dict] = []
        for fid in family_ids:
            try:
                results.append(await self.get_aggregate(fid))
            except Exception:
                continue
        return results

    async def get_dependents_for_head(self, head_citizen_id):
        family_id = await self._repository.find_active_family_by_head(head_citizen_id)
        if not family_id:
            return {'citizen_id': head_citizen_id, 'dependents': [], 'count': 0}
        tree = await self.get_family_tree(family_id)
        return {'citizen_id': head_citizen_id, 'dependents': tree['dependents'], 'count': len(tree['dependents'])}