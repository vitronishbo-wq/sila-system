from __future__ import annotations

from typing import Any
from .mock_adapter import MockAdapter


class TaxAuthorityMockAdapter(MockAdapter):
    async def validate_nif(self, nif: str) -> dict[str, Any]:
        return await self.call("validate_nif", nif=nif)
