from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.marketplace_institution_model import (
    MarketplaceInstitutionModel,
)


class MarketplaceInstitutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        provincia: str | None = None,
        municipio: str | None = None,
        bairro: str | None = None,
        tipo: str | None = None,
        nivel_ensino: str | None = None,
        q: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[MarketplaceInstitutionModel], int]:
        stmt = select(MarketplaceInstitutionModel).where(MarketplaceInstitutionModel.status == "activa")
        count_stmt = select(MarketplaceInstitutionModel.id).where(MarketplaceInstitutionModel.status == "activa")
        if provincia:
            stmt = stmt.where(MarketplaceInstitutionModel.provincia == provincia)
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.provincia == provincia)
        if municipio:
            stmt = stmt.where(MarketplaceInstitutionModel.municipio == municipio)
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.municipio == municipio)
        if bairro:
            stmt = stmt.where(MarketplaceInstitutionModel.bairro == bairro)
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.bairro == bairro)
        if tipo:
            stmt = stmt.where(MarketplaceInstitutionModel.tipo == tipo)
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.tipo == tipo)
        if nivel_ensino:
            stmt = stmt.where(MarketplaceInstitutionModel.nivel_ensino == nivel_ensino)
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.nivel_ensino == nivel_ensino)
        if q:
            pattern = f"%{q}%"
            stmt = stmt.where(MarketplaceInstitutionModel.nome.ilike(pattern))
            count_stmt = count_stmt.where(MarketplaceInstitutionModel.nome.ilike(pattern))

        count_result = await self.session.execute(count_stmt)
        total = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size).order_by(MarketplaceInstitutionModel.nome)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def get_by_institution_id(self, institution_id: uuid.UUID) -> MarketplaceInstitutionModel | None:
        stmt = select(MarketplaceInstitutionModel).where(
            MarketplaceInstitutionModel.institution_id == institution_id,
            MarketplaceInstitutionModel.status == "activa",
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_from_escola(self, data: dict) -> MarketplaceInstitutionModel:
        existing = await self.get_by_institution_id(data["institution_id"])
        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
            return existing
        model = MarketplaceInstitutionModel(**data)
        self.session.add(model)
        return model
