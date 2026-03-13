from sqlalchemy import Column, Float, String
from app.domain.db import Base

class ContractModel(Base):
    __tablename__ = 'procurement_contracts'
    id = Column(String, primary_key=True)
    tender_id = Column(String, nullable=False)
    supplier_id = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    status = Column(String, nullable=False)