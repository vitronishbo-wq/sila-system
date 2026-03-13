from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from apps.backend.app.modules.justice.bounded_contexts.shared import Base
import uuid

class CemeteryInspectionRecord(Base):
    """Modelo de Domínio para Inspeções de Cemitérios."""
    __tablename__ = 'cemetery_inspections'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cemetery_name = Column(String, nullable=False)
    inspector_id = Column(String, nullable=False)
    inspection_date = Column(DateTime, default=datetime.utcnow)
    results = Column(JSON, nullable=False)
    observations = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CemeteryInspectionRecord(cemetery={self.cemetery_name}, date={self.inspection_date})>'