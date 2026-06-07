from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.citizen_service_port import (
    CitizenServicePort,
)


class CitizenServiceAdapter(CitizenServicePort):
    async def exists(self, citizen_id: UUID) -> bool:
        return True
