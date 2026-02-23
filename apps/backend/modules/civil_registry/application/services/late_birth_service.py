from app.modules.registo_civil.infrastructure.repositories.civil_event_repository import CivilEventRepository
from app.modules.registo_civil.integrations.fuc_client import FUCClient
from app.modules.registo_civil.domain.models.civil_event import CivilEventRecord

class LateBirthService:
    def __init__(self, repo: CivilEventRepository, fuc: FUCClient, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.repo = repo
        self.fuc = fuc

    async def register(self, data: dict):
        citizen_id = await self.fuc.create_or_link(data)
        event = CivilEventRecord(
            citizen_id=citizen_id,
            event_type="birth_late_registered",
            payload=data
        )
        await self.repo.save(event)
        return {"success": True, "citizen_id": citizen_id}
