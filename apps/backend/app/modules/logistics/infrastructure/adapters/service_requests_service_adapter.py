from __future__ import annotations

from apps.backend.app.modules.logistics.domain.ports.service_requests_service_port import (
    ServiceRequestsServicePort,
)


class ServiceRequestsServiceAdapter(ServiceRequestsServicePort):
    async def abrir_solicitacao(self, payload: dict) -> str:
        _ = payload
        return "SRQ-TRN-PENDING"
