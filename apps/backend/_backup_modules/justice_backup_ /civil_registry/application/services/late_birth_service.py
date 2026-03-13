from ..ports.platform_shared_ports import trace
from apps.backend.app.modules.justice.bounded_contexts.infrastructure.repositories.civil_event_repository import CivilEventRepository
from apps.backend.app.modules.justice.bounded_contexts.integrations.fuc_client import FUCClient
from apps.backend.app.modules.justice.bounded_contexts.infrastructure.models.civil_event import CivilEventRecord

class LateBirthService:

    def __init__(self, repo: CivilEventRepository, fuc: FUCClient, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.repo = repo
        self.fuc = fuc

    @trace()
    async def register(self, data: dict):
        citizen_id = await self.fuc.create_or_link(data)
        event = CivilEventRecord(citizen_id=citizen_id, event_type='birth_late_registered', payload=data)
        await self.repo.save(event)
        return {'success': True, 'citizen_id': citizen_id}