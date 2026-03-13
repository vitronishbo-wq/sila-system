from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class FamilyCompositionViewModel(Base):
    __tablename__ = 'family_composition_view'
    family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    head_citizen_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    head_name: Mapped[str] = mapped_column(String(200), nullable=False, default='')
    member_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dependents_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active_relationships: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    composition_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())