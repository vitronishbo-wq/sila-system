from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class OutboxRepositoryPort(ABC):
    @abstractmethod
    async def store_many(self, events: list[Any]) -> None:
        raise NotImplementedError
