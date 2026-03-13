from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import CitizenRepository
from app.core.db import AsyncSessionLocal
from apps.backend.app.modules.society.familia.application.events.bus import event_bus
from apps.backend.app.modules.society.familia.application.services.family_aggregate_service import FamilyAggregateService
from apps.backend.app.modules.society.familia.application.services.family_projection_handler import FamilyProjectionHandler
from apps.backend.app.modules.society.familia.application.services.family_query_service import FamilyQueryService
from apps.backend.app.modules.society.familia.domain.events import FamilyCreatedEvent, FamilyDissolvedEvent, FamilyHeadTransferredEvent, FamilyMemberAddedEvent, FamilyMemberRemovedEvent
from app.core.events import DomainEvent
from apps.backend.app.modules.society.familia.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.society.familia.infrastructure.adapters.civil_registry_adapter import CivilRegistryAdapter
from apps.backend.app.modules.society.familia.infrastructure.repositories.outbox_repository import OutboxRepository
from apps.backend.app.modules.society.familia.infrastructure.repositories.redis_projection_repository import RedisProjectionRepository
from apps.backend.app.modules.society.familia.infrastructure.repositories.sqlalchemy_family_aggregate_repository import SQLAlchemyFamilyAggregateRepository
from apps.backend.app.modules.society.familia.infrastructure.event_handlers.on_citizen_deceased import on_citizen_deceased
from app.core.events import EventBusAdapter
_subscriptions_configured = False
_core_subscriptions_configured = False

async def _project_family_created(event: DomainEvent) -> None:
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        projection_repo = RedisProjectionRepository(session)
        handler = FamilyProjectionHandler(projection_repository=projection_repo, family_repository=repo)
        await handler.on_family_created(event)
        await session.commit()

async def _project_family_member_added(event: DomainEvent) -> None:
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        projection_repo = RedisProjectionRepository(session)
        handler = FamilyProjectionHandler(projection_repository=projection_repo, family_repository=repo)
        await handler.on_family_member_added(event)
        await session.commit()

async def _project_family_head_transferred(event: DomainEvent) -> None:
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        projection_repo = RedisProjectionRepository(session)
        handler = FamilyProjectionHandler(projection_repository=projection_repo, family_repository=repo)
        await handler.on_family_member_added(event)
        await session.commit()

async def _project_family_dissolved(event: DomainEvent) -> None:
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        projection_repo = RedisProjectionRepository(session)
        handler = FamilyProjectionHandler(projection_repository=projection_repo, family_repository=repo)
        await handler.on_family_member_added(event)
        await session.commit()

async def _project_family_member_removed(event: DomainEvent) -> None:
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        projection_repo = RedisProjectionRepository(session)
        handler = FamilyProjectionHandler(projection_repository=projection_repo, family_repository=repo)
        await handler.on_family_member_added(event)
        await session.commit()

def _configure_subscriptions() -> None:
    global _subscriptions_configured
    if _subscriptions_configured:
        return
    event_bus.subscribe(FamilyCreatedEvent.event_name, _project_family_created)
    event_bus.subscribe(FamilyMemberAddedEvent.event_name, _project_family_member_added)
    event_bus.subscribe(FamilyHeadTransferredEvent.event_name, _project_family_head_transferred)
    event_bus.subscribe(FamilyDissolvedEvent.event_name, _project_family_dissolved)
    event_bus.subscribe(FamilyMemberRemovedEvent.event_name, _project_family_member_removed)
    _subscriptions_configured = True

def _configure_core_event_subscriptions() -> None:
    global _core_subscriptions_configured
    if _core_subscriptions_configured:
        return
    core_bus = EventBusAdapter()
    core_bus.subscribe('registo_civil.death_registered', on_citizen_deceased)
    _core_subscriptions_configured = True
_configure_subscriptions()
_configure_core_event_subscriptions()

async def get_family_aggregate_service(session: AsyncSession=Depends(get_db)) -> FamilyAggregateService:
    repo = SQLAlchemyFamilyAggregateRepository(session)
    outbox = OutboxRepository(session)
    citizen_adapter = CitizenServiceAdapter(CitizenRepository(session))
    civil_registry_adapter = CivilRegistryAdapter(session)
    return FamilyAggregateService(repository=repo, outbox_repository=outbox, event_bus=event_bus, citizen_service=citizen_adapter, civil_registry_service=civil_registry_adapter)

async def get_family_query_service(session: AsyncSession=Depends(get_db)) -> FamilyQueryService:
    projection_repo = RedisProjectionRepository(session)
    repo = SQLAlchemyFamilyAggregateRepository(session)
    citizen_adapter = CitizenServiceAdapter(CitizenRepository(session))
    return FamilyQueryService(repository=repo, projection_repository=projection_repo, citizen_service=citizen_adapter)