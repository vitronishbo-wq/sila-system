from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.agricultura_service_port import AgriculturaServicePort

class AgriculturaServiceAdapter(AgriculturaServicePort):

    async def validar_produtor(self, produtor_id: UUID) -> bool:
        return True