from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure.application.ports.justica_service_port import JusticaServicePort

class JusticaServiceAdapter(JusticaServicePort):

    async def possui_recurso_ativo(self, processo_id: UUID) -> bool:
        return False