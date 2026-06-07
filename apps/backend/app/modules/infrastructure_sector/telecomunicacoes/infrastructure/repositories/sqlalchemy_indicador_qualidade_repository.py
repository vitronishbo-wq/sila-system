from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.indicador_qualidade_repository_port import (
    IndicadorQualidadeRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import (
    StatusIndicadorQualidade,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.indicador_qualidade import (
    IndicadorQualidade,
)
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.indicador_qualidade_model import (
    IndicadorQualidadeModel,
)


class SQLAlchemyIndicadorQualidadeRepository(IndicadorQualidadeRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, indicador: IndicadorQualidade) -> IndicadorQualidade:
        model = await self.session.get(IndicadorQualidadeModel, indicador.id)
        if not model:
            model = IndicadorQualidadeModel(id=indicador.id)
            self.session.add(model)
        model.codigo_indicador = indicador.codigo_indicador
        model.operadora_id = indicador.operadora_id
        model.referencia_ano = indicador.referencia_ano
        model.referencia_mes = indicador.referencia_mes
        model.total_medicoes = indicador.total_medicoes
        model.disponibilidade_media_percentual = indicador.disponibilidade_media_percentual
        model.latencia_media_ms = indicador.latencia_media_ms
        model.jitter_medio_ms = indicador.jitter_medio_ms
        model.perda_pacotes_media_percentual = indicador.perda_pacotes_media_percentual
        model.conformidade_percentual = indicador.conformidade_percentual
        model.data_calculo = indicador.data_calculo
        model.status = indicador.status.value
        model.observacoes = indicador.observacoes
        model.ativo = indicador.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, indicador_id: UUID) -> IndicadorQualidade | None:
        model = await self.session.get(IndicadorQualidadeModel, indicador_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_indicador: str) -> IndicadorQualidade | None:
        stmt = select(IndicadorQualidadeModel).where(
            IndicadorQualidadeModel.codigo_indicador == codigo_indicador.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_operadora_periodo(
        self, operadora_id: UUID, referencia_ano: int, referencia_mes: int
    ) -> IndicadorQualidade | None:
        stmt = (
            select(IndicadorQualidadeModel)
            .where(
                IndicadorQualidadeModel.operadora_id == operadora_id,
                IndicadorQualidadeModel.referencia_ano == referencia_ano,
                IndicadorQualidadeModel.referencia_mes == referencia_mes,
            )
            .limit(1)
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[IndicadorQualidade]:
        stmt = select(IndicadorQualidadeModel).order_by(
            IndicadorQualidadeModel.referencia_ano.desc(),
            IndicadorQualidadeModel.referencia_mes.desc(),
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_operadora(self, operadora_id: UUID) -> list[IndicadorQualidade]:
        stmt = (
            select(IndicadorQualidadeModel)
            .where(IndicadorQualidadeModel.operadora_id == operadora_id)
            .order_by(
                IndicadorQualidadeModel.referencia_ano.desc(),
                IndicadorQualidadeModel.referencia_mes.desc(),
            )
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusIndicadorQualidade) -> list[IndicadorQualidade]:
        stmt = (
            select(IndicadorQualidadeModel)
            .where(IndicadorQualidadeModel.status == status.value)
            .order_by(
                IndicadorQualidadeModel.referencia_ano.desc(),
                IndicadorQualidadeModel.referencia_mes.desc(),
            )
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, indicador_id: UUID) -> bool:
        model = await self.session.get(IndicadorQualidadeModel, indicador_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(IndicadorQualidadeModel)
            .where(IndicadorQualidadeModel.codigo_indicador.like(f"IND/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"IND/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: IndicadorQualidadeModel) -> IndicadorQualidade:
        return IndicadorQualidade(
            id=model.id,
            codigo_indicador=model.codigo_indicador,
            operadora_id=model.operadora_id,
            referencia_ano=model.referencia_ano,
            referencia_mes=model.referencia_mes,
            total_medicoes=model.total_medicoes,
            disponibilidade_media_percentual=float(model.disponibilidade_media_percentual),
            latencia_media_ms=float(model.latencia_media_ms),
            jitter_medio_ms=float(model.jitter_medio_ms),
            perda_pacotes_media_percentual=float(model.perda_pacotes_media_percentual),
            conformidade_percentual=float(model.conformidade_percentual),
            data_calculo=model.data_calculo,
            status=StatusIndicadorQualidade(model.status),
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
