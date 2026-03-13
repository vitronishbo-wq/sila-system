from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class EspecieModel(Base):
    __tablename__ = 'pescas_especies'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_comum: Mapped[str] = mapped_column(String(120), nullable=False)
    nome_cientifico: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo_fao: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    ameacada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())