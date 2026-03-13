from typing import List

class ForecastingService:

    def forecast_moving_average(self, series: List[float], window: int=3) -> List[float]:
        if not series or window <= 0:
            return []
        res = []
        for i in range(len(series)):
            window_vals = series[max(0, i - window + 1):i + 1]
            res.append(sum(window_vals) / len(window_vals))
        return res

    def detect_trend(self, series: List[float]) -> str:
        if len(series) < 2:
            return 'stable'
        if series[-1] > series[0]:
            return 'up'
        if series[-1] < series[0]:
            return 'down'
        return 'stable'