from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.application.ports.citizen_service_port import (
    CitizenServicePort,
)


class CitizenServiceAdapter(CitizenServicePort):
    async def exists(self, citizen_id: UUID) -> bool:
        return True
