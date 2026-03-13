from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.governance.workflow.application.ports.juventude_adapter_port import JuventudeAdapterPort

class JuventudeAdapter(JuventudeAdapterPort):

    def __init__(self, jovem_repo: Any):
        self._jovem_repo = jovem_repo

    async def has_jovem(self, citizen_id: UUID) -> bool:
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        return jovem is not None

    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        if jovem is None:
            return False
        vulnerabilidades = {str(getattr(item, 'value', item)).lower() for item in jovem.vulnerabilidades or []}
        sinais_criticos = {'situacao_rua', 'violencia_domestica', 'trabalho_infantil', 'exploracao_sexual', 'dependencia_quimica'}
        return bool(vulnerabilidades.intersection(sinais_criticos))