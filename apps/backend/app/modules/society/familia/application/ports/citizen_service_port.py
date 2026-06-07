from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class CitizenServicePort(ABC):
    @abstractmethod
    async def get_citizen(self, citizen_id: UUID) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def verify_civil_capacity(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_age(self, citizen_id: UUID) -> int:
        raise NotImplementedError
