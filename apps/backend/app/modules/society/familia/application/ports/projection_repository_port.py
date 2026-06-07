from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class ProjectionRepositoryPort(ABC):
    @abstractmethod
    async def get_family_composition(self, family_id: UUID) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert_family_composition(self, payload: dict) -> None:
        raise NotImplementedError
