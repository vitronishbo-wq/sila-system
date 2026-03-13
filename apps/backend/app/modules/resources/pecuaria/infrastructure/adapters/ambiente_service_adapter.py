from __future__ import annotations
from uuid import UUID
from app.modules.resources.pecuaria.application.ports.ambiente_service_port import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    def __init__(self, service: AmbienteServicePort):
        self._service = service

    async def possui_licenciamento_ativo(self, propriedade_id: UUID) -> bool:
        return await self._service.possui_licenciamento_ativo(propriedade_id)