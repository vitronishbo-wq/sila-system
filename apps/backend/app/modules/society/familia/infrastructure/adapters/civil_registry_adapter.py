from __future__ import annotations

from importlib import import_module
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.familia.application.ports.civil_registry_service_port import (
    CivilRegistryServicePort,
)


class CivilRegistryAdapter(CivilRegistryServicePort):
    """Adapter de leitura para o modulo registo_civil."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def has_active_marriage(self, citizen_id: UUID) -> bool:
        justice_module = import_module(
            "apps.backend.app.modules.justice.civil_registry.domain.models.marriage_record"
        )
        MarriageRecord = justice_module.MarriageRecord
        citizen = str(citizen_id)
        try:
            result = await self._session.execute(
                select(MarriageRecord.id)
                .where(
                    or_(MarriageRecord.spouse1_id == citizen, MarriageRecord.spouse2_id == citizen)
                )
                .limit(1)
            )
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError:
            return False

    async def is_deceased(self, citizen_id: UUID) -> bool:
        justice_module = import_module(
            "apps.backend.app.modules.justice.civil_registry.domain.models.death_record"
        )
        DeathRecord = justice_module.DeathRecord
        try:
            result = await self._session.execute(
                select(DeathRecord.id).where(DeathRecord.citizen_id == str(citizen_id)).limit(1)
            )
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError:
            return False

    async def relationship_exists(self, citizen_a_id: UUID, citizen_b_id: UUID) -> bool:
        justice_module = import_module(
            "apps.backend.app.modules.justice.civil_registry.domain.models.marriage_record"
        )
        MarriageRecord = justice_module.MarriageRecord
        a = str(citizen_a_id)
        b = str(citizen_b_id)
        try:
            result = await self._session.execute(
                select(MarriageRecord.id)
                .where(
                    or_(
                        (MarriageRecord.spouse1_id == a) & (MarriageRecord.spouse2_id == b),
                        (MarriageRecord.spouse1_id == b) & (MarriageRecord.spouse2_id == a),
                    )
                )
                .limit(1)
            )
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError:
            return False
