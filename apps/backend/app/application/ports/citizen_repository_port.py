from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from ...domain.citizen import Citizen

class CitizenRepositoryPort(ABC):
    @abstractmethod
    async def add(self, citizen: Citizen) -> Citizen:
        pass

    @abstractmethod
    async def update(self, citizen: Citizen) -> Citizen:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Citizen]:
        pass

    @abstractmethod
    async def get_by_national_id_number(self, national_id_number: str) -> Optional[Citizen]:
        pass

    @abstractmethod
    async def get_by_nif(self, nif: str) -> Optional[Citizen]:
        pass

    @abstractmethod
    async def list(self, *, filters: dict, limit: int, offset: int) -> List[Citizen]:
        pass

    @abstractmethod
    async def soft_delete(self, id: UUID) -> None:
        pass
