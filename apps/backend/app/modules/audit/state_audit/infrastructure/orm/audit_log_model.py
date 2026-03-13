from sqlalchemy import Column, DateTime, JSON, String
from app.domain.db import Base

class AuditLogModel(Base):
    __tablename__ = 'audit_logs'
    id = Column(String, primary_key=True)
    event_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    actor_id = Column(String, nullable=False)
    metadata = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)