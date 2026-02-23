from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DashboardModel(Base):
    __tablename__ = "bi_dashboards"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, nullable=True, index=True)
    layout = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_bi_dashboards_owner", DashboardModel.owner_id)
