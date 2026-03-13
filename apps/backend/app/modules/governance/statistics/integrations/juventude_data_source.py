from __future__ import annotations
from datetime import date
from sqlalchemy import func, select
from apps.backend.app.domain.bridges.society_statistics_models_bridge import JovemModel, ProgramaJuvenilModel
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class JuventudeDataSource(BaseDataSource):
    """Metricas do modulo Juventude via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        del data_ref
        total_jovens_ativos = int(await self._scalar(select(func.count()).select_from(JovemModel).where(JovemModel.ativo.is_(True)), 0))
        jovens_em_acompanhamento = int(await self._scalar(select(func.count()).select_from(JovemModel).where(JovemModel.ativo.is_(True), JovemModel.acompanhamento_psicossocial.is_(True)), 0))
        jovens_em_busca_emprego = int(await self._scalar(select(func.count()).select_from(JovemModel).where(JovemModel.ativo.is_(True), self._status_in_ci(JovemModel.situacao_ocupacional, ('desempregado', 'procura_emprego', 'nao_estuda_nao_trabalha'))), 0))
        programas_ativos = int(await self._scalar(select(func.count()).select_from(ProgramaJuvenilModel).where(ProgramaJuvenilModel.ativo.is_(True), self._status_in_ci(ProgramaJuvenilModel.status, ('ativo', 'inscricoes_abertas'))), 0))
        taxa_inclusao = round((total_jovens_ativos - jovens_em_busca_emprego) / total_jovens_ativos * 100, 2) if total_jovens_ativos > 0 else 0.0
        return {'jovens_ativos': total_jovens_ativos, 'jovens_em_acompanhamento': jovens_em_acompanhamento, 'jovens_em_busca_emprego': jovens_em_busca_emprego, 'programas_ativos': programas_ativos, 'taxa_inclusao_socioeconomica': taxa_inclusao}