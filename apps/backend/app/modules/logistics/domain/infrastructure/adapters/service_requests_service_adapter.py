from __future__ import annotations
from app.modules.logistics.application.ports.service_requests_service_port import ServiceRequestsServicePort

class ServiceRequestsServiceAdapter(ServiceRequestsServicePort):

    async def abrir_solicitacao(self, payload: dict) -> str:
        _ = payload
        return 'SRQ-TRN-PENDING'
