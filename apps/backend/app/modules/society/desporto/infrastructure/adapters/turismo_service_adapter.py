from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.desporto.application.ports.turismo_service_port import (
    TurismoServicePort,
)


class TurismoServiceAdapter(TurismoServicePort):
    def __init__(self, atracao_service):
        self._atracao_service = atracao_service

    async def atracao_exists(self, atracao_id: UUID) -> bool:
        try:
            await self._atracao_service.obter(atracao_id)
            return True
        except Exception:
            return False
