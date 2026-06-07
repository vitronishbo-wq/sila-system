"""
Repository pattern for economy module.
"""

from abc import ABC, abstractmethod
from typing import Any


class EconomyRepository(ABC):
    """Abstract repository for economy."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get economy by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save economy."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete economy."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all economy."""
        pass


class EconomyMemoryRepository(EconomyRepository):
    """In-memory repository for economy."""

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
