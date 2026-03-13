import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from uuid import uuid4
from apps.backend.app.modules.society.familia.api.router import router as familia_router
from apps.backend.app.modules.society.familia.api.deps import get_family_aggregate_service, get_family_query_service
from apps.backend.app.modules.society.familia.application.services.family_aggregate_service import FamilyAggregateService
from apps.backend.app.modules.society.familia.application.services.family_query_service import FamilyQueryService
from apps.backend.app.modules.society.familia.domain.enums import MemberRole
from apps.backend.app.modules.society.familia.tests._fakes import InMemoryFamilyRepository, InMemoryOutbox, NoopBus

class FakeCitizenService:

    def __init__(self, citizens: dict) -> None:
        self._citizens = citizens

    async def get_citizen(self, citizen_id):
        data = self._citizens.get(citizen_id)
        if not data:
            raise ValueError('Cidadao nao encontrado')
        return {'citizen_id': str(citizen_id), **data}

    async def verify_civil_capacity(self, citizen_id):
        data = await self.get_citizen(citizen_id)
        return data.get('is_active', True) and data.get('age', 0) >= 18 and (str(data.get('vital_status', 'alive')).lower() in {'alive', 'active'})

class FakeCivilRegistryService:

    async def has_active_marriage(self, citizen_id):
        _ = citizen_id
        return False

    async def is_deceased(self, citizen_id):
        _ = citizen_id
        return False

    async def relationship_exists(self, citizen_a_id, citizen_b_id):
        _ = (citizen_a_id, citizen_b_id)
        return False

class NoopProjectionRepository:

    async def get_family_composition(self, family_id):
        _ = family_id
        return None

    async def upsert_family_composition(self, payload: dict) -> None:
        _ = payload

@pytest.mark.asyncio
async def test_family_lifecycle_e2e():
    repo = InMemoryFamilyRepository()
    outbox = InMemoryOutbox()
    bus = NoopBus()
    head_id = uuid4()
    spouse_id = uuid4()
    child_id = uuid4()
    citizens = {head_id: {'full_name': 'Joao Silva', 'age': 35, 'is_active': True, 'vital_status': 'alive'}, spouse_id: {'full_name': 'Maria Silva', 'age': 32, 'is_active': True, 'vital_status': 'alive'}, child_id: {'full_name': 'Pedro Silva', 'age': 8, 'is_active': True, 'vital_status': 'alive'}}
    citizen_service = FakeCitizenService(citizens)
    civil_registry_service = FakeCivilRegistryService()

    async def _get_aggregate_service():
        return FamilyAggregateService(repository=repo, outbox_repository=outbox, event_bus=bus, citizen_service=citizen_service, civil_registry_service=civil_registry_service)

    async def _get_query_service():
        return FamilyQueryService(repository=repo, projection_repository=NoopProjectionRepository(), citizen_service=citizen_service)
    app = FastAPI()
    app.include_router(familia_router, prefix='/v1')
    app.dependency_overrides[get_family_aggregate_service] = _get_aggregate_service
    app.dependency_overrides[get_family_query_service] = _get_query_service
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        create_payload = {'head_citizen_id': str(head_id), 'members': [{'citizen_id': str(spouse_id), 'role': 'MEMBER'}], 'metadata': {'jurisdiction_code': 'AO-LUA'}}
        resp = await ac.post('/v1/familia/families', json=create_payload)
        assert resp.status_code == 201, resp.text
        data = resp.json()
        family_id = data['id']
        assert data['head_citizen_id'] == str(head_id)
        assert data['member_count'] == 2
        resp = await ac.post(f'/v1/familia/families/{family_id}/members', json={'citizen_id': str(child_id), 'role': 'DEPENDENT'})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data['member_count'] == 3
        resp = await ac.get(f'/v1/familia/families/{family_id}/tree')
        assert resp.status_code == 200, resp.text
        tree = resp.json()
        assert tree['status'] == 'ACTIVE'
        assert len(tree['members']) == 3
        assert len(tree['dependents']) == 1
        assert tree['dependents'][0]['citizen_name'] == 'Pedro Silva'
        resp = await ac.get(f'/v1/familia/families/citizen/{head_id}/dependents')
        assert resp.status_code == 200, resp.text
        deps = resp.json()
        assert deps['count'] == 1
        resp = await ac.put(f'/v1/familia/families/{family_id}/transfer-head', json={'new_head_citizen_id': str(spouse_id)})
        assert resp.status_code == 200, resp.text
        transferred = resp.json()
        assert transferred['head_citizen_id'] == str(spouse_id)
        resp = await ac.request('DELETE', f'/v1/familia/families/{family_id}', json={'reason': 'divorce'})
        assert resp.status_code == 200, resp.text
        dissolved = resp.json()
        assert dissolved['status'] == 'DISSOLVED'
        resp = await ac.get(f'/v1/familia/families/{family_id}/tree')
        assert resp.status_code == 200, resp.text
        tree2 = resp.json()
        assert tree2['status'] == 'DISSOLVED'
        assert all((m['is_active'] is False for m in tree2['members']))
    app.dependency_overrides.clear()