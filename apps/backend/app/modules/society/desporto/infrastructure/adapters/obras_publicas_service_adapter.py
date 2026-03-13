from __future__ import annotations
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import ObrasPublicasServicePort

class ObrasPublicasServiceAdapter(ObrasPublicasServicePort):

    def __init__(self, obra_service):
        self._obra_service = obra_service

    async def obra_exists(self, codigo_obra: str) -> bool:
        try:
            await self._obra_service.obter_por_codigo(codigo_obra.strip())
            return True
        except Exception:
            return False