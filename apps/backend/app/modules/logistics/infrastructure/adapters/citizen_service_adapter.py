from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports.citizen_service_port import CitizenServicePort

class CitizenServiceAdapter(CitizenServicePort):

    async def get_by_id(self, citizen_id: UUID):
        return {'id': str(citizen_id), 'ativo': True}