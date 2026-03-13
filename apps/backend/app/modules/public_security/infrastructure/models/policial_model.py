from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class PolicialModel(Base):
    __tablename__ = 'seguranca_policiais'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricula: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    unidade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False, index=True)
    rg: Mapped[str] = mapped_column(String(30), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    vinculo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    cargo: Mapped[str | None] = mapped_column(String(40), nullable=True)
    patente: Mapped[str | None] = mapped_column(String(40), nullable=True)
    data_ingresso: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='ativo', index=True)
    porte_arma: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    numero_porte: Mapped[str | None] = mapped_column(String(40), nullable=True)
    data_validade_porte: Mapped[date | None] = mapped_column(Date, nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(255), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())