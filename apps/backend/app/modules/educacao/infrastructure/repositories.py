"""
Repository pattern for educacao module.
"""

from abc import ABC, abstractmethod
from typing import Any


class EducacaoRepository(ABC):
    """Abstract repository for educacao."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get educacao by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save educacao."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete educacao."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all educacao."""
        pass


class EducacaoMemoryRepository(EducacaoRepository):
    """In-memory repository for educacao."""

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
