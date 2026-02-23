from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.registo_civil.application.ports.marriage_repository_port import MarriageRepositoryPort
from app.modules.registo_civil.domain.models.marriage_record import MarriageRecord

class MarriageRepository(MarriageRepositoryPort):
    def __init__(self, session: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.session = session

    async def save(self, marriage: MarriageRecord) -> MarriageRecord:
        self.session.add(marriage)
        await self.session.commit()
        await self.session.refresh(marriage)
        return marriage

    async def get_by_id(self, marriage_id: str) -> Optional[MarriageRecord]:
        result = await self.session.execute(
            select(MarriageRecord).where(MarriageRecord.id == marriage_id)
        )
        return result.scalars().first()

    async def list_by_spouse(self, citizen_id: str) -> List[MarriageRecord]:
        result = await self.session.execute(
            select(MarriageRecord).where(
                or_(
                    MarriageRecord.spouse1_id == citizen_id,
                    MarriageRecord.spouse2_id == citizen_id
                )
            )
        )
        return list(result.scalars().all())
