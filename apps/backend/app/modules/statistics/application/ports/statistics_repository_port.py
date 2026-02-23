from typing import Protocol, List


class StatisticsRepositoryPort(Protocol):
    def register_statistic(self, statistic):
        ...

    def record_value(self, timeseries_point):
        ...

    def get_series(self, statistic_id: int, limit: int = 100) -> List:
        ...

    def get_latest(self, statistic_id: int):
        ...
