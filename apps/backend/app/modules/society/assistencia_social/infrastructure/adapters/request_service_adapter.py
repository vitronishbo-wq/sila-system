from __future__ import annotations
from datetime import date
from typing import Any
from uuid import UUID
from apps.backend.app.core.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.society.assistencia_social.application.ports import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    def __init__(self, bridge: ServiceRequestLifecycleBridge):
        self._bridge = bridge

    async def create_request(self, *, request_type: str, entity_id: UUID, citizen_id: UUID, numero_processo: str, metadata: dict[str, Any] | None=None) -> UUID | None:
        _ = metadata
        return await self._bridge.create_education_request(entity_id=entity_id, citizen_id=citizen_id, numero_processo=numero_processo, escola_nome=f'AssistenciaSocial/{request_type}', ano_letivo=str(date.today().year))