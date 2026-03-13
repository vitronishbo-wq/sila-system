from typing import Any

class AnalyticsService:

    def __init__(self, report_repo, exporter=None):
        self.report_repo = report_repo
        self.exporter = exporter

    def run_report(self, report_id: int, params: dict) -> Any:
        report = self.report_repo.get(report_id)
        if not report:
            return None
        return {'result': [], 'report': report}

    def export_report(self, report_id: int, fmt: str='csv') -> bytes:
        data = self.run_report(report_id, {})
        return b''

    def schedule_report(self, report_id: int, cron: str):
        return True