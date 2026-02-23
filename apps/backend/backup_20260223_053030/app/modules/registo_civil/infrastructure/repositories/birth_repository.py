from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.registo_civil.application.ports.birth_repository_port import BirthRepositoryPort
from app.modules.registo_civil.domain.models.birth_record import BirthRecord

class BirthRepository(BirthRepositoryPort):
    def __init__(self, session: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.session = session

    async def save(self, birth: BirthRecord) -> BirthRecord:
        self.session.add(birth)
        await self.session.commit()
        await self.session.refresh(birth)
        return birth

    async def get_by_id(self, birth_id: str) -> Optional[BirthRecord]:
        result = await self.session.execute(
            select(BirthRecord).where(BirthRecord.id == birth_id)
        )
        return result.scalars().first()

    async def get_by_nub(self, nub: str) -> Optional[BirthRecord]:
        result = await self.session.execute(
            select(BirthRecord).where(BirthRecord.nub == nub)
        )
        return result.scalars().first()

    async def list_all(self, limit: int = 10, offset: int = 0) -> List[BirthRecord]:
        result = await self.session.execute(
            select(BirthRecord).offset(offset).limit(limit)
        )
        return list(result.scalars().all())
