from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional
from app.core.workflow.models.request import Request

class RequestRepository:

    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = db

    async def create(self, request: Request) -> Request:
        self.db.add(request)
        await self.db.flush()
        return request

    async def get_by_id(self, request_id: UUID) -> Optional[Request]:
        result = await self.db.execute(select(Request).where(Request.id == request_id))
        return result.scalar_one_or_none()

    async def list_by_citizen(self, citizen_id: UUID) -> List[Request]:
        result = await self.db.execute(select(Request).where(Request.citizen_id == citizen_id).order_by(Request.created_at.desc()))
        return list(result.scalars().all())

    async def update_status(self, request_id: UUID, new_status: str) -> Optional[Request]:
        request = await self.get_by_id(request_id)
        if request:
            request.status = new_status
            await self.db.flush()
        return request