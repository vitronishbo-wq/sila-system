"""
Repository pattern for migration_service module.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class MigrationServiceRepository(ABC):
    """Abstract repository for migration_service."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get migration_service by ID."""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save migration_service."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete migration_service."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all migration_service."""
        pass

class MigrationServiceMemoryRepository(MigrationServiceRepository):
    """In-memory repository for migration_service."""

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