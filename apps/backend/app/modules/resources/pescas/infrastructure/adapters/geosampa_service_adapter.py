from __future__ import annotations
from uuid import UUID
from app.modules.resources.pescas.application.ports import GeosampaServicePort

class GeosampaServiceAdapter(GeosampaServicePort):

    def __init__(self, service: GeosampaServicePort):
        self._service = service

    async def validar_zona_pesca(self, zona_pesca_id: UUID) -> bool:
        return await self._service.validar_zona_pesca(zona_pesca_id)