from __future__ import annotations
from typing import Any
from uuid import UUID
from app.modules.justice.bounded_contexts.application.ports.juventude_service_port import JuventudeServicePort

class JuventudeServiceAdapter(JuventudeServicePort):

    def __init__(self, jovem_repo: Any):
        self._jovem_repo = jovem_repo

    async def get_perfil_jovem(self, citizen_id: UUID) -> dict[str, Any] | None:
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        if jovem is None:
            return None
        return {'id': str(jovem.id), 'numero_registro': jovem.numero_registro, 'nome': jovem.nome, 'faixa_etaria': jovem.faixa_etaria.value, 'escolaridade': jovem.escolaridade.value, 'situacao_ocupacional': jovem.situacao_ocupacional.value, 'vulnerabilidades': [item.value for item in jovem.vulnerabilidades] if jovem.vulnerabilidades else [], 'ativo': jovem.ativo}

    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        if jovem is None:
            return False
        return bool(jovem.vulnerabilidades)