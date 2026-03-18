from __future__ import annotations
from apps.backend.app.modules.logistics.domain.ports.obras_publicas_service_port import ObrasPublicasServicePort

class ObrasPublicasServiceAdapter(ObrasPublicasServicePort):

    async def validar_corredor(self, codigo_corredor: str) -> bool:
        return bool(codigo_corredor.strip())