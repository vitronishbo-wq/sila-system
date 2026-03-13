from sqlalchemy import Boolean, Column, DateTime, String
from apps.backend.app.domain.db import Base

class AuditCaseModel(Base):
    __tablename__ = 'audit_cases'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    opened_at = Column(DateTime, nullable=False)
    resolved = Column(Boolean, default=False)