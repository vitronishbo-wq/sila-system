from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class OutboxRepositoryPort(ABC):
    @abstractmethod
    async def enqueue(self, event: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_pending(self, *, limit: int = 100) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    async def mark_done(self, message_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def increment_retries(self, message_id: UUID, *, error: str | None = None) -> None:
        raise NotImplementedError
