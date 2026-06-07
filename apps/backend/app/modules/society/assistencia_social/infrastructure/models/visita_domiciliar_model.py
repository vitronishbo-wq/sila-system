from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class VisitaDomiciliarModel(Base):
    __tablename__ = "assistencia_social_visitas_domiciliares"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    beneficiario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    assistente_social_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    data_visita: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    condicoes_moradia: Mapped[str] = mapped_column(String(180), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    recomendacoes: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    resultado: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
