from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from ...domain.enums.taxpayer_status import TaxpayerStatus


class TaxpayerModel(Base):
    __tablename__ = "taxpayers"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PG_UUID(as_uuid=True), nullable=False)
    citizen_id = Column(PG_UUID(as_uuid=True), nullable=False)
    nif = Column(String(64), nullable=False, index=True, unique=True)
    name = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default=TaxpayerStatus.DRAFT.value)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    # relationships can be added later (debts, certificates)
