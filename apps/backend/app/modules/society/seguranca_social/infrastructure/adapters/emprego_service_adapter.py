from __future__ import annotations
from uuid import UUID
from app.core.bridges.emprego_bridge import CandidatoRepositoryPort
from apps.backend.app.modules.society.seguranca_social.application.ports import EmpregoServicePort

class EmpregoServiceAdapter(EmpregoServicePort):
    """Reuse emprego repository to validate desempregado eligibility."""

    def __init__(self, candidato_repo: CandidatoRepositoryPort):
        self.candidato_repo = candidato_repo

    async def is_candidato_registrado(self, citizen_id: UUID) -> bool:
        candidato = await self.candidato_repo.get_by_citizen(citizen_id)
        return candidato is not None