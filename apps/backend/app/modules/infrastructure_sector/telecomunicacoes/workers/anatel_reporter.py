from __future__ import annotations

import asyncio


async def run_reporter(*, interval_seconds: float = 60.0) -> None:
    while True:
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(run_reporter())
