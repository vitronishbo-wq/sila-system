from __future__ import annotations
from typing import Any
from uuid import UUID
from apps.backend.app.modules.governance.workflow.application.ports.emprego_adapter_port import EmpregoAdapterPort

class EmpregoAdapter(EmpregoAdapterPort):

    def __init__(self, candidato_repo: Any):
        self._candidato_repo = candidato_repo

    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        status = str(getattr(getattr(candidato, 'status', None), 'value', getattr(candidato, 'status', ''))).lower()
        return bool(candidato and status in {'ativo', 'active'})

    async def get_status_candidato(self, citizen_id: UUID) -> str | None:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        return candidato.status.value if candidato else None