from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure.application.ports.ambiente_service_port import AmbienteServicePort

class AmbienteServiceAdapter(AmbienteServicePort):

    async def validar_licenca_ambiental(self, obra_id: UUID) -> bool:
        return True
