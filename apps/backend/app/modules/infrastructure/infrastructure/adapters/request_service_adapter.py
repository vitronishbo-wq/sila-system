from __future__ import annotations

from apps.backend.app.modules.infrastructure.application.ports.request_service_port import (
    RequestServicePort,
)


class RequestServiceAdapter(RequestServicePort):
    async def create(self, payload: dict) -> str:
        return "REQ-PENDING"
