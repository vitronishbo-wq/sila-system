from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure.application.events.contracts import EVENT_CONTRACTS
from apps.backend.app.modules.infrastructure.infrastructure.governance.event_catalog_model import EventCatalogModel
from apps.backend.app.modules.infrastructure.infrastructure.governance.schema_validator import validate_payload

class EventGovernanceError(RuntimeError):
    pass

@dataclass(frozen=True)
class EventContract:
    event_name: str
    version: int
    owner: str
    description: str
    schema: dict[str, Any]

class EventGovernanceService:

    def resolve_contract(self, event_name: str) -> EventContract:
        raw = EVENT_CONTRACTS.get(event_name)
        if raw is None:
            raise EventGovernanceError(f'Evento sem contrato catalogado: {event_name}')
        return EventContract(event_name=event_name, version=int(raw['version']), owner=str(raw['owner']), description=str(raw['description']), schema=dict(raw['schema']))

    async def validate_event(self, *, session: AsyncSession, event_name: str, payload: dict[str, Any]) -> None:
        contract = self.resolve_contract(event_name)
        payload_version = int(payload.get('version') or 0)
        if payload_version != contract.version:
            raise EventGovernanceError(f'Versao invalida para {event_name}: payload={payload_version}, catalog={contract.version}')
        if not validate_payload(payload, contract.schema):
            raise EventGovernanceError(f'Payload invalido para contrato {event_name}')
        await self._ensure_catalog_entry(session, contract=contract)

    async def _ensure_catalog_entry(self, session: AsyncSession, *, contract: EventContract) -> None:
        try:
            stmt = select(EventCatalogModel).where(EventCatalogModel.event_name == contract.event_name)
            result = await session.execute(stmt)
            row = result.scalars().first()
        except SQLAlchemyError:
            return
        if row is None:
            session.add(EventCatalogModel(event_name=contract.event_name, version=contract.version, owner=contract.owner, description=contract.description, schema=contract.schema, active=True))
            await session.flush()
            return
        if not row.active:
            raise EventGovernanceError(f'Evento inativo no catalogo central: {contract.event_name}')
        if int(row.version) != contract.version:
            raise EventGovernanceError(f'Versao divergente no catalogo: {contract.event_name} v{row.version} != v{contract.version}')
