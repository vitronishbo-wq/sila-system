from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class InspecaoModel(Base):
    __tablename__ = 'pescas_industriais_inspecoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_inspecao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    unidade_processamento_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_agendada: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    selo_inspecao: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    fiscal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    lote_producao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    data_realizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    pontuacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    inconformidades: Mapped[list[str] | None] = mapped_column(ARRAY(String(255)), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())