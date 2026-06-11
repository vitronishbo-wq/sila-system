from __future__ import annotations

from typing import Any
from .mock_adapter import MockAdapter


class SocialSecurityMockAdapter(MockAdapter):
    async def verify_ss_number(self, ss_number: str) -> dict[str, Any]:
        return await self.call("verify_ss", ss_number=ss_number)
