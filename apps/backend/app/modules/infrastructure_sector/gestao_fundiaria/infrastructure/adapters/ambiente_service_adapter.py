from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.ambiente_service_port import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    async def validar_car(self, imovel_id: UUID) -> bool:
        return True