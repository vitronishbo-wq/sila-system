from sqlalchemy import Column, String, DateTime
from app.core.database import Base
from datetime import datetime
import uuid

class MarriageRegistrationRecord(Base):
    __tablename__ = "marriage_registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    spouse1_id = Column(String, nullable=False)
    spouse2_id = Column(String, nullable=False)
    marriage_date = Column(DateTime, nullable=False)
    regime = Column(String, nullable=False) # e.g., Communal, Separate
    place_of_marriage = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
