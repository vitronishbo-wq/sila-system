"""
Repository pattern for justice module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class JusticeRepository(ABC):
    """Abstract repository for justice."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get justice by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save justice."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete justice."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all justice."""
        pass

class JusticeMemoryRepository(JusticeRepository):
    """In-memory repository for justice."""

    def __init__(self):
        self.data = {}

    async def get_by_id(self, id: str) -> Optional[Any]:
        return self.data.get(id)

    async def save(self, entity: Any) -> Any:
        self.data[entity.id] = entity
        return entity

    async def delete(self, id: str) -> bool:
        if id in self.data:
            del self.data[id]
            return True
        return False

    async def list_all(self) -> List[Any]:
        return list(self.data.values())