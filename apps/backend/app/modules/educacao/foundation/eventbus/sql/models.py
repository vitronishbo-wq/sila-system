from __future__ import annotations

import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OutboxEvent(Base):
    __tablename__ = "foundation_outbox"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(255), nullable=False)
    payload = Column(JSON, nullable=False)
    tenant_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    dispatched = Column(Boolean, default=False, nullable=False)
    dispatched_at = Column(DateTime, nullable=True)
    locked_by = Column(String(64), nullable=True)
    locked_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0, nullable=False)
