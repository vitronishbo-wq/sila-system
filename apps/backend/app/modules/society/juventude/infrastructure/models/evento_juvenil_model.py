from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class EventoJuvenilModel(Base):
    __tablename__ = 'juventude_eventos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_evento: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    tipo_evento: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    area_interesse: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    data_evento: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    local: Mapped[str] = mapped_column(String(200), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    vagas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    participantes: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())