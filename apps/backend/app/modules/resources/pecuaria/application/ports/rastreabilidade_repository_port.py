from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pecuaria.domain.models.rastreabilidade import Rastreabilidade

class RastreabilidadeRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Rastreabilidade) -> Rastreabilidade:
        pass

    @abstractmethod
    async def list_by_animal(self, animal_id: UUID) -> list[Rastreabilidade]:
        pass