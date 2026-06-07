from datetime import datetime
from typing import Any, Protocol


class StatisticsRepositoryPort(Protocol):
    def statistic_exists(self, code: str) -> bool: ...

    def create_statistic(
        self,
        name: str,
        code: str,
        description: str = None,
        unit: str = None,
        source_module: str = None,
    ) -> Any: ...

    def get_statistic(self, statistic_id: int) -> Any | None: ...

    def get_statistic_by_code(self, code: str) -> Any | None: ...

    def list_statistics(self, skip: int = 0, limit: int = 100) -> list[Any]: ...

    def list_statistics_by_module(self, module: str) -> list[Any]: ...

    def update_statistic(self, statistic_id: int, **kwargs) -> Any | None: ...

    def delete_statistic(self, statistic_id: int) -> bool: ...

    def count_timeseries(self, statistic_id: int) -> int: ...

    def record_value(
        self,
        statistic_id: int,
        value: float,
        period_start: datetime,
        period_end: datetime | None = None,
        dimensions: dict[str, Any] = None,
    ) -> Any: ...

    def get_series(
        self,
        statistic_id: int,
        limit: int = 100,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[Any]: ...

    def get_latest(self, statistic_id: int) -> Any | None: ...

    def get_series_by_period(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> list[Any]: ...

    def bulk_record_values(self, records: list[dict[str, Any]]) -> list[Any]: ...

    def delete_timeseries(self, timeseries_id: int) -> bool: ...

    def calculate_average(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> float | None: ...

    def calculate_sum(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> float: ...

    def calculate_min_max(
        self, statistic_id: int, period_start: datetime, period_end: datetime
    ) -> dict[str, float] | None: ...

    def get_statistics_summary(self) -> dict[str, Any]: ...
