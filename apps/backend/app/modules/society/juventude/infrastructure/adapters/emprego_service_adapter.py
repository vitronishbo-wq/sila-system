from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.emprego.application.ports.candidato_repository_port import (
    CandidatoRepositoryPort,
)
from apps.backend.app.modules.society.emprego.domain.enums import StatusCandidato
from apps.backend.app.modules.society.juventude.application.ports.emprego_service_port import (
    EmpregoServicePort,
)


class EmpregoServiceAdapter(EmpregoServicePort):
    def __init__(self, candidato_repo: CandidatoRepositoryPort):
        self._candidato_repo = candidato_repo

    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        candidato = await self._candidato_repo.get_by_citizen(citizen_id)
        if candidato is None:
            return False
        return candidato.status == StatusCandidato.ATIVO
