from abc import ABC, abstractmethod
from uuid import UUID


class OcorrenciaIncendioRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: object) -> object:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> object | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[object]:
        pass
