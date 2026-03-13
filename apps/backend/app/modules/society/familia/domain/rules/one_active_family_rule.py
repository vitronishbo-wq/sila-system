from __future__ import annotations
from uuid import UUID
from app.modules.society.familia.domain.exceptions.family_exceptions import CitizenAlreadyInActiveFamilyError

class OneActiveFamilyRule:

    async def validate(self, *, citizen_id: UUID, family_repository, exclude_family_id: UUID | None=None) -> bool:
        existing = await family_repository.find_active_family_for_citizen(citizen_id, exclude_family_id)
        if existing:
            raise CitizenAlreadyInActiveFamilyError(citizen_id, existing)
        return True