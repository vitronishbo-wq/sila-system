from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.core.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.infrastructure_sector.meteorologia.application.ports.request_service_port import (
    RequestServicePort,
)


class RequestServiceAdapter(RequestServicePort):
    def __init__(self, bridge: ServiceRequestLifecycleBridge):
        self._bridge = bridge

    async def criar_request(self, request_data: dict) -> bool:
        citizen_id = request_data.get("citizen_id")
        if not citizen_id:
            return True
        try:
            entity_id = request_data.get("entity_id") or uuid4()
            if isinstance(entity_id, str):
                entity_id = UUID(entity_id)
            elif not isinstance(entity_id, UUID):
                entity_id = UUID(str(entity_id))
            if isinstance(citizen_id, str):
                citizen_id = UUID(citizen_id)
            elif not isinstance(citizen_id, UUID):
                citizen_id = UUID(str(citizen_id))
        except (ValueError, TypeError):
            return False
        numero_processo = (
            request_data.get("numero_processo") or f"MET-{date.today().year}-{str(entity_id)[:8]}"
        )
        modulo_origem = request_data.get("tipo") or "METEOROLOGIA"
        await self._bridge.create_education_request(
            entity_id=entity_id,
            citizen_id=citizen_id,
            numero_processo=numero_processo,
            escola_nome=f"Alertas/{modulo_origem}",
            ano_letivo=str(date.today().year),
        )
        return True
