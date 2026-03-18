from __future__ import annotations
from apps.backend.app.modules.logistics.domain.ports.geosampa_service_port import GeosampaServicePort

class GeosampaServiceAdapter(GeosampaServicePort):

    async def rota_valida(self, itinerario: list[dict]) -> bool:
        return bool(itinerario)