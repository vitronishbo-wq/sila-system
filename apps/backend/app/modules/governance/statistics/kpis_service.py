from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.statistics.application.services.statistics_service import (
    StatisticsService,
)
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.statistics_repository import (
    StatisticsRepository,
)
from apps.backend.app.modules.governance.statistics.integrations.data_sources import DataSources


class KPIService:
    """Faixada de KPIs para dashboards executivos."""

    def __init__(
        self,
        db: AsyncSession | None = None,
        stats_service: StatisticsService | None = None,
        **_: Any,
    ):
        self.db = db
        self.stats_service = stats_service
        if self.stats_service is None and self.db is not None:
            repository = StatisticsRepository(self.db)
            sources = DataSources.from_session(self.db).as_dict()
            self.stats_service = StatisticsService(repository, data_sources=sources)

    async def get_dashboard_kpis(self) -> dict[str, Any]:
        if not self.stats_service:
            return {
                "generated_at": datetime.utcnow().isoformat(),
                "message": "StatisticsService nao configurado",
            }
        return await self.stats_service.get_dashboard_kpis()

    async def get_growth_metrics(self, days: int = 30) -> dict[str, Any]:
        """Metrica simples de variacao do volume de atendimento entre dois periodos."""
        if not self.stats_service:
            return {"periodo_dias": days, "growth_percent": 0.0}
        end_ref = date.today()
        current_ref = end_ref
        previous_ref = end_ref - timedelta(days=days)
        current = await self.stats_service.get_dashboard_kpis(current_ref)
        previous = await self.stats_service.get_dashboard_kpis(previous_ref)
        current_volume = self._sum_key_contains(current, ("total", "ativos", "mes"))
        previous_volume = self._sum_key_contains(previous, ("total", "ativos", "mes"))
        if previous_volume <= 0:
            growth = 100.0 if current_volume > 0 else 0.0
        else:
            growth = (current_volume - previous_volume) / previous_volume * 100
        return {
            "periodo_dias": days,
            "volume_atual": round(current_volume, 2),
            "volume_periodo_anterior": round(previous_volume, 2),
            "growth_percent": round(growth, 2),
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def _sum_key_contains(payload: dict[str, Any], fragments: tuple[str, ...]) -> float:
        total = 0.0
        for key, value in payload.items():
            if not isinstance(value, (int, float)):
                continue
            if any(fragment in key for fragment in fragments):
                total += float(value)
        return total
