from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.aguas_saneamento_service_port import (
    AguasSaneamentoServicePort,
)


class AguasSaneamentoServiceAdapter(AguasSaneamentoServicePort):
    async def validar_capacidade_atendimento(
        self, *, zoneamento_id: UUID, quantidade_lotes: int
    ) -> bool:
        _ = zoneamento_id
        return quantidade_lotes <= 8000
