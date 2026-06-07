from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class AnacomAdapter:
    """Gateway para a ANACOM (regulador europeu)."""

    async def enviar_relatorio(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return {"status": "not_configured", "payload": dict(payload)}
