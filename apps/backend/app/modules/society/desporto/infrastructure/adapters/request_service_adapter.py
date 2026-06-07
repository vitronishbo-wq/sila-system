from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from apps.backend.app.core.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)


class RequestServiceAdapter(RequestServicePort):
    def __init__(self, bridge: ServiceRequestLifecycleBridge):
        self._bridge = bridge

    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        metadata: dict[str, Any] | None = None,
        citizen_id: UUID | None = None,
        numero_processo: str | None = None,
    ) -> UUID | None:
        if citizen_id is None:
            return None
        return await self._bridge.create_education_request(
            entity_id=entity_id,
            citizen_id=citizen_id,
            numero_processo=numero_processo or str(entity_id),
            escola_nome=f"Desporto/{request_type}",
            ano_letivo=str(date.today().year),
        )
