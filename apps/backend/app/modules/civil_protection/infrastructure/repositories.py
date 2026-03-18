"""
Repository pattern for civil_protection module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class CivilProtectionRepository(ABC):
    """Abstract repository for civil_protection."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get civil_protection by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save civil_protection."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete civil_protection."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all civil_protection."""
        pass

class CivilProtectionMemoryRepository(CivilProtectionRepository):
    """In-memory repository for civil_protection."""

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