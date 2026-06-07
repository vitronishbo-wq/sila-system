"""
Repository pattern for infrastructure_sector module.
"""

from abc import ABC, abstractmethod
from typing import Any


class InfrastructureSectorRepository(ABC):
    """Abstract repository for infrastructure_sector."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get infrastructure_sector by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save infrastructure_sector."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete infrastructure_sector."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all infrastructure_sector."""
        pass


class InfrastructureSectorMemoryRepository(InfrastructureSectorRepository):
    """In-memory repository for infrastructure_sector."""

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
