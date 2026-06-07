from datetime import datetime
from typing import Optional

from apps.backend.app.core.db import Base
from sqlalchemy import Column, DateTime, Enum, String, Text


class ProviderContract(Base):
    __tablename__ = "provider_contracts"

    provider = Column(String(100), nullable=False, index=True)
    contract_number = Column(String(100), nullable=False)
    entity = Column(String(200), nullable=False)
    signed_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        Enum("draft", "testing", "active", "suspended", "terminated", name="contract_status"),
        nullable=False,
        default="draft",
    )
    terms = Column(Text, nullable=True)
    metadata_json = Column("metadata", Text, nullable=True)
