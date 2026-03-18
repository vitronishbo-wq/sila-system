"""Base repository interface"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository following Repository pattern"""
    
    @abstractmethod
    async def find_all(self) -> List[T]:
        """Find all entities"""
        pass
    
    @abstractmethod
    async def find_by_id(self, id: Any) -> Optional[T]:
        """Find entity by ID"""
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save or update entity"""
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete entity"""
        pass
    
    @abstractmethod
    async def exists(self, id: Any) -> bool:
        """Check if entity exists"""
        pass


__all__ = ["BaseRepository"]
