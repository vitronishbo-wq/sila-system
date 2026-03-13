from __future__ import annotations
from datetime import datetime, timedelta
from app.modules.governance.statistics.application.services.statistics_service import StatisticsService

def test_register_and_record_placeholder():

    class Obj:

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class FakeRepo:

        def __init__(self):
            self._stats = {}
            self._timeseries = []
            self._next_stat_id = 1
            self._next_ts_id = 1

        def statistic_exists(self, code: str) -> bool:
            return any((item.code == code for item in self._stats.values()))

        def create_statistic(self, name: str, code: str, description=None, unit=None, source_module=None):
            stat = Obj(id=self._next_stat_id, name=name, code=code, description=description, unit=unit, source_module=source_module, created_at=datetime.utcnow())
            self._stats[stat.id] = stat
            self._next_stat_id += 1
            return stat

        def get_statistic(self, statistic_id: int):
            return self._stats.get(statistic_id)

        def record_value(self, statistic_id: int, value: float, period_start: datetime, period_end=None, dimensions=None):
            ts = Obj(id=self._next_ts_id, statistic_id=statistic_id, value=float(value), period_start=period_start, period_end=period_end, dimensions=dimensions, created_at=datetime.utcnow())
            self._timeseries.append(ts)
            self._next_ts_id += 1
            return ts
    svc = StatisticsService(FakeRepo())
    stat = svc.register_statistic('Test', 'TEST_CODE')
    assert stat['code'] == 'TEST_CODE'
    now = datetime.utcnow()
    ts = svc.record_value(1, 10.0, now, now + timedelta(hours=1), {})
    assert ts['statistic_id'] == 1
    assert ts['value'] == 10.0