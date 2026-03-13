from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.justice.bounded_contexts.infrastructure.models.cemetery_inspection_model import CemeteryInspectionRecord

class CemeteryInspectionRepository:

    def __init__(self, session: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.session = session

    async def save(self, record: CemeteryInspectionRecord):
        self.session.add(record)
        await self.session.commit()