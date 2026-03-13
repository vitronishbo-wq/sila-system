from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pecuaria.domain.models.reproducao import Reproducao

class ReproducaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Reproducao) -> Reproducao:
        pass

    @abstractmethod
    async def list_by_femea(self, femea_id: UUID | None=None) -> list[Reproducao]:
        pass