from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from uuid import UUID

@dataclass(slots=True)
class OutboxMessage:
    id: UUID | None
    event: object
    event_name: str
    payload: dict
    retries: int = 0
    locked_by: str | None = None
    locked_at: datetime | None = None

class OutboxRepositoryPort(ABC):

    @abstractmethod
    async def append(self, event: object) -> None:
        raise NotImplementedError

    @abstractmethod
    async def pop_batch(self, batch_size: int=100, *, worker_id: str | None=None, lock_ttl_seconds: int=60) -> list[OutboxMessage]:
        raise NotImplementedError

    @abstractmethod
    async def mark_processed(self, message: OutboxMessage) -> None:
        raise NotImplementedError

    @abstractmethod
    async def mark_failed(self, message: OutboxMessage, *, error: str | None=None, retry_delay_seconds: int=5) -> None:
        raise NotImplementedError