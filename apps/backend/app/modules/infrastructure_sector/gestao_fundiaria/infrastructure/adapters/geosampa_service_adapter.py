from __future__ import annotations
from decimal import Decimal
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.geosampa_service_port import GeosampaServicePort

class GeosampaServiceAdapter(GeosampaServicePort):

    async def validar_coordenadas(self, latitude: Decimal, longitude: Decimal) -> bool:
        return True