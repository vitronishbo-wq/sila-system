from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class RiscoEvasaoModel(Base):
    __tablename__ = 'juventude_riscos_evasao'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_risco: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    jovem_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    matricula_ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    situacao_ocupacional: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    vulnerabilidades: Mapped[list[str] | None] = mapped_column(ARRAY(String(40)), nullable=True)
    pontuacao: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    nivel_risco: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    data_avaliacao: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    fatores: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    recomendacoes: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())