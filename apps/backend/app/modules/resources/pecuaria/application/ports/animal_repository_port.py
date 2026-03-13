from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pecuaria.domain.enums import StatusAnimal, TipoAnimal
from app.modules.resources.pecuaria.domain.models.animal import Animal

class AnimalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, animal: Animal) -> Animal:
        pass

    @abstractmethod
    async def get_by_id(self, animal_id: UUID) -> Animal | None:
        pass

    @abstractmethod
    async def get_by_brinco(self, brinco: str) -> Animal | None:
        pass

    @abstractmethod
    async def list_by_propriedade(self, propriedade_id: UUID) -> list[Animal]:
        pass

    @abstractmethod
    async def list_by_rebanho(self, rebanho_id: UUID) -> list[Animal]:
        pass

    @abstractmethod
    async def list_by_filtros(self, *, tipo: TipoAnimal | None=None, status: StatusAnimal | None=None) -> list[Animal]:
        pass

    @abstractmethod
    async def next_brinco(self, propriedade_id: UUID) -> str:
        pass