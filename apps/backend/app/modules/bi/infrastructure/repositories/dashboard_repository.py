from typing import Optional
from ..models.dashboard_model import DashboardModel


class DashboardRepository:
    def __init__(self, session):
        self.session = session

    def add(self, dashboard: DashboardModel) -> DashboardModel:
        self.session.add(dashboard)
        self.session.flush()
        return dashboard

    def get(self, id: int) -> Optional[DashboardModel]:
        return self.session.query(DashboardModel).get(id)

    def list(self, owner_id: Optional[int] = None):
        q = self.session.query(DashboardModel)
        if owner_id is not None:
            q = q.filter(DashboardModel.owner_id == owner_id)
        return q.all()
