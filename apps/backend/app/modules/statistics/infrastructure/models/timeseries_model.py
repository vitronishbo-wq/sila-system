from sqlalchemy import Column, Integer, Float, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base


class TimeSeriesModel(Base):
    __tablename__ = "statistics_timeseries"

    id = Column(Integer, primary_key=True)
    statistic_id = Column(Integer, nullable=False, index=True)
    value = Column(Float, nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=True)
    dimensions = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_timeseries_statistic_id", TimeSeriesModel.statistic_id)
Index("ix_timeseries_period_start", TimeSeriesModel.period_start)
