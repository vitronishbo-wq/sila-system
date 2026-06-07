from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.civil_protection.domain.enums import StatusCorporacao
from apps.backend.app.modules.civil_protection.domain.models.corporacao import Corporacao
from apps.backend.app.modules.civil_protection.domain.ports.corporacao_repository_port import (
    CorporacaoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.infrastructure.models.corporacao_model import (
    CorporacaoModel,
)


class SQLAlchemyCorporacaoRepository(CorporacaoRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, corporacao: Corporacao) -> Corporacao:
        model = await self.session.get(CorporacaoModel, corporacao.id)
        if not model:
            model = CorporacaoModel(id=corporacao.id)
            self.session.add(model)
        model.codigo_corporacao = corporacao.codigo_corporacao
        model.nome = corporacao.nome
        model.municipio = corporacao.municipio
        model.provincia = corporacao.provincia
        model.endereco = corporacao.endereco
        model.comandante = corporacao.comandante
        model.data_ativacao = corporacao.data_ativacao
        model.status = corporacao.status.value
        model.telefone = corporacao.telefone
        model.email = corporacao.email
        model.observacoes = corporacao.observacoes
        model.ativo = corporacao.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, corporacao_id: UUID) -> Corporacao | None:
        model = await self.session.get(CorporacaoModel, corporacao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_corporacao: str) -> Corporacao | None:
        stmt = select(CorporacaoModel).where(
            CorporacaoModel.codigo_corporacao == codigo_corporacao.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Corporacao]:
        stmt = select(CorporacaoModel).order_by(CorporacaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Corporacao]:
        normalized = municipio.strip().lower()
        stmt = (
            select(CorporacaoModel)
            .where(func.lower(CorporacaoModel.municipio) == normalized)
            .order_by(CorporacaoModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusCorporacao) -> list[Corporacao]:
        stmt = (
            select(CorporacaoModel)
            .where(CorporacaoModel.status == status.value)
            .order_by(CorporacaoModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, corporacao_id: UUID) -> bool:
        model = await self.session.get(CorporacaoModel, corporacao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"COR/{year}/"
        stmt = (
            select(func.count())
            .select_from(CorporacaoModel)
            .where(CorporacaoModel.codigo_corporacao.like(f"{prefix}%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"{prefix}{count + 1:05d}"

    @staticmethod
    def _to_domain(model: CorporacaoModel) -> Corporacao:
        return Corporacao(
            id=model.id,
            codigo_corporacao=model.codigo_corporacao,
            nome=model.nome,
            municipio=model.municipio,
            provincia=model.provincia,
            endereco=model.endereco,
            comandante=model.comandante,
            data_ativacao=model.data_ativacao,
            status=StatusCorporacao(model.status),
            telefone=model.telefone,
            email=model.email,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
