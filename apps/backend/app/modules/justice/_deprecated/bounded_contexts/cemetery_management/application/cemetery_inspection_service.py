from ..ports.platform_shared_ports import trace
from app.modules.justice.bounded_contexts.infrastructure.repositories.cemetery_inspection_repository import CemeteryInspectionRepository
from app.modules.justice.bounded_contexts.infrastructure.models.cemetery_inspection_model import CemeteryInspectionRecord

class CemeteryInspectionService:

    def __init__(self, repo: CemeteryInspectionRepository, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.repo = repo

    @trace()
    async def register_inspection(self, data: dict):
        record = CemeteryInspectionRecord(cemetery_name=data['cemetery_name'], inspector_id=data['inspector_id'], results=data['results'])
        await self.repo.save(record)
        return {'success': True, 'inspection_id': str(record.id)}