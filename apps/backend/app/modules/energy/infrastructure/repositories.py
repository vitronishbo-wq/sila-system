"""
Repository pattern for energy module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class EnergyRepository(ABC):
    """Abstract repository for energy."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get energy by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save energy."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete energy."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all energy."""
        pass

class EnergyMemoryRepository(EnergyRepository):
    """In-memory repository for energy."""

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