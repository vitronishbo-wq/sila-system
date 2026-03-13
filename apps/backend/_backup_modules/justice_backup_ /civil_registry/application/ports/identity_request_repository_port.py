from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

class IdentityRequestRepositoryPort(ABC):

    @abstractmethod
    async def save(self, identity_request: Any) -> Any:
        pass

    @abstractmethod
    async def get_by_id(self, req_id: UUID) -> Optional[Any]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: str, skip: int=0, limit: int=100, **filters) -> tuple:
        pass

    @abstractmethod
    async def get_pending(self) -> list[Any]:
        pass