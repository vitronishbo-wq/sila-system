from __future__ import annotations

from typing import Any
from .mock_adapter import MockAdapter


class PaymentsMockAdapter(MockAdapter):
    async def create_payment(self, amount: float, reference: str | None = None) -> dict[str, Any]:
        return await self.call("create_payment", amount=amount, reference=reference)
