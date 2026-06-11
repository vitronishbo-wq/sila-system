from __future__ import annotations

import asyncio
from typing import Any


class MockAdapter:
    """Simple mock adapter that simulates external system calls.

    Methods are intentionally permissive: they accept keyword args and return
    deterministic mock responses. Replace with HttpAdapter/SoapAdapter later.
    """

    async def call(self, method: str, **kwargs: Any) -> dict[str, Any]:
        await asyncio.sleep(0.01)
        return {"status": "ok", "method": method, "result": kwargs}
