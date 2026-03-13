from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base

class StatisticModel(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    unit = Column(String(50), nullable=True)
    source_module = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
Index('ix_statistics_code', StatisticModel.code)