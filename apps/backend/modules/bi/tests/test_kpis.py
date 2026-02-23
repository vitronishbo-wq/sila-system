def test_calculate_kpi_placeholder():
    # placeholder: no DB access here, ensure function exists
    from app.modules.bi.application.services.kpi_service import KPIService

    class FakeRepo:
        def find_by_code(self, code):
            class M:
                value = 42

            return M()

    svc = KPIService(FakeRepo())
    assert svc.calculate_kpi("x") == 42.0
