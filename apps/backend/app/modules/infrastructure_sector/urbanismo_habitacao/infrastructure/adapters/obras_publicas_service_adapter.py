from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.obras_publicas_service_port import ObrasPublicasServicePort

class ObrasPublicasServiceAdapter(ObrasPublicasServicePort):

    async def validar_obra(self, obra_id: UUID) -> bool:
        return True