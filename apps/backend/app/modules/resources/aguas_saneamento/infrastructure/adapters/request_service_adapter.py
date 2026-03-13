from __future__ import annotations
from app.modules.resources.aguas_saneamento.application.ports.request_service_port import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    async def create(self, payload: dict) -> str:
        return f'REQ-{payload.get('numero_outorga', 'N/A')}'