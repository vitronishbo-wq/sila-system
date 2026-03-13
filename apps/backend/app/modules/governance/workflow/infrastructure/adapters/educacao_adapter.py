from __future__ import annotations
from typing import Any
from uuid import UUID
from apps.backend.app.modules.governance.workflow.application.ports.educacao_adapter_port import EducacaoAdapterPort

class EducacaoAdapter(EducacaoAdapterPort):

    def __init__(self, matricula_repo: Any, turma_repo: Any):
        self._matricula_repo = matricula_repo
        self._turma_repo = turma_repo

    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        matriculas = await self._matricula_repo.get_by_citizen(citizen_id)
        ativos = {'pendente', 'ativa', 'pending', 'active', 'confirmed', 'aprovada'}
        return any((str(getattr(item.status, 'value', item.status)).lower() in ativos for item in matriculas))

    async def validar_disponibilidade_vaga(self, *, turma_id: UUID, ano_letivo_id: UUID) -> bool:
        turma = await self._turma_repo.get_by_id(turma_id)
        if turma is None or not turma.ativa:
            return False
        if turma.ano_letivo_id != ano_letivo_id:
            return False
        ocupacao = await self._turma_repo.count_matriculas_ativas(turma_id=turma_id, ano_letivo_id=ano_letivo_id)
        return ocupacao < turma.capacidade