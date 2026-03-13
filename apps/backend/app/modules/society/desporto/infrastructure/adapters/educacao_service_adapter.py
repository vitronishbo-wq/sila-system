from __future__ import annotations
from uuid import UUID
from app.modules.society.desporto.application.ports.educacao_service_port import EducacaoServicePort

class EducacaoServiceAdapter(EducacaoServicePort):

    def __init__(self, escola_repo):
        self._escola_repo = escola_repo

    async def instituicao_exists(self, instituicao_id: UUID) -> bool:
        return await self._escola_repo.get_by_id(instituicao_id) is not None