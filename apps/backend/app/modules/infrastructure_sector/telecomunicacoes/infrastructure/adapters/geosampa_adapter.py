from __future__ import annotations

class GeosampaAdapter:
    """Adapter para consulta de dados geoespaciais."""

    async def consultar_setor(self, latitude: float, longitude: float) -> dict[str, float]:
        return {'latitude': latitude, 'longitude': longitude}