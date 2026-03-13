from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import func, select
from app.core.bridges.identity_bridge import BIEventRecord, BIRecord, CitizenFUC
from apps.backend.app.modules.governance.statistics.integrations.base_data_source import BaseDataSource

class IdentidadeDataSource(BaseDataSource):
    """Metricas do modulo Identidade Civil via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        start, next_month = self._month_window(data_ref)
        start_dt = datetime.combine(start, datetime.min.time())
        next_month_dt = datetime.combine(next_month, datetime.min.time())
        cidadaos_ativos = int(await self._scalar(select(func.count()).select_from(CitizenFUC).where(CitizenFUC.is_active.is_(True)), 0))
        obitos_registrados = int(await self._scalar(select(func.count()).select_from(CitizenFUC).where(self._status_in_ci(CitizenFUC.vital_status, ('deceased', 'obito', 'morto'))), 0))
        documentos_bi_ativos = int(await self._scalar(select(func.count()).select_from(BIRecord).where(self._status_in_ci(BIRecord.status, ('active', 'ativo'))), 0))
        eventos_identidade_mes = int(await self._scalar(select(func.count()).select_from(BIEventRecord).where(BIEventRecord.timestamp >= start_dt, BIEventRecord.timestamp < next_month_dt), 0))
        return {'cidadaos_ativos': cidadaos_ativos, 'obitos_registrados': obitos_registrados, 'documentos_bi_ativos': documentos_bi_ativos, 'eventos_identidade_mes': eventos_identidade_mes}