"""
Repository pattern for compliance module.
"""

from abc import ABC, abstractmethod
from typing import Any


class ComplianceRepository(ABC):
    """Abstract repository for compliance."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get compliance by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save compliance."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete compliance."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all compliance."""
        pass


class ComplianceMemoryRepository(ComplianceRepository):
    """In-memory repository for compliance."""

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
