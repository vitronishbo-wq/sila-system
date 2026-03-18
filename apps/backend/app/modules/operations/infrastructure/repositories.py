"""
Repository pattern for operations module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class OperationsRepository(ABC):
    """Abstract repository for operations."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get operations by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save operations."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete operations."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all operations."""
        pass

class OperationsMemoryRepository(OperationsRepository):
    """In-memory repository for operations."""

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