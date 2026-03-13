from __future__ import annotations
from app.modules.logistics.application.ports.urbanismo_service_port import UrbanismoServicePort

class UrbanismoServiceAdapter(UrbanismoServicePort):

    async def validar_zoneamento_rota(self, origem: str, destino: str) -> bool:
        return bool(origem.strip() and destino.strip())
