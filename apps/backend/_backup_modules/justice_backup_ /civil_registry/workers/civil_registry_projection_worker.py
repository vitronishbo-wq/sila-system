from __future__ import annotations
import asyncio
from typing import Any, AsyncIterator
from app.core.events.workers.projection_worker import ProjectionWorker
from app.modules.justice.bounded_contexts.projection.civil_registry_projector import CivilRegistryProjector

async def run_worker(session: Any, event_stream: AsyncIterator[Any]) -> None:
    projector = CivilRegistryProjector(session)
    worker = ProjectionWorker()
    worker.register_projection(projector.event_type, projector)
    async for event in event_stream:
        await worker.apply(event)

async def _no_stream() -> AsyncIterator[Any]:
    if False:
        yield None

def main() -> None:
    raise SystemExit('Event stream nao configurado. Use run_worker(session, event_stream) com um stream async de eventos do barramento/outbox.')
if __name__ == '__main__':
    main()