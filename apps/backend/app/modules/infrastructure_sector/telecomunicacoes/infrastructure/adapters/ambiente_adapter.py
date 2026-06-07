from __future__ import annotations


class AmbienteAdapter:
    """Adapter para verificacao de impacto ambiental."""

    async def validar_impacto(self, estudo_id: str) -> bool:
        _ = estudo_id
        return True
