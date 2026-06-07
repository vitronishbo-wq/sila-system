from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from apps.backend.app.modules.governance.statistics.application.ports.statistics_repository_port import (
    StatisticsRepositoryPort,
)
from apps.backend.app.modules.governance.statistics.infrastructure.models.statistic_model import (
    StatisticModel,
)
from apps.backend.app.modules.governance.statistics.infrastructure.models.timeseries_model import (
    TimeSeriesModel,
)


class StatisticsService:
    """Service layer for Statistics business logic"""

    def __init__(
        self, repository: StatisticsRepositoryPort, data_sources: dict[str, Any] | None = None
    ):
        self.repo = repository
        self.data_sources = data_sources or {}

    def register_statistic(
        self,
        name: str,
        code: str,
        description: str = None,
        unit: str = None,
        source_module: str = None,
    ) -> dict[str, Any]:
        """Register a new statistic with validation"""
        if self.repo.statistic_exists(code):
            raise ValueError(f"Statistic with code '{code}' already exists")
        if not name or not code:
            raise ValueError("Name and code are required")
        stat = self.repo.create_statistic(
            name=name, code=code, description=description, unit=unit, source_module=source_module
        )
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "unit": stat.unit,
            "source_module": stat.source_module,
            "created_at": stat.created_at.isoformat() if stat.created_at else None,
        }

    def get_statistic_details(self, statistic_id: int) -> dict[str, Any] | None:
        """Get detailed information about a statistic"""
        stat = self.repo.get_statistic(statistic_id)
        if not stat:
            return None
        count = self.repo.count_timeseries(statistic_id)
        latest = self.repo.get_latest(statistic_id)
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "description": stat.description,
            "unit": stat.unit,
            "source_module": stat.source_module,
            "created_at": stat.created_at.isoformat() if stat.created_at else None,
            "total_records": count,
            "latest_value": {
                "value": latest.value,
                "period_start": latest.period_start.isoformat() if latest.period_start else None,
            }
            if latest
            else None,
        }

    def list_all_statistics(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """List all statistics with pagination"""
        stats = self.repo.list_statistics(skip=skip, limit=limit)
        return [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "unit": s.unit,
                "source_module": s.source_module,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in stats
        ]

    def list_statistics_by_module(self, module: str) -> list[dict[str, Any]]:
        """List all statistics for a specific module"""
        stats = self.repo.list_statistics_by_module(module)
        return [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "unit": s.unit,
                "source_module": s.source_module,
            }
            for s in stats
        ]

    def update_statistic(self, statistic_id: int, **kwargs) -> dict[str, Any] | None:
        """Update a statistic"""
        stat = self.repo.update_statistic(statistic_id, **kwargs)
        if not stat:
            return None
        return {
            "id": stat.id,
            "name": stat.name,
            "code": stat.code,
            "unit": stat.unit,
            "source_module": stat.source_module,
        }

    def delete_statistic(self, statistic_id: int) -> bool:
        """Delete a statistic and all associated data"""
        return self.repo.delete_statistic(statistic_id)

    def record_value(
        self,
        statistic_id: int,
        value: float,
        period_start: datetime,
        period_end: datetime | None = None,
        dimensions: dict[str, Any] = None,
    ) -> dict[str, Any]:
        """Record a new timeseries value with validation"""
        stat = self.repo.get_statistic(statistic_id)
        if not stat:
            raise ValueError(f"Statistic with ID {statistic_id} not found")
        try:
            float(value)
        except (ValueError, TypeError) as err:
            raise ValueError(f"Value must be numeric, got {type(value).__name__}") from err
        ts = self.repo.record_value(
            statistic_id=statistic_id,
            value=value,
            period_start=period_start,
            period_end=period_end,
            dimensions=dimensions,
        )
        return {
            "id": ts.id,
            "statistic_id": ts.statistic_id,
            "value": ts.value,
            "period_start": ts.period_start.isoformat() if ts.period_start else None,
            "period_end": ts.period_end.isoformat() if ts.period_end else None,
            "created_at": ts.created_at.isoformat() if ts.created_at else None,
        }

    def get_series(
        self,
        statistic_id: int,
        limit: int = 100,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Get timeseries values with optional date range filtering"""
        series = self.repo.get_series(
            statistic_id=statistic_id, limit=limit, start_date=start_date, end_date=end_date
        )
        return [
            {
                "id": ts.id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None,
                "period_end": ts.period_end.isoformat() if ts.period_end else None,
                "dimensions": ts.dimensions,
            }
            for ts in series
        ]

    def get_latest(self, statistic_id: int) -> dict[str, Any] | None:
        """Get the latest value for a statistic"""
        ts = self.repo.get_latest(statistic_id)
        if not ts:
            return None
        return {
            "id": ts.id,
            "value": ts.value,
            "period_start": ts.period_start.isoformat() if ts.period_start else None,
            "period_end": ts.period_end.isoformat() if ts.period_end else None,
            "dimensions": ts.dimensions,
        }

    def get_series_by_period(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> list[dict[str, Any]]:
        """Get timeseries values for a specific period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id, period_start=period_start, period_end=period_end
        )
        return [
            {
                "id": ts.id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None,
                "period_end": ts.period_end.isoformat() if ts.period_end else None,
            }
            for ts in series
        ]

    def bulk_record_values(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Record multiple values at once"""
        for record in records:
            if (
                "statistic_id" not in record
                or "value" not in record
                or "period_start" not in record
            ):
                raise ValueError("Each record must have statistic_id, value, and period_start")
        timeseries_list = self.repo.bulk_record_values(records)
        return [
            {
                "id": ts.id,
                "statistic_id": ts.statistic_id,
                "value": ts.value,
                "period_start": ts.period_start.isoformat() if ts.period_start else None,
            }
            for ts in timeseries_list
        ]

    def delete_timeseries(self, timeseries_id: int) -> bool:
        """Delete a timeseries value"""
        return self.repo.delete_timeseries(timeseries_id)

    def delete_series_by_period(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> dict[str, Any]:
        """Delete all timeseries values in a period"""
        count = self.repo.delete_series_by_period(
            statistic_id=statistic_id, period_start=period_start, period_end=period_end
        )
        return {
            "deleted_count": count,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
        }

    def calculate_average(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> float | None:
        """Calculate average value for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id, period_start=period_start, period_end=period_end
        )
        if not series:
            return None
        return sum(ts.value for ts in series) / len(series)

    def calculate_sum(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> float:
        """Calculate sum for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id, period_start=period_start, period_end=period_end
        )
        return sum(ts.value for ts in series) if series else 0.0

    def calculate_min_max(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> dict[str, float] | None:
        """Get min and max values for a period"""
        series = self.repo.get_series_by_period(
            statistic_id=statistic_id, period_start=period_start, period_end=period_end
        )
        if not series:
            return None
        values = [ts.value for ts in series]
        return {"min": min(values), "max": max(values)}

    def get_statistics_summary(self) -> dict[str, Any]:
        """Get summary statistics about all data"""
        total_stats = self.repo.count_statistics()
        return {"total_statistics": total_stats, "timestamp": datetime.now().isoformat()}

    async def collect_all_metrics(self, data_ref: date | None = None) -> dict[str, Any]:
        """Coleta métricas de todos os data sources configurados."""
        ref = data_ref or date.today()
        results: dict[str, Any] = {}
        for source_name, source in self.data_sources.items():
            if source is None:
                results[source_name] = {"status": "not_configured", "metrics_collected": 0}
                continue
            try:
                metrics = await source.collect_metrics(ref)
                persisted = await self._persist_metrics(source_name, metrics, ref)
                results[source_name] = {
                    "status": "success",
                    "metrics_collected": len(metrics),
                    "persisted": persisted,
                }
            except Exception as exc:
                results[source_name] = {
                    "status": "error",
                    "metrics_collected": 0,
                    "error": str(exc),
                }
        return results

    async def get_dashboard_kpis(self, data_ref: date | None = None) -> dict[str, Any]:
        """Consolida KPIs atuais de todas as fontes configuradas."""
        ref = data_ref or date.today()
        dashboard: dict[str, Any] = {
            "reference_date": ref.isoformat(),
            "generated_at": datetime.utcnow().isoformat(),
        }
        for source_name, source in self.data_sources.items():
            if source is None:
                continue
            try:
                metrics = await source.collect_metrics(ref)
                for metric_name, value in metrics.items():
                    dashboard[f"{source_name}.{metric_name}"] = value
            except Exception as exc:
                dashboard[f"{source_name}.error"] = str(exc)
        return dashboard

    async def _persist_metrics(self, source_name: str, metrics: dict[str, Any], ref: date) -> bool:
        """Persiste métricas em statistics/statistics_timeseries quando houver sessão async."""
        session = getattr(self.repo, "session", None)
        if session is None or not hasattr(session, "execute"):
            return False
        period_start = datetime.combine(ref, time.min)
        period_end = datetime.combine(ref, time.max)
        try:
            for metric_name, raw_value in metrics.items():
                numeric_value = self._coerce_metric_value(raw_value)
                if numeric_value is None:
                    continue
                code = f"{source_name}.{metric_name}"
                statement = select(StatisticModel).where(StatisticModel.code == code)
                existing = await session.execute(statement)
                statistic = existing.scalars().first()
                if not statistic:
                    statistic = StatisticModel(
                        name=code,
                        code=code,
                        description=f"Coleta automatica de {code}",
                        unit=self._infer_unit(metric_name),
                        source_module=source_name,
                    )
                    session.add(statistic)
                    await session.flush()
                point = TimeSeriesModel(
                    statistic_id=statistic.id,
                    value=numeric_value,
                    period_start=period_start,
                    period_end=period_end,
                    dimensions={"source": source_name},
                )
                session.add(point)
            await session.flush()
            return True
        except SQLAlchemyError:
            return False

    @staticmethod
    def _coerce_metric_value(value: Any) -> float | None:
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        return None

    @staticmethod
    def _infer_unit(metric_name: str) -> str:
        lowered = metric_name.lower()
        if "taxa" in lowered:
            return "percentual"
        if "tempo" in lowered:
            return "horas"
        if "renda" in lowered:
            return "moeda"
        return "contagem"
