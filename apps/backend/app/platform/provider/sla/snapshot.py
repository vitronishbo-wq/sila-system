from datetime import datetime
from typing import Optional

from apps.backend.app.core.db import Base
from sqlalchemy import Column, DateTime, Float, String


class ProviderSLASnapshot(Base):
    __tablename__ = "provider_sla_snapshots"

    provider = Column(String(100), nullable=False, index=True)
    availability = Column(Float, nullable=False, default=0.0)
    latency_p95 = Column(Float, nullable=False, default=0.0)
    latency_p99 = Column(Float, nullable=False, default=0.0)
    error_rate = Column(Float, nullable=False, default=0.0)
    mttr = Column(Float, nullable=False, default=0.0)
    mtbf = Column(Float, nullable=False, default=0.0)
    measurement_mode = Column(String(50), nullable=False, default="simulated")
    snapshot_timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
