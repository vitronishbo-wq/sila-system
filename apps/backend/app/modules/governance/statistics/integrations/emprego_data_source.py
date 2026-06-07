from __future__ import annotations

from datetime import date

from sqlalchemy import func, select

from apps.backend.app.core.bridges.society_statistics_models_bridge import (
    CandidatoModel,
    ContratoModel,
    OfertaModel,
)
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import (
    BaseDataSource,
)


class EmpregoDataSource(BaseDataSource):
    """Metricas do modulo Emprego via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        del data_ref
        candidatos_ativos = int(
            await self._scalar(
                select(func.count())
                .select_from(CandidatoModel)
                .where(self._status_in_ci(CandidatoModel.status, ("ativo",))),
                0,
            )
        )
        candidatos_colocados = int(
            await self._scalar(
                select(func.count())
                .select_from(CandidatoModel)
                .where(self._status_in_ci(CandidatoModel.status, ("colocado", "concluida"))),
                0,
            )
        )
        ofertas_abertas = int(
            await self._scalar(
                select(func.count())
                .select_from(OfertaModel)
                .where(self._status_in_ci(OfertaModel.status, ("aberta", "ativo", "pendente"))),
                0,
            )
        )
        contratos_ativos = int(
            await self._scalar(
                select(func.count())
                .select_from(ContratoModel)
                .where(self._status_in_ci(ContratoModel.status, ("ativo", "active", "concluida"))),
                0,
            )
        )
        taxa_colocacao = (
            round(candidatos_colocados / candidatos_ativos * 100, 2)
            if candidatos_ativos > 0
            else 0.0
        )
        return {
            "candidatos_ativos": candidatos_ativos,
            "candidatos_colocados": candidatos_colocados,
            "ofertas_abertas": ofertas_abertas,
            "contratos_ativos": contratos_ativos,
            "taxa_colocacao": taxa_colocacao,
        }
