"""Sanity tests - VERIFICAÇÃO ZERO DÍVIDA"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_imports():
    from app.core.db import Base, AsyncSessionLocal, importAsyncSessionLocal
    from app.core.security import IAMClient
    from app.core.events import get_event_bus
    assert all([Base, AsyncSessionLocal, importAsyncSessionLocal, IAMClient, get_event_bus()])
    print("✅ All imports OK")

def test_iam():
    from app.core.security import IAMClient
    import asyncio
    async def test():
        user = await IAMClient().get_current_user("test")
        assert user is not None
    asyncio.run(test())
    print("✅ IAM OK")

def test_events():
    from app.core.events import get_event_bus
    import asyncio
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
