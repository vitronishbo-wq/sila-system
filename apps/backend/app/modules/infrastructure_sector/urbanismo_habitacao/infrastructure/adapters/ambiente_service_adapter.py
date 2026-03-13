from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.ambiente_service_port import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    async def validar_licenca_ambiental(self, referencia_id: UUID) -> bool:
        return True