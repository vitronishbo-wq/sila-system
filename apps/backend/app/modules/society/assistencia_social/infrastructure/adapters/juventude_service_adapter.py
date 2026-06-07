from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.assistencia_social.application.ports import (
    JuventudeServicePort,
)
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import (
    JovemRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import TipoVulnerabilidade


class JuventudeServiceAdapter(JuventudeServicePort):
    def __init__(self, jovem_repo: JovemRepositoryPort):
        self._jovem_repo = jovem_repo

    async def is_jovem_em_risco(self, citizen_id: UUID) -> bool:
        jovem = await self._jovem_repo.get_by_citizen(citizen_id)
        if jovem is None:
            return False
        vulnerabilidades = set(jovem.vulnerabilidades or [])
        sinais_criticos = {
            TipoVulnerabilidade.SITUACAO_RUA,
            TipoVulnerabilidade.VIOLENCIA_DOMESTICA,
            TipoVulnerabilidade.TRABALHO_INFANTIL,
            TipoVulnerabilidade.EXPLORACAO_SEXUAL,
            TipoVulnerabilidade.DEPENDENCIA_QUIMICA,
        }
        return bool(vulnerabilidades.intersection(sinais_criticos))
