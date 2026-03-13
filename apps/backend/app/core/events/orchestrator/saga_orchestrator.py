from __future__ import annotations
from typing import Any
from app.core.events.saga.saga_registry import SagaRegistry

class SagaOrchestrator:

    async def process(self, event: Any) -> None:
        sagas = SagaRegistry.get_sagas()
        for saga in sagas:
            await saga.handle(event)