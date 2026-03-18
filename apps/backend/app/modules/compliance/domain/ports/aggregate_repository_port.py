from abc import ABC, abstractmethod
from typing import List, Optional

class AggregateRepositoryPort(ABC):
    """Port: Generic aggregate repository pattern for domain persistence (Compliance)."""

    @abstractmethod
    async def create(self, aggregate) -> None:
        pass

    @abstractmethod
    async def save(self, aggregate) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[object]:
        pass

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> List[object]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass