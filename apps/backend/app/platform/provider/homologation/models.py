from apps.backend.app.core.db import Base
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text


class ProviderHomologationEvidence(Base):
    __tablename__ = "provider_homologation_evidence"

    provider = Column(String(100), nullable=False, index=True)
    endpoint = Column(String(500), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    latency_ms = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    auth_ok = Column(Boolean, default=False)
    payload_hash = Column(String(128), nullable=True)
    operator = Column(String(200), nullable=True)
    result = Column(String(50), nullable=False)
    details = Column(Text, nullable=True)
