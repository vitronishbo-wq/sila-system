from __future__ import annotations
from app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.geosampa_service_port import GeosampaServicePort

class GeosampaServiceAdapter(GeosampaServicePort):

    async def validar_coordenadas(self, latitude: float, longitude: float) -> bool:
        return True