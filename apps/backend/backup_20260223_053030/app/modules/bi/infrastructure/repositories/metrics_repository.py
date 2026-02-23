from typing import List, Optional
from ..models.metric_model import MetricModel


class MetricsRepository:
    """Repository responsible for reading/writing metrics.

    In production this should receive a SQLAlchemy session via DI.
    """

    def __init__(self, session):
        self.session = session

    def add(self, metric: MetricModel) -> MetricModel:
        self.session.add(metric)
        self.session.flush()
        return metric

    def list(self, limit: int = 100) -> List[MetricModel]:
        return self.session.query(MetricModel).order_by(MetricModel.created_at.desc()).limit(limit).all()

    def find_by_code(self, code: str) -> Optional[MetricModel]:
        return self.session.query(MetricModel).filter(MetricModel.code == code).first()
