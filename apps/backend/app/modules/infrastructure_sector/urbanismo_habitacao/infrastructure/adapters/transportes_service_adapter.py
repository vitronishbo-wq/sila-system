from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.transportes_service_port import TransportesServicePort

class TransportesServiceAdapter(TransportesServicePort):

    async def validar_impacto_viario(self, *, zoneamento_id: UUID, quantidade_lotes: int) -> bool:
        _ = zoneamento_id
        return quantidade_lotes <= 5000