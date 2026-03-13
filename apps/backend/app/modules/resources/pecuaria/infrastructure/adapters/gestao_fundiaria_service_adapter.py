from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.resources.pecuaria.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort

class GestaoFundiariaServiceAdapter(GestaoFundiariaServicePort):

    def __init__(self, service: GestaoFundiariaServicePort):
        self._service = service

    async def propriedade_existe(self, propriedade_id: UUID) -> bool:
        return await self._service.propriedade_existe(propriedade_id)