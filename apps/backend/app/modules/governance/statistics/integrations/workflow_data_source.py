from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func, select

from apps.backend.app.modules.governance.statistics.integrations.base_data_source import (
    BaseDataSource,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_instance_model import (
    WorkflowInstanceModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import (
    WorkflowTaskModel,
)


class WorkflowDataSource(BaseDataSource):
    """Metricas do modulo Workflow via ORM."""

    async def collect_metrics(self, data_ref: date) -> dict[str, float | int]:
        start, next_month = self._month_window(data_ref)
        start_dt = datetime.combine(start, datetime.min.time())
        next_month_dt = datetime.combine(next_month, datetime.min.time())
        instancias_ativas = int(
            await self._scalar(
                select(func.count())
                .select_from(WorkflowInstanceModel)
                .where(self._status_in_ci(WorkflowInstanceModel.status, ("active", "ativo"))),
                0,
            )
        )
        instancias_concluidas_mes = int(
            await self._scalar(
                select(func.count())
                .select_from(WorkflowInstanceModel)
                .where(
                    self._status_in_ci(WorkflowInstanceModel.status, ("completed", "concluida")),
                    WorkflowInstanceModel.completed_at.is_not(None),
                    WorkflowInstanceModel.completed_at >= start_dt,
                    WorkflowInstanceModel.completed_at < next_month_dt,
                ),
                0,
            )
        )
        tasks_pendentes = int(
            await self._scalar(
                select(func.count())
                .select_from(WorkflowTaskModel)
                .where(self._status_in_ci(WorkflowTaskModel.status, ("pending", "pendente"))),
                0,
            )
        )
        duration_expr = (
            func.extract(
                "epoch", WorkflowInstanceModel.completed_at - WorkflowInstanceModel.started_at
            )
            / 3600.0
        )
        tempo_medio_horas = self._as_float(
            await self._scalar(
                select(func.avg(duration_expr)).where(
                    WorkflowInstanceModel.completed_at.is_not(None),
                    WorkflowInstanceModel.started_at.is_not(None),
                ),
                0,
            )
        )
        return {
            "instancias_ativas": instancias_ativas,
            "instancias_concluidas_mes": instancias_concluidas_mes,
            "tasks_pendentes": tasks_pendentes,
            "tempo_medio_conclusao_horas": round(tempo_medio_horas, 2),
        }
