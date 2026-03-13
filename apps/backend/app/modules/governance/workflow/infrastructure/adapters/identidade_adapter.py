from __future__ import annotations
from typing import Any
from uuid import UUID
from apps.backend.app.domain.bridges import CitizenRepositoryPort
from apps.backend.app.modules.governance.workflow.application.ports.identidade_adapter_port import IdentidadeAdapterPort

class IdentidadeAdapter(IdentidadeAdapterPort):

    def __init__(self, citizen_repo: CitizenRepositoryPort):
        self._citizen_repo = citizen_repo

    async def validar_cidadao_ativo(self, citizen_id: UUID) -> bool:
        citizen = await self._citizen_repo.get_by_id(citizen_id)
        if citizen is None:
            return False
        if getattr(citizen, 'is_active', True) is False:
            return False
        vital_status = getattr(citizen, 'vital_status', None)
        if isinstance(vital_status, str) and vital_status.lower() in {'inactive', 'deceased'}:
            return False
        return True

    async def get_cidadao(self, citizen_id: UUID) -> Any | None:
        return await self._citizen_repo.get_by_id(citizen_id)