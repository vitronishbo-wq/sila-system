from sqlalchemy import Column, Float, String
from app.domain.db import Base

class TenderModel(Base):
    __tablename__ = 'procurement_tenders'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    budget_program_id = Column(String, nullable=False)
    estimated_value = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, nullable=False)