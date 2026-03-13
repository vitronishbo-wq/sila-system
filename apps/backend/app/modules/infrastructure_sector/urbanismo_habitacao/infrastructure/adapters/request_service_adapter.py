from __future__ import annotations
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.request_service_port import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    async def create(self, payload: dict) -> str:
        return 'REQ-PENDING'