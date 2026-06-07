from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.desporto.application.ports.transferencia_repository_port import (
    TransferenciaRepositoryPort,
)
from apps.backend.app.modules.society.desporto.domain.enums import StatusTransferencia
from apps.backend.app.modules.society.desporto.domain.models.transferencia import Transferencia
from apps.backend.app.modules.society.desporto.infrastructure.models.transferencia_model import (
    TransferenciaModel,
)


class SQLAlchemyTransferenciaRepository(TransferenciaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, transferencia: Transferencia) -> Transferencia:
        model = await self.session.get(TransferenciaModel, transferencia.id)
        if not model:
            model = TransferenciaModel(id=transferencia.id)
            self.session.add(model)
        model.codigo_transferencia = transferencia.codigo_transferencia
        model.atleta_id = transferencia.atleta_id
        model.clube_origem_id = transferencia.clube_origem_id
        model.clube_destino_id = transferencia.clube_destino_id
        model.data_solicitacao = transferencia.data_solicitacao
        model.data_conclusao = transferencia.data_conclusao
        model.valor_transferencia = transferencia.valor_transferencia
        model.status = transferencia.status.value
        model.ativo = transferencia.ativo
        model.observacoes = transferencia.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, transferencia_id: UUID) -> Transferencia | None:
        model = await self.session.get(TransferenciaModel, transferencia_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_transferencia: str) -> Transferencia | None:
        stmt = select(TransferenciaModel).where(
            TransferenciaModel.codigo_transferencia == codigo_transferencia.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Transferencia]:
        stmt = select(TransferenciaModel).order_by(TransferenciaModel.data_solicitacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_atleta(self, atleta_id: UUID) -> list[Transferencia]:
        stmt = (
            select(TransferenciaModel)
            .where(TransferenciaModel.atleta_id == atleta_id)
            .order_by(TransferenciaModel.data_solicitacao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusTransferencia) -> list[Transferencia]:
        stmt = (
            select(TransferenciaModel)
            .where(TransferenciaModel.status == status.value)
            .order_by(TransferenciaModel.data_solicitacao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, transferencia_id: UUID) -> bool:
        model = await self.session.get(TransferenciaModel, transferencia_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(TransferenciaModel)
            .where(TransferenciaModel.codigo_transferencia.like(f"TRF/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"TRF/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: TransferenciaModel) -> Transferencia:
        return Transferencia(
            id=model.id,
            codigo_transferencia=model.codigo_transferencia,
            atleta_id=model.atleta_id,
            clube_origem_id=model.clube_origem_id,
            clube_destino_id=model.clube_destino_id,
            data_solicitacao=model.data_solicitacao,
            data_conclusao=model.data_conclusao,
            valor_transferencia=Decimal(model.valor_transferencia)
            if model.valor_transferencia is not None
            else None,
            status=StatusTransferencia(model.status),
            ativo=model.ativo,
            observacoes=model.observacoes,
        )
