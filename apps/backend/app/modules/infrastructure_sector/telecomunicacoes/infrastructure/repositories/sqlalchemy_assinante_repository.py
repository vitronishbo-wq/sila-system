from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import (
    AssinanteRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusAssinante,
    TipoPlano,
    TipoServico,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.assinante import (
    Assinante,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.assinante_model import (
    AssinanteModel,
)


class SQLAlchemyAssinanteRepository(AssinanteRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, assinante: Assinante) -> Assinante:
        model = await self.session.get(AssinanteModel, assinante.id)
        if not model:
            model = AssinanteModel(id=assinante.id)
            self.session.add(model)
        model.codigo_assinante = assinante.codigo_assinante
        model.operadora_id = assinante.operadora_id
        model.tipo_plano = assinante.tipo_plano.value
        model.servico_principal = assinante.servico_principal.value
        model.data_adesao = assinante.data_adesao
        model.status = assinante.status.value
        model.municipio = assinante.municipio
        model.provincia = assinante.provincia
        model.nome = assinante.nome
        model.citizen_id = assinante.citizen_id
        model.telefone_contato = assinante.telefone_contato
        model.email_contato = assinante.email_contato
        model.contrato_numero = assinante.contrato_numero
        model.valor_mensal = assinante.valor_mensal
        model.observacoes = assinante.observacoes
        model.ativo = assinante.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, assinante_id: UUID) -> Assinante | None:
        model = await self.session.get(AssinanteModel, assinante_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_assinante: str) -> Assinante | None:
        stmt = select(AssinanteModel).where(
            AssinanteModel.codigo_assinante == codigo_assinante.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID) -> Assinante | None:
        stmt = (
            select(AssinanteModel)
            .where(AssinanteModel.citizen_id == citizen_id)
            .order_by(AssinanteModel.data_adesao.desc())
            .limit(1)
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Assinante]:
        stmt = select(AssinanteModel).order_by(AssinanteModel.data_adesao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[Assinante]:
        stmt = (
            select(AssinanteModel)
            .where(AssinanteModel.operadora_id == operadora_id)
            .order_by(AssinanteModel.data_adesao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Assinante]:
        normalized = municipio.strip().lower()
        stmt = (
            select(AssinanteModel)
            .where(func.lower(AssinanteModel.municipio) == normalized)
            .order_by(AssinanteModel.data_adesao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_ativos(self) -> list[Assinante]:
        stmt = (
            select(AssinanteModel)
            .where(
                AssinanteModel.ativo.is_(True), AssinanteModel.status == StatusAssinante.ATIVO.value
            )
            .order_by(AssinanteModel.data_adesao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, assinante_id: UUID) -> bool:
        model = await self.session.get(AssinanteModel, assinante_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(AssinanteModel)
            .where(AssinanteModel.codigo_assinante.like(f"ASS/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"ASS/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: AssinanteModel) -> Assinante:
        return Assinante(
            id=model.id,
            codigo_assinante=model.codigo_assinante,
            operadora_id=model.operadora_id,
            tipo_plano=TipoPlano(model.tipo_plano),
            servico_principal=TipoServico(model.servico_principal),
            data_adesao=model.data_adesao,
            status=StatusAssinante(model.status),
            municipio=model.municipio,
            provincia=model.provincia,
            nome=model.nome,
            citizen_id=model.citizen_id,
            telefone_contato=model.telefone_contato,
            email_contato=model.email_contato,
            contrato_numero=model.contrato_numero,
            valor_mensal=float(model.valor_mensal) if model.valor_mensal is not None else None,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
