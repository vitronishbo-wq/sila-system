from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from config.database import Base


class HealthRecord(Base):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "health_healthrecords"
    id = Column(Integer, primary_key=True)
    patient_id = Column(UUIDType(binary=False), ForeignKey("citizenship_citizens.id"), nullable=False)
    description = Column(String(1024), nullable=True)
    diagnosis = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Citizen
    citizen = relationship("Citizen", foreign_keys=[patient_id], back_populates="health_records")

