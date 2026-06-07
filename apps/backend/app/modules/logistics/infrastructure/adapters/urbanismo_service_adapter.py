from __future__ import annotations

from apps.backend.app.modules.logistics.domain.ports.urbanismo_service_port import (
    UrbanismoServicePort,
)


class UrbanismoServiceAdapter(UrbanismoServicePort):
    async def validar_zoneamento_rota(self, origem: str, destino: str) -> bool:
        return bool(origem.strip() and destino.strip())
