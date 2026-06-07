from __future__ import annotations

import asyncio
from typing import Any


async def invoke_async_method(
    target: object | None, method_name: str, *args: Any, **kwargs: Any
) -> tuple[bool, Any]:
    if target is None:
        return (False, None)
    method = getattr(target, method_name, None)
    if not callable(method):
        return (False, None)
    try:
        result = method(*args, **kwargs)
        if asyncio.iscoroutine(result):
            result = await result
        return (True, result)
    except Exception:
        return (False, None)
