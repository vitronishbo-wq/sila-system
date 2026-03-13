from sqlalchemy import Column, Float, String
from app.domain.db import Base

class BidModel(Base):
    __tablename__ = 'procurement_bids'
    id = Column(String, primary_key=True)
    tender_id = Column(String, nullable=False)
    supplier_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)