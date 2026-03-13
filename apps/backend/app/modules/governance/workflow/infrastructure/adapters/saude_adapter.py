from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.governance.workflow.application.ports.saude_adapter_port import SaudeAdapterPort

class SaudeAdapter(SaudeAdapterPort):

    def __init__(self, appointment_repo: Any):
        self._appointment_repo = appointment_repo

    async def has_atendimento_ativo(self, citizen_id: UUID) -> bool:
        atendimentos = await self._appointment_repo.get_by_citizen(citizen_id, skip=0, limit=200)
        ativos = {'pending', 'scheduled', 'confirmed', 'in_progress', 'rescheduled'}
        return any((str(getattr(atendimento.status, 'value', atendimento.status)).lower() in ativos for atendimento in atendimentos))

    async def count_atendimentos(self, citizen_id: UUID) -> int:
        atendimentos = await self._appointment_repo.get_by_citizen(citizen_id, skip=0, limit=200)
        return len(atendimentos)