from __future__ import annotations
from typing import Any
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.outbox_repository_port import OutboxRepositoryPort

class BaseOutboxRepository:
    """Commit atomico simplificado para repositorios in-memory/async."""

    def __init__(self, *, outbox_repo: OutboxRepositoryPort | None=None) -> None:
        self._outbox_repo = outbox_repo

    async def commit_with_event(self, *, persist: Any, event: Any | None=None) -> Any:
        saved = await persist
        if self._outbox_repo is not None and event is not None:
            await self._outbox_repo.enqueue(event)
        return saved