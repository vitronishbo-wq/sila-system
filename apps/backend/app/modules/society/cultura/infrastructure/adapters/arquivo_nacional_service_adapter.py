from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.society.cultura.application.ports.arquivo_nacional_service_port import ArquivoNacionalServicePort

class ArquivoNacionalServiceAdapter(ArquivoNacionalServicePort):

    async def documento_exists(self, documento_id: UUID) -> bool:
        return False