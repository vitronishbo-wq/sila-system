"""Service Registry Models - ORM definitions"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from config.database import Base


class ServiceRegistry(Base):
    __tablename__ = "service_hub_serviceregistrys"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

