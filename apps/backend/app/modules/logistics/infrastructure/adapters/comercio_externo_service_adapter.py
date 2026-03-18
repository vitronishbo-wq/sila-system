from __future__ import annotations
from apps.backend.app.modules.logistics.domain.ports.comercio_externo_service_port import ComercioExternoServicePort

class ComercioExternoServiceAdapter(ComercioExternoServicePort):

    async def validar_corredor_exportacao(self, codigo: str) -> bool:
        return bool(codigo.strip())