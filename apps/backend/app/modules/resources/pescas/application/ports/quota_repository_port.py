from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.pescas.domain.models.quota import Quota


class QuotaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, quota: Quota) -> Quota:
        pass

    @abstractmethod
    async def get_by_id(self, quota_id: UUID) -> Quota | None:
        pass

    @abstractmethod
    async def list_by_especie(self, especie_id: UUID) -> list[Quota]:
        pass

    @abstractmethod
    async def list_by_ano(self, ano: int) -> list[Quota]:
        pass
