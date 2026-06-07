import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String

from apps.backend.app.core.db import Base


class CemeteryInspectionRecord(Base):
    __tablename__ = "cemetery_inspections"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cemetery_name = Column(String, nullable=False)
    inspection_date = Column(DateTime, default=datetime.utcnow)
    inspector_id = Column(String, nullable=False)
    results = Column(JSON, nullable=False)
    status = Column(String, default="completed")
