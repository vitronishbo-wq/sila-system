from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.desporto.application.ports.contrato_repository_port import ContratoRepositoryPort
from app.modules.society.desporto.domain.enums import StatusContrato, TipoContrato
from app.modules.society.desporto.domain.models.contrato import Contrato
from app.modules.society.desporto.infrastructure.models.contrato_model import ContratoModel

class SQLAlchemyContratoRepository(ContratoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, contrato: Contrato) -> Contrato:
        model = await self.session.get(ContratoModel, contrato.id)
        if not model:
            model = ContratoModel(id=contrato.id)
            self.session.add(model)
        model.codigo_contrato = contrato.codigo_contrato
        model.atleta_id = contrato.atleta_id
        model.clube_id = contrato.clube_id
        model.tipo = contrato.tipo.value
        model.data_inicio = contrato.data_inicio
        model.data_fim = contrato.data_fim
        model.salario_mensal = contrato.salario_mensal
        model.clausula_rescisao = contrato.clausula_rescisao
        model.status = contrato.status.value
        model.ativo = contrato.ativo
        model.observacoes = contrato.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, contrato_id: UUID) -> Contrato | None:
        model = await self.session.get(ContratoModel, contrato_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_contrato: str) -> Contrato | None:
        stmt = select(ContratoModel).where(ContratoModel.codigo_contrato == codigo_contrato.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Contrato]:
        stmt = select(ContratoModel).order_by(ContratoModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_atleta(self, atleta_id: UUID) -> list[Contrato]:
        stmt = select(ContratoModel).where(ContratoModel.atleta_id == atleta_id).order_by(ContratoModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_clube(self, clube_id: UUID) -> list[Contrato]:
        stmt = select(ContratoModel).where(ContratoModel.clube_id == clube_id).order_by(ContratoModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoContrato) -> list[Contrato]:
        stmt = select(ContratoModel).where(ContratoModel.tipo == tipo.value).order_by(ContratoModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusContrato) -> list[Contrato]:
        stmt = select(ContratoModel).where(ContratoModel.status == status.value).order_by(ContratoModel.data_inicio.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, contrato_id: UUID) -> bool:
        model = await self.session.get(ContratoModel, contrato_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ContratoModel).where(ContratoModel.codigo_contrato.like(f'CTR/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'CTR/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ContratoModel) -> Contrato:
        return Contrato(id=model.id, codigo_contrato=model.codigo_contrato, atleta_id=model.atleta_id, clube_id=model.clube_id, tipo=TipoContrato(model.tipo), data_inicio=model.data_inicio, data_fim=model.data_fim, salario_mensal=Decimal(model.salario_mensal), clausula_rescisao=Decimal(model.clausula_rescisao) if model.clausula_rescisao is not None else None, status=StatusContrato(model.status), ativo=model.ativo, observacoes=model.observacoes)