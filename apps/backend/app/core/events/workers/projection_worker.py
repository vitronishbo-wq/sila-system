"""Projection Worker - applies projections for incoming events."""

from apps.backend.app.core.events.projection.projection_manager import ProjectionManager


class ProjectionWorker:
    """Simple projection worker used for audit tests."""

    def __init__(self):
        self.running = False

    def register_projection(self, event_name: str, projection) -> None:
        ProjectionManager.register(event_name, projection)

    async def apply(self, event) -> None:
        await ProjectionManager.apply(event)

    async def start(self) -> None:
        self.running = True

    async def stop(self) -> None:
        self.running = False
