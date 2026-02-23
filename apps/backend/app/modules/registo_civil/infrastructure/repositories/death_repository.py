from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.registo_civil.application.ports.death_repository_port import DeathRepositoryPort
from app.modules.registo_civil.domain.models.death_record import DeathRecord

class DeathRepository(DeathRepositoryPort):
    def __init__(self, session: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.session = session

    async def save(self, death: DeathRecord) -> DeathRecord:
        self.session.add(death)
        await self.session.commit()
        await self.session.refresh(death)
        return death

    async def get_by_id(self, death_id: str) -> Optional[DeathRecord]:
        result = await self.session.execute(
            select(DeathRecord).where(DeathRecord.id == death_id)
        )
        return result.scalars().first()

    async def get_by_citizen_id(self, citizen_id: str) -> Optional[DeathRecord]:
        result = await self.session.execute(
            select(DeathRecord).where(DeathRecord.citizen_id == citizen_id)
        )
        return result.scalars().first()
