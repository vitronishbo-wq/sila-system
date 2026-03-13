from __future__ import annotations
import logging
from typing import Any, Optional
from uuid import UUID
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.justice.bounded_contexts.civil_registry_core.application.ports.citizen_repository_port import (
    CitizenRepositoryPort,
)
from apps.backend.app.core.database.repositories import BaseRepository
from apps.backend.app.core.bridges.identity_bridge import CitizenFUC
logger = logging.getLogger('identity.repository.citizen')

class CitizenRepository(BaseRepository, CitizenRepositoryPort):
    """Canonical repository implementation for citizen records."""

    def __init__(self, session: AsyncSession, **kwargs):
        super().__init__(session)

    async def create(self, citizen: CitizenFUC, commit: bool=True) -> CitizenFUC:
        self.session.add(citizen)
        if commit:
            await self.session.commit()
            await self.session.refresh(citizen)
        else:
            await self.session.flush()
        logger.info('Citizen created', extra={'citizen_id': str(citizen.citizen_id)})
        return citizen

    async def add(self, citizen: CitizenFUC, commit: bool=True) -> CitizenFUC:
        """Legacy alias."""
        return await self.create(citizen, commit=commit)

    async def update(self, citizen: CitizenFUC, commit: bool=True) -> CitizenFUC:
        if commit:
            await self.session.commit()
            await self.session.refresh(citizen)
        else:
            await self.session.flush()
        logger.info('Citizen updated', extra={'citizen_id': str(citizen.citizen_id)})
        return citizen

    async def get_by_id(self, citizen_id: UUID) -> Optional[CitizenFUC]:
        result = await self.session.execute(select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id))
        return result.scalar_one_or_none()

    async def get_by_bi(self, bi_number: str) -> Optional[CitizenFUC]:
        result = await self.session.execute(text('\n                SELECT c.citizen_id\n                FROM citizen_fuc c\n                JOIN bi_records b ON c.citizen_id = b.citizen_fuc_id\n                WHERE b.bi_number = :bi\n                '), {'bi': bi_number})
        row = result.first()
        if row:
            return await self.get_by_id(row[0])
        legacy = await self.session.execute(select(CitizenFUC).where(CitizenFUC.document_number == bi_number))
        return legacy.scalar_one_or_none()

    async def get_by_national_id_number(self, national_id_number: str) -> Optional[CitizenFUC]:
        """Legacy alias for BI lookup."""
        return await self.get_by_bi(national_id_number)

    async def get_by_nif(self, nif: str) -> Optional[CitizenFUC]:
        if not hasattr(CitizenFUC, 'nif'):
            return None
        result = await self.session.execute(select(CitizenFUC).where(CitizenFUC.nif == nif))
        return result.scalar_one_or_none()

    async def list_all(self, limit: int=100, offset: int=0) -> list[CitizenFUC]:
        result = await self.session.execute(select(CitizenFUC).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def list(self, *, filters: dict, limit: int, offset: int) -> list[CitizenFUC]:
        query = select(CitizenFUC)
        for attr, value in (filters or {}).items():
            if value is None or not hasattr(CitizenFUC, attr):
                continue
            query = query.where(getattr(CitizenFUC, attr) == value)
        result = await self.session.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    async def search_by_name(self, name: str, limit: int=50) -> list[CitizenFUC]:
        result = await self.session.execute(select(CitizenFUC).where(CitizenFUC.full_name.ilike(f'%{name}%')).limit(limit))
        return list(result.scalars().all())

    async def soft_delete(self, citizen_id: UUID) -> None:
        citizen = await self.get_by_id(citizen_id)
        if not citizen:
            return
        if hasattr(citizen, 'vital_status'):
            citizen.vital_status = 'inactive'
        if hasattr(citizen, 'is_active'):
            citizen.is_active = False
        await self.session.commit()

    async def get(self, citizen_id: str) -> Optional[dict[str, Any]]:
        """Compatibility method for CitizenPort-style consumers."""
        try:
            target = UUID(str(citizen_id))
        except (ValueError, TypeError):
            return None
        citizen = await self.get_by_id(target)
        if not citizen:
            return None
        return citizen.to_dict() if hasattr(citizen, 'to_dict') else {'citizen_id': str(citizen.citizen_id)}
