def test_run_report_placeholder():
    # placeholder test for report runner
    from app.modules.bi.application.services.analytics_service import AnalyticsService

    class FakeRepo:
        def get(self, id):
            return {"id": id, "query": "select 1"}

    svc = AnalyticsService(FakeRepo())
    res = svc.run_report(1, {})
    assert res["report"]["id"] == 1
