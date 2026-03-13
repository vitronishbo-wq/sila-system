from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.justice.bounded_contexts.application.ports.emprego_service_port import EmpregoServicePort

class EmpregoServiceAdapter(EmpregoServicePort):

    def __init__(self, candidato_repo: Any):
        self._candidato_repo = candidato_repo

    async def get_candidatura(self, citizen_id: UUID) -> dict[str, Any] | None:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        if candidato is None:
            return None
        return {'id': str(candidato.id), 'numero_processo': candidato.numero_processo, 'status': candidato.status.value, 'situacao': candidato.situacao.value, 'escolaridade': candidato.escolaridade.value, 'areas_interesse': candidato.areas_interesse, 'observacoes': candidato.observacoes}

    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        if candidato is None:
            return False
        status = str(getattr(candidato.status, 'value', candidato.status)).lower()
        return status == 'ativo'