from __future__ import annotations
from uuid import UUID
from app.modules.resources.pecuaria.application.ports.agricultura_service_port import AgriculturaServicePort

class AgriculturaServiceAdapter(AgriculturaServicePort):

    def __init__(self, service: AgriculturaServicePort):
        self._service = service

    async def propriedade_existe(self, propriedade_id: UUID) -> bool:
        return await self._service.propriedade_existe(propriedade_id)