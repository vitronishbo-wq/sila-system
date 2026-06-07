"""
Repository pattern for saude module.
"""

from abc import ABC, abstractmethod
from typing import Any


class SaudeRepository(ABC):
    """Abstract repository for saude."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get saude by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save saude."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete saude."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all saude."""
        pass


class SaudeMemoryRepository(SaudeRepository):
    """In-memory repository for saude."""

    def __init__(self):
        self.data = {}

    async def get_by_id(self, id: str) -> Any | None:
        return self.data.get(id)

    async def save(self, entity: Any) -> Any:
        self.data[entity.id] = entity
        return entity

    async def delete(self, id: str) -> bool:
        if id in self.data:
            del self.data[id]
            return True
        return False

    async def list_all(self) -> list[Any]:
        return list(self.data.values())
