from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MetricModel(Base):
    __tablename__ = "bi_metrics"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    dimension = Column(String(100), nullable=True)
    period = Column(String(50), nullable=False, index=True)
    extra = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_bi_metrics_code", MetricModel.code)
Index("ix_bi_metrics_period", MetricModel.period)
