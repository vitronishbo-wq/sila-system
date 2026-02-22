from datetime import datetime, timedelta

from app.modules.statistics.application.services.statistics_service import StatisticsService


def test_register_and_record_placeholder():
    class FakeRepo:
        def __init__(self):
            self.stats = []
            self.sync_session = self

        def add(self, obj):
            if not getattr(obj, "id", None):
                obj.id = 1
            self.stats.append(obj)

        def add_all(self, objects):
            self.stats.extend(objects)

        def flush(self):
            pass

        def query(self, model):
            return self

        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return self.stats[0] if self.stats else None

    svc = StatisticsService(FakeRepo())
    stat = svc.register_statistic("Test", "TEST_CODE")
    assert stat is not None
    now = datetime.utcnow()
    ts = svc.record_value(1, 10.0, now, now + timedelta(hours=1), {})
    assert ts is not None
