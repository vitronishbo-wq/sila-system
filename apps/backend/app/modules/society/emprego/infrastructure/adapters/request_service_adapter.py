from __future__ import annotations
from datetime import date
from typing import Any, Optional
from uuid import UUID
from apps.backend.app.domain.bridges import ServiceRequestLifecycleBridge
from apps.backend.app.modules.society.emprego.application.ports import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    def __init__(self, bridge: ServiceRequestLifecycleBridge):
        self.bridge = bridge

    async def create_request(self, *, request_type: str, entity_id: UUID, citizen_id: UUID, numero_processo: str, metadata: dict[str, Any] | None=None) -> Optional[UUID]:
        return await self.bridge.create_education_request(entity_id=entity_id, citizen_id=citizen_id, numero_processo=numero_processo, escola_nome=f'Emprego/{request_type}', ano_letivo=str(date.today().year))

    async def complete_request(self, *, entity_id: UUID, actor_id: UUID, metadata: dict[str, Any] | None=None) -> bool:
        return await self.bridge.mark_education_request_completed(entity_id=entity_id, actor_id=actor_id, metadata=metadata)