from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.pecuaria.domain.models.vacina import Vacina


class SanidadeRepositoryPort(ABC):
    @abstractmethod
    async def save_vacina(self, item: Vacina) -> Vacina:
        pass

    @abstractmethod
    async def list_vacinas(self, animal_id: UUID | None = None) -> list[Vacina]:
        pass
