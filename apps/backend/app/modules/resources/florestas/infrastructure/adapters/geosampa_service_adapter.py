from __future__ import annotations
from typing import Any
from app.modules.resources.florestas.application.ports.geosampa_service_port import GeosampaServicePort

class GeosampaServiceAdapter(GeosampaServicePort):

    def __init__(self, dependency: object | None=None):
        self.dependency = dependency

    async def available(self) -> bool:
        return callable(getattr(self.dependency, 'get_all_provinces', None))

    async def integration_payload(self) -> dict[str, Any]:
        return {'provider': type(self.dependency).__name__ if self.dependency is not None else 'none', 'capability': 'base_geoespacial', 'supports_provincias': callable(getattr(self.dependency, 'get_all_provinces', None))}