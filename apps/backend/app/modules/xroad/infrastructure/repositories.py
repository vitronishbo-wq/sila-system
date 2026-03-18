"""
Repository pattern for xroad module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class XroadRepository(ABC):
    """Abstract repository for xroad."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get xroad by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save xroad."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete xroad."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all xroad."""
        pass

class XroadMemoryRepository(XroadRepository):
    """In-memory repository for xroad."""

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