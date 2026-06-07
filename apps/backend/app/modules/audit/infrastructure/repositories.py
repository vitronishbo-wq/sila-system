"""
Repository pattern for audit module.
"""

from abc import ABC, abstractmethod
from typing import Any


class AuditRepository(ABC):
    """Abstract repository for audit."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Any | None:
        """Get audit by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save audit."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete audit."""
        pass

    @abstractmethod
    async def list_all(self) -> list[Any]:
        """List all audit."""
        pass


class AuditMemoryRepository(AuditRepository):
    """In-memory repository for audit."""

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
