from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.core.database import Base
import uuid

class BirthRecord(Base):
    """Modelo de Domínio Rico para Assento de Nascimento."""
    __tablename__ = "birth_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nub = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    place_of_birth = Column(String, nullable=False)
    
    # Filiação
    father_name = Column(String)
    father_id = Column(String, nullable=True) # Link opcional para FUC
    mother_name = Column(String, nullable=False)
    mother_id = Column(String, nullable=True) # Link opcional para FUC
    
    # Metadados de auditoria
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<BirthRecord(nub={self.nub}, name={self.full_name})>"
