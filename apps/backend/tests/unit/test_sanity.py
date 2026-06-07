"""Sanity tests - VERIFICAÇÃO ZERO DÍVIDA"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_imports():
    from apps.backend.app.core.db import AsyncSessionLocal, Base, importAsyncSessionLocal
    from apps.backend.app.core.events import get_event_bus
    from core.security import IAMClient

    assert all([Base, AsyncSessionLocal, importAsyncSessionLocal, IAMClient, get_event_bus()])
    print("✅ All imports OK")


def test_iam():
    import asyncio

    from core.security import IAMClient

    async def test():
        user = await IAMClient().get_current_user("test")
        assert user is not None

    asyncio.run(test())
    print("✅ IAM OK")


def test_events():
    import asyncio

    from apps.backend.app.core.events import get_event_bus

    async def test():
        bus = get_event_bus()
        received = []
        await bus.subscribe("test", lambda e: received.append(e))
        await bus.publish("test", {"ok": True})
        assert len(received) == 1

    asyncio.run(test())
    print("✅ Events OK")


if __name__ == "__main__":
    test_imports()
    test_iam()
    test_events()
    print("\n✅ ZERO DÍVIDA - ALL OK")
