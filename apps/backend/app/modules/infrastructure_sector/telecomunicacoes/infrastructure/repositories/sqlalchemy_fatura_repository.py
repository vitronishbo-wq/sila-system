from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.fatura_repository_port import (
    FaturaRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusFaturaTelecom,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.fatura_telecom import (
    FaturaTelecom,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.fatura_model import (
    FaturaTelecomModel,
)


class SQLAlchemyFaturaRepository(FaturaRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, fatura: FaturaTelecom) -> FaturaTelecom:
        model = await self.session.get(FaturaTelecomModel, fatura.id)
        if not model:
            model = FaturaTelecomModel(id=fatura.id)
            self.session.add(model)
        model.numero_fatura = fatura.numero_fatura
        model.assinante_id = fatura.assinante_id
        model.referencia = fatura.referencia
        model.consumo_total_gb = fatura.consumo_total_gb
        model.franquia_gb = fatura.franquia_gb
        model.excedente_gb = fatura.excedente_gb
        model.valor_plano = fatura.valor_plano
        model.valor_excedente = fatura.valor_excedente
        model.valor_total = fatura.valor_total
        model.data_emissao = fatura.data_emissao
        model.data_vencimento = fatura.data_vencimento
        model.status = fatura.status.value
        model.data_pagamento = fatura.data_pagamento
        model.valor_pago = fatura.valor_pago
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, fatura_id: UUID) -> FaturaTelecom | None:
        model = await self.session.get(FaturaTelecomModel, fatura_id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_fatura: str) -> FaturaTelecom | None:
        stmt = select(FaturaTelecomModel).where(
            FaturaTelecomModel.numero_fatura == numero_fatura.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_assinante(self, assinante_id: UUID) -> list[FaturaTelecom]:
        stmt = (
            select(FaturaTelecomModel)
            .where(FaturaTelecomModel.assinante_id == assinante_id)
            .order_by(FaturaTelecomModel.data_emissao.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_all(self) -> list[FaturaTelecom]:
        stmt = select(FaturaTelecomModel).order_by(FaturaTelecomModel.data_emissao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_numero(self) -> str:
        year = date.today().year
        stmt = (
            select(func.count())
            .select_from(FaturaTelecomModel)
            .where(FaturaTelecomModel.numero_fatura.like(f"FAT/{year}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"FAT/{year}/{count + 1:06d}"

    @staticmethod
    def _to_domain(model: FaturaTelecomModel) -> FaturaTelecom:
        return FaturaTelecom(
            id=model.id,
            numero_fatura=model.numero_fatura,
            assinante_id=model.assinante_id,
            referencia=model.referencia,
            consumo_total_gb=Decimal(model.consumo_total_gb),
            franquia_gb=Decimal(model.franquia_gb),
            excedente_gb=Decimal(model.excedente_gb),
            valor_plano=Decimal(model.valor_plano),
            valor_excedente=Decimal(model.valor_excedente),
            valor_total=Decimal(model.valor_total),
            data_emissao=model.data_emissao,
            data_vencimento=model.data_vencimento,
            status=StatusFaturaTelecom(model.status),
            data_pagamento=model.data_pagamento,
            valor_pago=Decimal(model.valor_pago) if model.valor_pago is not None else None,
        )
