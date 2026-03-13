from __future__ import annotations
from datetime import date
from sqlalchemy import func, select
from app.core.bridges.society_statistics_models_bridge import AppointmentModel, InternamentoModel, VaccineDoseModel
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class SaudeDataSource(BaseDataSource):
    """Metricas do modulo Saude via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        start, next_month = self._month_window(data_ref)
        atendimentos_mes = int(await self._scalar(select(func.count()).select_from(AppointmentModel).where(AppointmentModel.appointment_date >= start, AppointmentModel.appointment_date < next_month), 0))
        atendimentos_concluidos_mes = int(await self._scalar(select(func.count()).select_from(AppointmentModel).where(AppointmentModel.appointment_date >= start, AppointmentModel.appointment_date < next_month, self._status_in_ci(AppointmentModel.status, ('completed', 'concluida', 'realizada'))), 0))
        vacinas_aplicadas_mes = int(await self._scalar(select(func.count()).select_from(VaccineDoseModel).where(VaccineDoseModel.application_date >= start, VaccineDoseModel.application_date < next_month, self._status_in_ci(VaccineDoseModel.status, ('aplicada', 'applied', 'administered'))), 0))
        internamentos_ativos = int(await self._scalar(select(func.count()).select_from(InternamentoModel).where(self._status_in_ci(InternamentoModel.status, ('admitted', 'under_observation', 'ativo', 'internado'))), 0))
        taxa_conclusao = round(atendimentos_concluidos_mes / atendimentos_mes * 100, 2) if atendimentos_mes > 0 else 0.0
        return {'atendimentos_mes': atendimentos_mes, 'atendimentos_concluidos_mes': atendimentos_concluidos_mes, 'vacinas_aplicadas_mes': vacinas_aplicadas_mes, 'internamentos_ativos': internamentos_ativos, 'taxa_conclusao_atendimentos': taxa_conclusao}