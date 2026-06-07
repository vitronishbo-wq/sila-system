from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.marketplace_institution_model import (
    MarketplaceInstitutionModel,
)
from apps.backend.app.modules.educacao.infrastructure.models.marketplace_vacancy_model import (
    MarketplaceVacancyModel,
)


class MarketplaceVacancyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        provincia: str | None = None,
        municipio: str | None = None,
        classe: str | None = None,
        turno: str | None = None,
        instituicao_id: uuid.UUID | None = None,
        min_vagas: int = 1,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[MarketplaceVacancyModel], int]:
        stmt = select(MarketplaceVacancyModel).where(MarketplaceVacancyModel.vagas_disponiveis >= min_vagas)
        count_stmt = select(MarketplaceVacancyModel.id).where(MarketplaceVacancyModel.vagas_disponiveis >= min_vagas)
        if provincia:
            stmt = stmt.where(MarketplaceVacancyModel.institution_id.in_(
                select(MarketplaceInstitutionModel.institution_id).where(
                    MarketplaceInstitutionModel.provincia == provincia
                )
            ))
            count_stmt = count_stmt.where(MarketplaceVacancyModel.institution_id.in_(
                select(MarketplaceInstitutionModel.institution_id).where(
                    MarketplaceInstitutionModel.provincia == provincia
                )
            ))
        if municipio:
            stmt = stmt.where(MarketplaceVacancyModel.institution_id.in_(
                select(MarketplaceInstitutionModel.institution_id).where(
                    MarketplaceInstitutionModel.municipio == municipio
                )
            ))
            count_stmt = count_stmt.where(MarketplaceVacancyModel.institution_id.in_(
                select(MarketplaceInstitutionModel.institution_id).where(
                    MarketplaceInstitutionModel.municipio == municipio
                )
            ))
        if classe:
            stmt = stmt.where(MarketplaceVacancyModel.classe == classe)
            count_stmt = count_stmt.where(MarketplaceVacancyModel.classe == classe)
        if turno:
            stmt = stmt.where(MarketplaceVacancyModel.turno == turno)
            count_stmt = count_stmt.where(MarketplaceVacancyModel.turno == turno)
        if instituicao_id:
            stmt = stmt.where(MarketplaceVacancyModel.institution_id == instituicao_id)
            count_stmt = count_stmt.where(MarketplaceVacancyModel.institution_id == instituicao_id)

        count_result = await self.session.execute(count_stmt)
        total = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size).order_by(MarketplaceVacancyModel.vagas_disponiveis.desc())
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def get_by_institution_class_shift(
        self, institution_id: uuid.UUID, ano_letivo: str, classe: str, turno: str
    ) -> MarketplaceVacancyModel | None:
        stmt = select(MarketplaceVacancyModel).where(
            MarketplaceVacancyModel.institution_id == institution_id,
            MarketplaceVacancyModel.ano_letivo == ano_letivo,
            MarketplaceVacancyModel.classe == classe,
            MarketplaceVacancyModel.turno == turno,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _lock_vacancy(self, vacancy_id: uuid.UUID) -> MarketplaceVacancyModel | None:
        stmt = (
            select(MarketplaceVacancyModel)
            .where(MarketplaceVacancyModel.id == vacancy_id)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def reserve_slot(self, vacancy_id: uuid.UUID) -> bool:
        locked = await self._lock_vacancy(vacancy_id)
        if not locked or locked.vagas_disponiveis < 1:
            return False
        stmt = (
            update(MarketplaceVacancyModel)
            .where(
                MarketplaceVacancyModel.id == vacancy_id,
                MarketplaceVacancyModel.vagas_disponiveis > 0,
            )
            .values(
                vagas_disponiveis=MarketplaceVacancyModel.vagas_disponiveis - 1,
                vagas_ocupadas=MarketplaceVacancyModel.vagas_ocupadas + 1,
            )
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def release_slot(self, vacancy_id: uuid.UUID) -> bool:
        locked = await self._lock_vacancy(vacancy_id)
        if not locked or locked.vagas_ocupadas < 1:
            return False
        stmt = (
            update(MarketplaceVacancyModel)
            .where(
                MarketplaceVacancyModel.id == vacancy_id,
                MarketplaceVacancyModel.vagas_ocupadas > 0,
            )
            .values(
                vagas_disponiveis=MarketplaceVacancyModel.vagas_disponiveis + 1,
                vagas_ocupadas=MarketplaceVacancyModel.vagas_ocupadas - 1,
            )
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def count_total(self) -> int:
        stmt = select(MarketplaceVacancyModel.id)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def sum_vagas_disponiveis(self) -> int:
        stmt = select(MarketplaceVacancyModel.vagas_disponiveis)
        result = await self.session.execute(stmt)
        return sum(result.scalars().all())
