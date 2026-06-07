from __future__ import annotations

from decimal import Decimal

from apps.backend.app.modules.resources.aguas_saneamento.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)


class GeosampaServiceAdapter(GeosampaServicePort):
    async def validar_coordenadas(self, latitude: Decimal, longitude: Decimal) -> bool:
        return Decimal("-90") <= latitude <= Decimal("90") and Decimal(
            "-180"
        ) <= longitude <= Decimal("180")
