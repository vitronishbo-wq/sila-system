from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import func, select
from apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class ServiceRequestsDataSource(BaseDataSource):
    """Metricas do modulo Service Requests via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        start, next_month = self._month_window(data_ref)
        start_dt = datetime.combine(start, datetime.min.time())
        next_month_dt = datetime.combine(next_month, datetime.min.time())
        requests_total_mes = int(await self._scalar(select(func.count()).select_from(ServiceRequestModel).where(ServiceRequestModel.created_at >= start_dt, ServiceRequestModel.created_at < next_month_dt), 0))
        requests_concluidas_mes = int(await self._scalar(select(func.count()).select_from(ServiceRequestModel).where(ServiceRequestModel.created_at >= start_dt, ServiceRequestModel.created_at < next_month_dt, self._status_in_ci(ServiceRequestModel.status, ('completed', 'concluida', 'fechado'))), 0))
        requests_pendentes = int(await self._scalar(select(func.count()).select_from(ServiceRequestModel).where(self._status_in_ci(ServiceRequestModel.status, ('submitted', 'under_review', 'in_progress', 'waiting_info', 'pending', 'draft', 'rascunho', 'em_analise'))), 0))
        requests_sla_violado = int(await self._scalar(select(func.count()).select_from(ServiceRequestModel).where(ServiceRequestModel.sla_breached.is_(True)), 0))
        taxa_conclusao = round(requests_concluidas_mes / requests_total_mes * 100, 2) if requests_total_mes > 0 else 0.0
        return {'requests_total_mes': requests_total_mes, 'requests_concluidas_mes': requests_concluidas_mes, 'requests_pendentes': requests_pendentes, 'requests_sla_violado': requests_sla_violado, 'taxa_conclusao_requests': taxa_conclusao}