from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.core.database import Base
import uuid

class DeathRecord(Base):
    """Modelo de Domínio Rico para Assento de Óbito."""
    __tablename__ = "death_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = Column(String, nullable=False, index=True)
    
    death_date = Column(DateTime, nullable=False)
    place_of_death = Column(String, nullable=False)
    cause_of_death = Column(String, nullable=False)
    
    # Auditoria
    witnesses = Column(String) # Nomes ou IDs separados por vírgula para simplificar
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DeathRecord(citizen={self.citizen_id}, date={self.death_date})>"
