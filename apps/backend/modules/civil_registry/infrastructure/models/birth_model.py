from sqlalchemy import Column, String, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime
import uuid

class BirthRegistrationRecord(Base):
    __tablename__ = "birth_registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nub = Column(String, unique=True, nullable=False) # Numero Unico de Bilhete
    full_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    place_of_birth = Column(String, nullable=False)
    father_name = Column(String)
    mother_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
