from __future__ import annotations
from datetime import date
from sqlalchemy import func, select
from apps.backend.app.domain.bridges.society_statistics_models_bridge import MatriculaModel, TurmaModel
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class EducacaoDataSource(BaseDataSource):
    """Metricas do modulo Educacao via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        total_matriculas = int(await self._scalar(select(func.count()).select_from(MatriculaModel).where(MatriculaModel.data_matricula <= data_ref), 0))
        matriculas_ativas = int(await self._scalar(select(func.count()).select_from(MatriculaModel).where(MatriculaModel.data_matricula <= data_ref, self._status_in_ci(MatriculaModel.status, ('ativa', 'confirmada', 'aprovada'))), 0))
        turmas_ativas = int(await self._scalar(select(func.count()).select_from(TurmaModel).where(TurmaModel.ativa.is_(True)), 0))
        vagas_totais = int(await self._scalar(select(func.coalesce(func.sum(TurmaModel.capacidade), 0)).where(TurmaModel.ativa.is_(True)), 0))
        vagas_disponiveis = max(vagas_totais - matriculas_ativas, 0)
        taxa_ocupacao = round(matriculas_ativas / vagas_totais * 100, 2) if vagas_totais > 0 else 0.0
        return {'matriculas_total': total_matriculas, 'matriculas_ativas': matriculas_ativas, 'turmas_ativas': turmas_ativas, 'vagas_disponiveis': vagas_disponiveis, 'taxa_ocupacao': taxa_ocupacao}