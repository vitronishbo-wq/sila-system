from __future__ import annotations
from uuid import UUID
from app.core.db import AsyncSessionLocal
from app.modules.society.familia.application.events.bus import event_bus as familia_event_bus
from app.modules.society.familia.application.services.family_aggregate_service import FamilyAggregateService
from app.modules.society.familia.infrastructure.repositories.outbox_repository import OutboxRepository
from app.modules.society.familia.infrastructure.repositories.sqlalchemy_family_aggregate_repository import SQLAlchemyFamilyAggregateRepository

def _extract_payload(event: object) -> dict:
    if isinstance(event, dict):
        return event.get('payload') or event.get('data') or {}
    payload = getattr(event, 'payload', None)
    if payload is not None:
        return payload
    data = getattr(event, 'data', None)
    if data is not None:
        return data
    if hasattr(event, 'to_payload'):
        try:
            return event.to_payload() or {}
        except Exception:
            return {}
    return {}

async def on_citizen_deceased(event: object) -> None:
    """
    Handler de integração: óbito registrado no registo_civil.

    Regras mínimas:
    - Se o cidadão falecido é chefe de uma família ativa -> dissolver agregado
    - Se é membro -> remover (soft leave) do agregado
    """
    payload = _extract_payload(event)
    raw_id = payload.get('citizen_id')
    if not raw_id:
        return
    try:
        citizen_id = UUID(str(raw_id))
    except Exception:
        return
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyFamilyAggregateRepository(session)
        family_id = await repo.find_active_family_for_citizen(citizen_id)
        if not family_id:
            return
        service = FamilyAggregateService(repository=repo, outbox_repository=OutboxRepository(session), event_bus=familia_event_bus)
        aggregate = await repo.get_by_id(family_id)
        if not aggregate:
            return
        if aggregate.head_citizen_id == citizen_id:
            await service.dissolve_aggregate(family_id=family_id, reason='death_registered')
        else:
            await service.remove_member(family_id=family_id, citizen_id=citizen_id, reason='death_registered')