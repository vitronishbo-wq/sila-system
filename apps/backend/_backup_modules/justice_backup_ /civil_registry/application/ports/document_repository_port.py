from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

class DocumentRepositoryPort(ABC):

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> list[Any]:
        pass

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> list[Any]:
        pass

    @abstractmethod
    async def create(self, document: Any) -> Any:
        pass