from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.seguranca_social_service_port import SegurancaSocialServicePort

class SegurancaSocialServiceAdapter(SegurancaSocialServicePort):

    async def validar_cadastro_social(self, citizen_id: UUID) -> bool:
        return True