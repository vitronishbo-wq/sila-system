from __future__ import annotations
from decimal import Decimal

class FinancasAdapter:
    """Adapter para integracao fiscal/tributaria."""

    async def registrar_fato_gerador(self, referencia: str, valor: Decimal) -> bool:
        _ = (referencia, valor)
        return True