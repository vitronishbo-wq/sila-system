from __future__ import annotations
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.infrastructure_sector.telecomunicacoes.application.ports.outbox_repository_port import OutboxRepositoryPort

class BaseRepositoryWithOutbox:

    def __init__(self, *, session: AsyncSession, outbox_repo: OutboxRepositoryPort | None=None) -> None:
        self.session = session
        self.outbox_repo = outbox_repo

    async def save_with_event(self, *, entity: Any, event: Any | None=None) -> Any:
        self.session.add(entity)
        await self.session.commit()
        if event is not None and self.outbox_repo is not None:
            await self.outbox_repo.enqueue(event)
        return entity