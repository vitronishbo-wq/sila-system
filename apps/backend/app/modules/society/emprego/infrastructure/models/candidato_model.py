from __future__ import annotations
import uuid
from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class CandidatoModel(Base):
    __tablename__ = 'emprego_candidatos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_processo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    citizen_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_registro: Mapped[str] = mapped_column(Date, nullable=False)
    escolaridade: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    situacao: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    areas_interesse: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    experiencias: Mapped[list[dict] | None] = mapped_column(JSONB, nullable=True)
    habilidades: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default='ativo', index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())