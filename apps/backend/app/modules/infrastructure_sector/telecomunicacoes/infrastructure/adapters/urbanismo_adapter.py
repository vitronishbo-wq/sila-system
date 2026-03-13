from __future__ import annotations

class UrbanismoAdapter:
    """Adapter para regras de zoneamento urbano."""

    async def validar_zoneamento(self, zona_id: str) -> bool:
        _ = zona_id
        return True