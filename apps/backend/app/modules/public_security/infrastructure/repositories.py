"""
Repository pattern for public_security module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class PublicSecurityRepository(ABC):
    """Abstract repository for public_security."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get public_security by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save public_security."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete public_security."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all public_security."""
        pass

class PublicSecurityMemoryRepository(PublicSecurityRepository):
    """In-memory repository for public_security."""

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