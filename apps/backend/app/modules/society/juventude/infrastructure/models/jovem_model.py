from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class JovemModel(Base):
    __tablename__ = 'juventude_jovens'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_registro: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    faixa_etaria: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=False)
    naturalidade: Mapped[str] = mapped_column(String(100), nullable=False)
    nacionalidade: Mapped[str] = mapped_column(String(50), nullable=False, default='Angolana')
    escolaridade: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    situacao_ocupacional: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    vulnerabilidades: Mapped[list[str] | None] = mapped_column(ARRAY(String(40)), nullable=True)
    programas: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    auxilios: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    formacoes: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), nullable=True)
    experiencias: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    interesses: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)), nullable=True)
    habilidades: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)), nullable=True)
    encaminhamentos: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    acompanhamento_psicossocial: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())