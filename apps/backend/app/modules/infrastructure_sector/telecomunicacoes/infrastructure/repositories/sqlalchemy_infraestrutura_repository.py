from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.infraestrutura_repository_port import (
    InfraestruturaRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.infraestrutura_telco import (
    InfraestruturaTelco,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.infraestrutura_telco_model import (
    InfraestruturaTelcoModel,
)


class SQLAlchemyInfraestruturaRepository(InfraestruturaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, infraestrutura: InfraestruturaTelco) -> InfraestruturaTelco:
        model = await self.session.get(InfraestruturaTelcoModel, infraestrutura.id)
        if not model:
            model = InfraestruturaTelcoModel(id=infraestrutura.id)
            self.session.add(model)
        model.codigo_infra = infraestrutura.codigo_infra
        model.operadora_id = infraestrutura.operadora_id
        model.tipo = infraestrutura.tipo.value
        model.identificador = infraestrutura.identificador
        model.municipio = infraestrutura.municipio
        model.provincia = infraestrutura.provincia
        model.data_implantacao = infraestrutura.data_implantacao
        model.status = infraestrutura.status.value
        model.latitude = infraestrutura.latitude
        model.longitude = infraestrutura.longitude
        model.capacidade = infraestrutura.capacidade
        model.observacoes = infraestrutura.observacoes
        model.ativo = infraestrutura.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, infraestrutura_id: UUID) -> InfraestruturaTelco | None:
        model = await self.session.get(InfraestruturaTelcoModel, infraestrutura_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_infra: str) -> InfraestruturaTelco | None:
        stmt = select(InfraestruturaTelcoModel).where(
            InfraestruturaTelcoModel.codigo_infra == codigo_infra.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[InfraestruturaTelco]:
        stmt = select(InfraestruturaTelcoModel).order_by(
            InfraestruturaTelcoModel.data_implantacao.desc()
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[InfraestruturaTelco]:
        stmt = (
            select(InfraestruturaTelcoModel)
            .where(InfraestruturaTelcoModel.operadora_id == operadora_id)
            .order_by(InfraestruturaTelcoModel.data_implantacao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[InfraestruturaTelco]:
        normalized = municipio.strip().lower()
        stmt = (
            select(InfraestruturaTelcoModel)
            .where(func.lower(InfraestruturaTelcoModel.municipio) == normalized)
            .order_by(InfraestruturaTelcoModel.data_implantacao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_ativas(self) -> list[InfraestruturaTelco]:
        stmt = (
            select(InfraestruturaTelcoModel)
            .where(
                InfraestruturaTelcoModel.ativo.is_(True),
                InfraestruturaTelcoModel.status == StatusInfraestrutura.ATIVA.value,
            )
            .order_by(InfraestruturaTelcoModel.data_implantacao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, infraestrutura_id: UUID) -> bool:
        model = await self.session.get(InfraestruturaTelcoModel, infraestrutura_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(InfraestruturaTelcoModel)
            .where(InfraestruturaTelcoModel.codigo_infra.like(f"INF/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"INF/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: InfraestruturaTelcoModel) -> InfraestruturaTelco:
        return InfraestruturaTelco(
            id=model.id,
            codigo_infra=model.codigo_infra,
            operadora_id=model.operadora_id,
            tipo=TipoInfraestrutura(model.tipo),
            identificador=model.identificador,
            municipio=model.municipio,
            provincia=model.provincia,
            data_implantacao=model.data_implantacao,
            status=StatusInfraestrutura(model.status),
            latitude=float(model.latitude) if model.latitude is not None else None,
            longitude=float(model.longitude) if model.longitude is not None else None,
            capacidade=model.capacidade,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
