"""
Repositório de Cidadãos - Módulo Identidade Civil (Baseado no Modelo Único FUC)
"""
import uuid
import logging
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.citizen.core.models import CitizenFUC

logger = logging.getLogger("identidade_civil.repository.citizen")

class CitizenRepository:
    """Repositório assíncrono para entidade CitizenFUC (Modelo Único)."""

    def __init__(self, session: AsyncSession, **kwargs):
        self.session = session

    async def create(self, citizen: CitizenFUC) -> CitizenFUC:
        """Persiste um novo cidadão (FUC)."""
        self.session.add(citizen)
        await self.session.commit()
        await self.session.refresh(citizen)
        logger.info("Citizen created", extra={"citizen_id": str(citizen.citizen_id)})
        return citizen

    async def get_by_id(self, citizen_id: uuid.UUID) -> Optional[CitizenFUC]:
        """Recupera cidadão por ID (UUID)."""
        result = await self.session.execute(
            select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id)
        )
        return result.scalar_one_or_none()

    async def get_by_bi(self, bi_number: str) -> Optional[CitizenFUC]:
        """Recupera cidadão por número de BI (document_number)."""
        result = await self.session.execute(
            select(CitizenFUC).where(CitizenFUC.document_number == bi_number)
        )
        return result.scalar_one_or_none()

    async def update(self, citizen: CitizenFUC) -> CitizenFUC:
        """Atualiza dados do cidadão."""
        await self.session.commit()
        await self.session.refresh(citizen)
        logger.info("Citizen updated", extra={"citizen_id": str(citizen.citizen_id)})
        return citizen

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[CitizenFUC]:
        """Lista cidadãos com paginação."""
        result = await self.session.execute(
            select(CitizenFUC).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def search_by_name(self, name: str, limit: int = 50) -> List[CitizenFUC]:
        """Busca cidadãos por nome (parcial, case-insensitive)."""
        result = await self.session.execute(
            select(CitizenFUC)
            .where(CitizenFUC.full_name.ilike(f"%{name}%"))
            .limit(limit)
        )
        return list(result.scalars().all())
