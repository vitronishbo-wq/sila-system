from __future__ import annotations
from datetime import date
from sqlalchemy import func, select
from apps.backend.app.core.bridges.society_statistics_models_bridge import BeneficiarioModel, BeneficioModel, CadastroUnicoModel
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class AssistenciaDataSource(BaseDataSource):
    """Metricas do modulo Assistencia Social via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        del data_ref
        beneficiarios_ativos = int(await self._scalar(select(func.count()).select_from(BeneficiarioModel).where(BeneficiarioModel.ativo.is_(True), self._status_in_ci(BeneficiarioModel.situacao, ('ativo',))), 0))
        beneficios_ativos = int(await self._scalar(select(func.count()).select_from(BeneficioModel).where(self._status_in_ci(BeneficioModel.status, ('ativo', 'aprovado'))), 0))
        cadastros_ativos = int(await self._scalar(select(func.count()).select_from(CadastroUnicoModel).where(self._status_in_ci(CadastroUnicoModel.status, ('ativo',))), 0))
        familias_baixa_renda = int(await self._scalar(select(func.count()).select_from(CadastroUnicoModel).where(CadastroUnicoModel.renda_per_capita <= 250), 0))
        renda_media = self._as_float(await self._scalar(select(func.avg(CadastroUnicoModel.renda_per_capita)), 0))
        return {'beneficiarios_ativos': beneficiarios_ativos, 'beneficios_ativos': beneficios_ativos, 'cadastros_ativos': cadastros_ativos, 'familias_baixa_renda': familias_baixa_renda, 'renda_media_per_capita': round(renda_media, 2)}