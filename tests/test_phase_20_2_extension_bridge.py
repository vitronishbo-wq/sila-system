"""Phase 20.2 Extension Bridge - Audit tests."""

from app.core.events.bridge.event_bus_bridge import EventBusBridge, EventBusEnhanced
from app.core.events.workers.projection_worker import ProjectionWorker


def test_event_bus_bridge_init():
    bridge = EventBusBridge()
    assert bridge is not None
    assert callable(bridge.publish_atomic)


def test_event_bus_enhanced_init():
    bus = EventBusEnhanced()
    assert bus is not None
    assert callable(bus.publish)


def test_projection_worker_lifecycle():
    worker = ProjectionWorker()
    assert hasattr(worker, "start")
    assert hasattr(worker, "stop")
    assert hasattr(worker, "register_projection")
