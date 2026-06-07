from sqlalchemy import JSON, Column, DateTime, String

from apps.backend.app.core.db import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    event_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    actor_id = Column(String, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)
