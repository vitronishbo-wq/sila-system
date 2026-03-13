from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.society.familia.domain.aggregates.family_aggregate_root import FamilyAggregate
from apps.backend.app.modules.society.familia.domain.enums import FamilyStatus

class InMemoryFamilyRepository:

    def __init__(self) -> None:
        self.data: dict[UUID, FamilyAggregate] = {}

    async def save(self, aggregate: FamilyAggregate) -> None:
        self.data[aggregate.id] = aggregate

    async def get_by_id(self, family_id: UUID) -> FamilyAggregate | None:
        return self.data.get(family_id)

    async def find_active_family_for_citizen(self, citizen_id: UUID, exclude_family_id: UUID | None=None):
        for agg in self.data.values():
            if exclude_family_id and agg.id == exclude_family_id:
                continue
            if agg.status != FamilyStatus.ACTIVE:
                continue
            for member in agg.members:
                if member.citizen_id == citizen_id:
                    return agg.id
        return None

    async def find_active_family_by_head(self, head_citizen_id: UUID) -> UUID | None:
        for agg in self.data.values():
            if agg.status != FamilyStatus.ACTIVE:
                continue
            if agg.head_citizen_id == head_citizen_id:
                return agg.id
        return None

    async def list_family_ids_for_citizen(self, citizen_id: UUID, *, limit: int=100, offset: int=0) -> list[UUID]:
        matches: list[UUID] = []
        for agg in self.data.values():
            if any((m.citizen_id == citizen_id for m in agg.all_members)):
                matches.append(agg.id)
        return matches[offset:offset + limit]

    async def get_next_sequence(self, year: int) -> int:
        _ = year
        return len(self.data) + 1

    async def commit(self) -> None:
        return None

class InMemoryOutbox:

    def __init__(self) -> None:
        self.events = []

    async def store_many(self, events: list[object]) -> None:
        self.events.extend(events)

class NoopBus:

    async def publish(self, event: object) -> None:
        _ = event