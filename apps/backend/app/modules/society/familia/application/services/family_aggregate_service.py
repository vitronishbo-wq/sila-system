from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from app.domain.events import EventBusPort
from apps.backend.app.modules.society.familia.application.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.society.familia.application.ports.civil_registry_service_port import CivilRegistryServicePort
from apps.backend.app.modules.society.familia.application.ports.family_aggregate_repository_port import FamilyAggregateRepositoryPort
from apps.backend.app.modules.society.familia.application.ports.outbox_repository_port import OutboxRepositoryPort
from apps.backend.app.modules.society.familia.domain.aggregates.family_aggregate_root import FamilyAggregate
from apps.backend.app.modules.society.familia.domain.enums import MemberRole
from apps.backend.app.modules.society.familia.domain.rules.one_active_family_rule import OneActiveFamilyRule
from apps.backend.app.modules.society.familia.domain.value_objects.family_code import FamilyCode

class FamilyAggregateService:

    def __init__(self, *, repository: FamilyAggregateRepositoryPort, outbox_repository: OutboxRepositoryPort, event_bus: EventBusPort, citizen_service: CitizenServicePort | None=None, civil_registry_service: CivilRegistryServicePort | None=None) -> None:
        self._repository = repository
        self._outbox = outbox_repository
        self._event_bus = event_bus
        self._citizen_service = citizen_service
        self._civil_registry_service = civil_registry_service

    async def create_aggregate(self, *, head_citizen_id: UUID, initial_members: list, metadata: dict):
        if self._citizen_service:
            await self._citizen_service.get_citizen(head_citizen_id)
            if not await self._citizen_service.verify_civil_capacity(head_citizen_id):
                raise ValueError('Chefe do agregado deve possuir capacidade civil ativa')
        if self._civil_registry_service and await self._civil_registry_service.is_deceased(head_citizen_id):
            raise ValueError('Nao e possivel criar agregado para cidadao com obito registrado')
        await OneActiveFamilyRule().validate(citizen_id=head_citizen_id, family_repository=self._repository, exclude_family_id=None)
        year = datetime.now(timezone.utc).year
        sequence = await self._repository.get_next_sequence(year)
        code = FamilyCode.generate(year=year, sequence=sequence).value
        aggregate = FamilyAggregate(family_id=uuid4(), code=code, head_citizen_id=head_citizen_id, metadata=metadata)
        for member in initial_members:
            if self._citizen_service:
                await self._citizen_service.get_citizen(member.citizen_id)
            if self._civil_registry_service and await self._civil_registry_service.is_deceased(member.citizen_id):
                raise ValueError(f'Membro {member.citizen_id} possui obito registrado')
            await OneActiveFamilyRule().validate(citizen_id=member.citizen_id, family_repository=self._repository, exclude_family_id=aggregate.id)
            aggregate.add_member(citizen_id=member.citizen_id, role=member.role)
        await self._repository.save(aggregate)
        events = aggregate.get_pending_events()
        await self._outbox.store_many(events)
        await self._repository.commit()
        for event in events:
            await self._event_bus.publish(event)
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}

    async def add_member_to_aggregate(self, *, family_id: UUID, citizen_id: UUID, role: MemberRole):
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        if self._citizen_service:
            await self._citizen_service.get_citizen(citizen_id)
        if self._civil_registry_service and await self._civil_registry_service.is_deceased(citizen_id):
            raise ValueError(f'Nao e possivel adicionar {citizen_id}: obito registrado')
        await OneActiveFamilyRule().validate(citizen_id=citizen_id, family_repository=self._repository, exclude_family_id=family_id)
        aggregate.add_member(citizen_id=citizen_id, role=role)
        await self._repository.save(aggregate)
        events = aggregate.get_pending_events()
        await self._outbox.store_many(events)
        await self._repository.commit()
        for event in events:
            await self._event_bus.publish(event)
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}

    async def transfer_head(self, *, family_id: UUID, new_head_citizen_id: UUID):
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        if self._citizen_service:
            await self._citizen_service.get_citizen(new_head_citizen_id)
            if not await self._citizen_service.verify_civil_capacity(new_head_citizen_id):
                raise ValueError('Novo chefe deve possuir capacidade civil ativa')
        if self._civil_registry_service and await self._civil_registry_service.is_deceased(new_head_citizen_id):
            raise ValueError('Nao e possivel transferir chefia para cidadao com obito registrado')
        aggregate.transfer_head(new_head_citizen_id=new_head_citizen_id)
        await self._repository.save(aggregate)
        events = aggregate.get_pending_events()
        await self._outbox.store_many(events)
        await self._repository.commit()
        for event in events:
            await self._event_bus.publish(event)
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}

    async def dissolve_aggregate(self, *, family_id: UUID, reason: str):
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        aggregate.dissolve(reason=reason)
        await self._repository.save(aggregate)
        events = aggregate.get_pending_events()
        await self._outbox.store_many(events)
        await self._repository.commit()
        for event in events:
            await self._event_bus.publish(event)
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}

    async def remove_member(self, *, family_id: UUID, citizen_id: UUID, reason: str | None=None):
        aggregate = await self._repository.get_by_id(family_id)
        if not aggregate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Agregado nao encontrado')
        aggregate.remove_member(citizen_id=citizen_id, reason=reason)
        await self._repository.save(aggregate)
        events = aggregate.get_pending_events()
        await self._outbox.store_many(events)
        await self._repository.commit()
        for event in events:
            await self._event_bus.publish(event)
        return {'id': aggregate.id, 'code': aggregate.code, 'head_citizen_id': aggregate.head_citizen_id, 'status': aggregate.status, 'member_count': len(aggregate.members), 'created_at': aggregate.created_at, 'updated_at': aggregate.updated_at}