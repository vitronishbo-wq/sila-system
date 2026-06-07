from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class ArtistaModel(Base):
    __tablename__ = "cultura_artistas"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registro_cultural: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    nome_artistico: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tipo: Mapped[list[str]] = mapped_column(ARRAY(String(30)), nullable=False, default=list)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    naturalidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    nacionalidade: Mapped[str] = mapped_column(String(50), nullable=False, default="Angolana")
    biografia: Mapped[str | None] = mapped_column(Text, nullable=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    provincia: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
