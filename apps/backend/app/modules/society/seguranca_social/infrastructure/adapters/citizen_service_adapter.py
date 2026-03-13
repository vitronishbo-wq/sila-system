from __future__ import annotations
from typing import Optional
from uuid import UUID
from app.domain.bridges import CitizenRepository
from apps.backend.app.modules.society.seguranca_social.application.ports import CitizenServicePort

class CitizenServiceAdapter(CitizenServicePort):

    def __init__(self, repository: CitizenRepository):
        self.repository = repository

    async def get_citizen(self, citizen_id: UUID) -> Optional[object]:
        return await self.repository.get_by_id(citizen_id)

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        citizen = await self.repository.get_by_id(citizen_id)
        if not citizen:
            return False
        if hasattr(citizen, 'is_active'):
            return bool(citizen.is_active)
        return True