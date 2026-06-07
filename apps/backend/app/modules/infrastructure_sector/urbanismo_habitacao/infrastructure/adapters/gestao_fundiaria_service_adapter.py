from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.gestao_fundiaria_service_port import (
    GestaoFundiariaServicePort,
)


class GestaoFundiariaServiceAdapter(GestaoFundiariaServicePort):
    async def validar_imovel(self, imovel_id: UUID) -> bool:
        return True
