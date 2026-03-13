from __future__ import annotations
from uuid import UUID
from app.modules.logistics.application.ports.request_service_port import RequestServicePort

class RequestServiceAdapter(RequestServicePort):

    async def create_transport_request(self, *, entity_id: UUID, citizen_id: UUID, metadata: dict):
        _ = (citizen_id, metadata)
        return {'request_id': f'TRQ-{str(entity_id)[:8].upper()}'}
