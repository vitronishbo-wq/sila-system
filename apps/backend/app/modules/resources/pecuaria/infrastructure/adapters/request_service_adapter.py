from __future__ import annotations
from datetime import date
from typing import Any
from uuid import UUID
from apps.backend.app.domain.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.resources.pecuaria.application.ports.request_service_port import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    def __init__(self, bridge: ServiceRequestLifecycleBridge):
        self._bridge = bridge

    async def create_request(self, *, request_type: str, entity_id: UUID, citizen_id: UUID, numero_processo: str, metadata: dict[str, Any] | None=None) -> UUID:
        return await self._bridge.create_education_request(entity_id=entity_id, citizen_id=citizen_id, numero_processo=numero_processo, escola_nome=f'Pecuaria/{request_type}', ano_letivo=str(date.today().year))

    async def complete_request(self, *, entity_id: UUID, actor_id: UUID, metadata: dict[str, Any] | None=None) -> bool:
        return await self._bridge.mark_education_request_completed(entity_id=entity_id, actor_id=actor_id, metadata=metadata)