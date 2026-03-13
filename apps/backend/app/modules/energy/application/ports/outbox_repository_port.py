from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class OutboxRepositoryPort(ABC):

    @abstractmethod
    async def enqueue(self, event: Any) -> Any:
        pass

    @abstractmethod
    async def get_pending(self, *, limit: int=100) -> list[Any]:
        pass

    @abstractmethod
    async def mark_done(self, message_id: UUID) -> None:
        pass

    @abstractmethod
    async def increment_retries(self, message_id: UUID, *, error: str | None=None) -> None:
        pass