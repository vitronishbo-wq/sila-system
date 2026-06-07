from abc import ABC, abstractmethod
from uuid import UUID


class CivilRegistryServicePort(ABC):
    @abstractmethod
    async def has_active_marriage(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_deceased(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def relationship_exists(self, citizen_a_id: UUID, citizen_b_id: UUID) -> bool:
        raise NotImplementedError
