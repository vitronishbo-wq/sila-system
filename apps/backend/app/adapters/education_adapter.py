from __future__ import annotations

from typing import Any
from .mock_adapter import MockAdapter


class EducationMockAdapter(MockAdapter):
    async def validate_school(self, school_id: str) -> dict[str, Any]:
        return await self.call("validate_school", school_id=school_id)
