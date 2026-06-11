from __future__ import annotations

from typing import Any
from .mock_adapter import MockAdapter


class CivilRegistryMockAdapter(MockAdapter):
    async def get_birth_record(self, citizen_id: str) -> dict[str, Any]:
        return await self.call("get_birth_record", citizen_id=citizen_id)
