from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.wallet.models import Document

async def get_documents(citizen_id: str, session: AsyncSession) -> list[Document]:
    result = await session.execute(select(Document).where(Document.citizen_id == citizen_id))
    return list(result.scalars().all())
__all__ = ['get_documents']