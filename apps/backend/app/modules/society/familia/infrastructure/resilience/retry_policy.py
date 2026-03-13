import asyncio

async def retry(coro, attempts: int=3):
    last_exc = None
    for _ in range(attempts):
        try:
            return await coro()
        except Exception as exc:
            last_exc = exc
            await asyncio.sleep(0)
    raise last_exc