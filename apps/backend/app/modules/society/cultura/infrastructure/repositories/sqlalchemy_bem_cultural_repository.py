from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.cultura.application.ports.bem_cultural_repository_port import (
    BemCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento, TipoPatrimonio
from apps.backend.app.modules.society.cultura.domain.models.bem_cultural import BemCultural
from apps.backend.app.modules.society.cultura.infrastructure.models.bem_cultural_model import (
    BemCulturalModel,
)


class SQLAlchemyBemCulturalRepository(BemCulturalRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, bem: BemCultural) -> BemCultural:
        model = await self.session.get(BemCulturalModel, bem.id)
        if not model:
            model = BemCulturalModel(id=bem.id)
            self.session.add(model)
        model.registro_ipat = bem.registro_ipat
        model.nome = bem.nome
        model.tipo = bem.tipo.value
        model.descricao = bem.descricao
        model.localizacao = bem.localizacao
        model.municipio = bem.municipio
        model.provincia = bem.provincia
        model.coordenadas_lat = bem.coordenadas_lat
        model.coordenadas_long = bem.coordenadas_long
        model.status_tombamento = bem.status_tombamento.value
        model.tombamento_id = bem.tombamento_id
        model.data_cadastro = bem.data_cadastro
        model.ativo = bem.ativo
        model.observacoes = bem.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, bem_id: UUID) -> BemCultural | None:
        model = await self.session.get(BemCulturalModel, bem_id)
        return self._to_domain(model) if model else None

    async def get_by_registro(self, registro_ipat: str) -> BemCultural | None:
        stmt = select(BemCulturalModel).where(
            BemCulturalModel.registro_ipat == registro_ipat.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[BemCultural]:
        stmt = select(BemCulturalModel).order_by(BemCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoPatrimonio) -> list[BemCultural]:
        stmt = (
            select(BemCulturalModel)
            .where(BemCulturalModel.tipo == tipo.value)
            .order_by(BemCulturalModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[BemCultural]:
        stmt = (
            select(BemCulturalModel)
            .where(func.lower(BemCulturalModel.municipio) == municipio.strip().lower())
            .order_by(BemCulturalModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status_tombamento(self, status: StatusTombamento) -> list[BemCultural]:
        stmt = (
            select(BemCulturalModel)
            .where(BemCulturalModel.status_tombamento == status.value)
            .order_by(BemCulturalModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, bem_id: UUID) -> bool:
        model = await self.session.get(BemCulturalModel, bem_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(BemCulturalModel)
            .where(BemCulturalModel.registro_ipat.like(f"IPAT/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"IPAT/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: BemCulturalModel) -> BemCultural:
        return BemCultural(
            id=model.id,
            registro_ipat=model.registro_ipat,
            nome=model.nome,
            tipo=TipoPatrimonio(model.tipo),
            descricao=model.descricao,
            localizacao=model.localizacao,
            municipio=model.municipio,
            provincia=model.provincia,
            data_cadastro=model.data_cadastro,
            status_tombamento=StatusTombamento(model.status_tombamento),
            coordenadas_lat=model.coordenadas_lat,
            coordenadas_long=model.coordenadas_long,
            tombamento_id=model.tombamento_id,
            ativo=model.ativo,
            observacoes=model.observacoes,
        )
