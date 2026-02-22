from typing import List, Optional
from ...domain.models.dashboard import Dashboard


class DashboardService:
    def __init__(self, dashboard_repo):
        self.dashboard_repo = dashboard_repo

    def create_dashboard(self, name: str, description: str, owner_id: int, layout) -> Dashboard:
        # minimal mapping — in real app map domain<->persistence
        dm = dict(name=name, description=description, owner_id=owner_id, layout=layout)
        dashboard = self.dashboard_repo.add(dm)
        return dashboard

    def get_dashboard(self, id: int) -> Optional[dict]:
        return self.dashboard_repo.get(id)

    def list_dashboards(self, owner_id: Optional[int] = None) -> List[dict]:
        return self.dashboard_repo.list(owner_id=owner_id)

    def update_layout(self, id: int, layout) -> dict:
        d = self.dashboard_repo.get(id)
        if not d:
            return None
        d.layout = layout
        self.dashboard_repo.session.flush()
        return d
