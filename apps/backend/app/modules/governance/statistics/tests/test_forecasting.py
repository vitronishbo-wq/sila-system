from apps.backend.app.modules.governance.statistics.application.services.forecasting_service import (
    ForecastingService,
)


def test_moving_average_and_trend():
    svc = ForecastingService()
    series = [1, 2, 3, 4, 5]
    ma = svc.forecast_moving_average(series, window=3)
    assert len(ma) == len(series)
    assert svc.detect_trend(series) == "up"
