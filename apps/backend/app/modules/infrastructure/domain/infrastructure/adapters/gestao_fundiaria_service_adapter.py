from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort

class GestaoFundiariaServiceAdapter(GestaoFundiariaServicePort):

    async def validar_imovel(self, imovel_id: UUID) -> bool:
        return True
