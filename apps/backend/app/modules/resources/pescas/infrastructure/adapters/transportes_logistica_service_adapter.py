from __future__ import annotations
from apps.backend.app.modules.resources.pescas.application.ports import TransportesLogisticaServicePort

class TransportesLogisticaServiceAdapter(TransportesLogisticaServicePort):

    def __init__(self, service: TransportesLogisticaServicePort):
        self._service = service

    async def validar_cadeia_frio(self, lote_codigo: str) -> bool:
        return await self._service.validar_cadeia_frio(lote_codigo)