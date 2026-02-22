from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from app.core.database import Base
import enum
import uuid

class MarriageRegime(str, enum.Enum):
    COMUNHAO_ADQUIRIDOS = "comunhao_adquiridos"
    COMUNHAO_GERAL = "comunhao_geral"
    SEPARACAO_BENS = "separacao_bens"

class MarriageRecord(Base):
    """Modelo de Domínio Rico para Assento de Casamento."""
    __tablename__ = "marriage_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    spouse1_id = Column(String, nullable=False, index=True)
    spouse2_id = Column(String, nullable=False, index=True)
    
    marriage_date = Column(DateTime, nullable=False)
    place_of_marriage = Column(String, nullable=False)
    regime = Column(Enum(MarriageRegime), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MarriageRecord(spouses={self.spouse1_id}/{self.spouse2_id})>"
