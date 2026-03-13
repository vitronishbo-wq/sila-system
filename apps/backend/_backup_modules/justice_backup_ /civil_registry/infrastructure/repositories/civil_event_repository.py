from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.justice.bounded_contexts.infrastructure.models.civil_event import CivilEventRecord

class CivilEventRepository:

    def __init__(self, session: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.session = session

    async def save(self, event: CivilEventRecord):
        self.session.add(event)
        await self.session.commit()