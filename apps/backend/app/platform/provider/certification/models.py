from datetime import datetime
from typing import Optional

from apps.backend.app.core.db import Base
from sqlalchemy import Column, DateTime, Enum, String, Text


class ProviderCertification(Base):
    __tablename__ = "provider_certifications"

    provider = Column(String(100), nullable=False, index=True)
    environment = Column(String(50), nullable=False, default="homologation")
    certification_status = Column(
        Enum("mock", "testing", "mock_live", "homologation", "certified", "production", "suspended", name="cert_status"),
        nullable=False,
        default="mock",
    )
    approved_by = Column(String(200), nullable=True)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
