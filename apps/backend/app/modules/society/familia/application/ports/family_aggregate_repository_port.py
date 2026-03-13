from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.familia.domain.aggregates.family_aggregate_root import FamilyAggregate

class FamilyAggregateRepositoryPort(ABC):

    @abstractmethod
    async def save(self, aggregate: FamilyAggregate) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, family_id: UUID) -> FamilyAggregate | None:
        raise NotImplementedError

    @abstractmethod
    async def find_active_family_for_citizen(self, citizen_id: UUID, exclude_family_id: UUID | None=None) -> UUID | None:
        raise NotImplementedError

    @abstractmethod
    async def find_active_family_by_head(self, head_citizen_id: UUID) -> UUID | None:
        raise NotImplementedError

    @abstractmethod
    async def list_family_ids_for_citizen(self, citizen_id: UUID, *, limit: int=100, offset: int=0) -> list[UUID]:
        raise NotImplementedError

    @abstractmethod
    async def get_next_sequence(self, year: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError