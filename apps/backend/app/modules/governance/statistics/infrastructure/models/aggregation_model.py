from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from apps.backend.app.db.base import Base

class AggregationModel(Base):
    __tablename__ = 'statistics_aggregations'
    id = Column(Integer, primary_key=True)
    statistic_id = Column(Integer, nullable=False)
    method = Column(String(20), nullable=False)
    parameters = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)