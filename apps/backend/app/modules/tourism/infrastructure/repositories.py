"""
Repository pattern for tourism module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class TourismRepository(ABC):
    """Abstract repository for tourism."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get tourism by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save tourism."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete tourism."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all tourism."""
        pass

class TourismMemoryRepository(TourismRepository):
    """In-memory repository for tourism."""

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