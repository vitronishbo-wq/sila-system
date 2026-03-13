from __future__ import annotations
from typing import Any
from uuid import UUID
from apps.backend.app.modules.justice.bounded_contexts.application.ports.educacao_service_port import EducacaoServicePort

class EducacaoServiceAdapter(EducacaoServicePort):

    def __init__(self, matricula_repo: Any):
        self._matricula_repo = matricula_repo

    async def get_matriculas_ativas(self, citizen_id: UUID) -> list[dict[str, Any]]:
        matriculas = await self._matricula_repo.get_by_citizen(citizen_id)
        ativos = []
        for item in matriculas:
            status = str(getattr(item.status, 'value', item.status)).lower()
            if status not in {'ativa', 'pendente'}:
                continue
            ativos.append({'id': str(item.id), 'numero_processo': item.numero_processo, 'escola_id': str(item.escola_id), 'turma_id': str(item.turma_id), 'ano_letivo_id': str(item.ano_letivo_id), 'status': status, 'data_matricula': item.data_matricula.isoformat()})
        return ativos

    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        matriculas = await self.get_matriculas_ativas(citizen_id)
        return bool(matriculas)