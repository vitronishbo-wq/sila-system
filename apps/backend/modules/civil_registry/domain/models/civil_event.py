from sqlalchemy import Column, String, DateTime, JSON
from app.core.database import Base
from datetime import datetime
import uuid

class CivilEventRecord(Base):
    __tablename__ = "civil_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
