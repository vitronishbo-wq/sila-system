from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ReportModel(Base):
    __tablename__ = "bi_reports"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    parameters = Column(JSONB, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
