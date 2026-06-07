from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.public_security.application.ports.unidade_policial_repository_port import (
    UnidadePolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import (
    StatusUnidadePolicial,
    TipoUnidadePolicial,
)
from apps.backend.app.modules.public_security.domain.models.unidade_policial import UnidadePolicial
from apps.backend.app.modules.public_security.infrastructure.models.unidade_policial_model import (
    UnidadePolicialModel,
)


class SQLAlchemyUnidadePolicialRepository(UnidadePolicialRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, unidade: UnidadePolicial) -> UnidadePolicial:
        model = await self.session.get(UnidadePolicialModel, unidade.id)
        if not model:
            model = UnidadePolicialModel(id=unidade.id)
            self.session.add(model)
        model.codigo_unidade = unidade.codigo_unidade
        model.nome = unidade.nome
        model.tipo = unidade.tipo.value
        model.municipio = unidade.municipio
        model.provincia = unidade.provincia
        model.endereco = unidade.endereco
        model.comandante = unidade.comandante
        model.data_ativacao = unidade.data_ativacao
        model.status = unidade.status.value
        model.telefone = unidade.telefone
        model.email = unidade.email
        model.observacoes = unidade.observacoes
        model.ativo = unidade.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, unidade_id: UUID) -> UnidadePolicial | None:
        model = await self.session.get(UnidadePolicialModel, unidade_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_unidade: str) -> UnidadePolicial | None:
        stmt = select(UnidadePolicialModel).where(
            UnidadePolicialModel.codigo_unidade == codigo_unidade.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[UnidadePolicial]:
        stmt = select(UnidadePolicialModel).order_by(UnidadePolicialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[UnidadePolicial]:
        normalized = municipio.strip().lower()
        stmt = (
            select(UnidadePolicialModel)
            .where(func.lower(UnidadePolicialModel.municipio) == normalized)
            .order_by(UnidadePolicialModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusUnidadePolicial) -> list[UnidadePolicial]:
        stmt = (
            select(UnidadePolicialModel)
            .where(UnidadePolicialModel.status == status.value)
            .order_by(UnidadePolicialModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, unidade_id: UUID) -> bool:
        model = await self.session.get(UnidadePolicialModel, unidade_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"UND/{year}/"
        stmt = (
            select(func.count())
            .select_from(UnidadePolicialModel)
            .where(UnidadePolicialModel.codigo_unidade.like(f"{prefix}%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"{prefix}{count + 1:05d}"

    @staticmethod
    def _to_domain(model: UnidadePolicialModel) -> UnidadePolicial:
        return UnidadePolicial(
            id=model.id,
            codigo_unidade=model.codigo_unidade,
            nome=model.nome,
            tipo=TipoUnidadePolicial(model.tipo),
            municipio=model.municipio,
            provincia=model.provincia,
            endereco=model.endereco,
            comandante=model.comandante,
            data_ativacao=model.data_ativacao,
            status=StatusUnidadePolicial(model.status),
            telefone=model.telefone,
            email=model.email,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
