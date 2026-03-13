from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class OcorrenciaModel(Base):
    __tablename__ = 'seguranca_ocorrencias'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_ocorrencia: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    unidade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    policial_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default='registrada', index=True)
    prioridade: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    data_ocorrencia: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    endereco: Mapped[str | None] = mapped_column(String(255), nullable=True)
    vitimas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    suspeitos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    preso_em_flagrante: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())