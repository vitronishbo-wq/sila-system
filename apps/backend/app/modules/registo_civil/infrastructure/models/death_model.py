from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from datetime import datetime
import uuid

class DeathRegistrationRecord(Base):
    __tablename__ = "death_registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = Column(String, nullable=False)
    death_date = Column(DateTime, nullable=False)
    place_of_death = Column(String)
    cause_of_death = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
