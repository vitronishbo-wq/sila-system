from __future__ import annotations
import inspect
from uuid import UUID
from apps.backend.app.modules.resources.pescas.industrial.application.ports.pescas_service_port import PescasServicePort

class PescasServiceAdapter(PescasServicePort):

    def __init__(self, service):
        self._service = service

    async def armador_exists(self, armador_id: UUID) -> bool:
        obter = getattr(self._service, 'obter_armador', None)
        if callable(obter):
            try:
                result = obter(armador_id)
                if inspect.isawaitable(result):
                    await result
                return True
            except Exception:
                return False
        get_by_id = getattr(self._service, 'get_by_id', None)
        if callable(get_by_id):
            result = get_by_id(armador_id)
            if inspect.isawaitable(result):
                result = await result
            return result is not None
        return True