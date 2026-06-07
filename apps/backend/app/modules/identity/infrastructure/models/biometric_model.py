from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Numeric, String, Text

from apps.backend.app.core.db import Base


class IdentityBiometric(Base):
    __tablename__ = "identity_biometrics"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    citizen_id = Column(String(64), nullable=False, index=True)
    biometric_type = Column(String(32), nullable=False, index=True)
    biometric_data = Column(Text, nullable=False)
    quality_score = Column(Numeric(5, 2), nullable=False)
    quality_threshold = Column(Numeric(5, 2), nullable=True)
    device_id = Column(String(128), nullable=True)
    location = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="ENROLLED", index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


__all__ = ["IdentityBiometric"]
