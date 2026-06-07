from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class NamedEntityRepositoryPort(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity_id: int, data: dict[str, Any]) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        raise NotImplementedError
