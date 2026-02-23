from typing import List


class KPIService:
    def __init__(self, metrics_repo):
        self.metrics_repo = metrics_repo

    def calculate_kpi(self, code: str) -> float:
        m = self.metrics_repo.find_by_code(code)
        if not m:
            return 0.0
        return float(m.value)

    def get_kpi_series(self, code: str, limit: int = 100) -> List:
        # naive: return last N metrics with code
        # In reality would aggregate by period
        return self.metrics_repo.session.query(self.metrics_repo.session.query.__self__.c).all()

    def aggregate_metrics(self, code: str, by: str):
        # placeholder
        return []
