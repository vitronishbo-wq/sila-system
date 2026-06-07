from __future__ import annotations

from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from apps.backend.app.core.db import Base


class Document(Base):
    __tablename__ = "wallet_documents"
    __table_args__ = {"extend_existing": True}
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    citizen_id = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    issued_at = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)


__all__ = ["Document"]
