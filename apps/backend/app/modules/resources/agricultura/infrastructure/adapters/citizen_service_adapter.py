from __future__ import annotations

from uuid import UUID

from apps.backend.app.core.bridges import CitizenRepositoryPort
from apps.backend.app.modules.resources.agricultura.application.ports import CitizenServicePort


class CitizenServiceAdapter(CitizenServicePort):
    def __init__(self, citizen_repository: CitizenRepositoryPort):
        self._citizen_repository = citizen_repository

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        citizen = await self._citizen_repository.get_by_id(citizen_id)
        if citizen is None:
            return False
        if getattr(citizen, "is_active", True) is False:
            return False
        vital_status = getattr(citizen, "vital_status", None)
        if isinstance(vital_status, str) and vital_status.lower() in {"inactive", "deceased"}:
            return False
        return True
