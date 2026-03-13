from __future__ import annotations
from uuid import UUID
from app.modules.resources.pescas.application.ports import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    def __init__(self, service: AmbienteServicePort):
        self._service = service

    async def possui_licenciamento_ativo(self, embarcacao_id: UUID) -> bool:
        return await self._service.possui_licenciamento_ativo(embarcacao_id)