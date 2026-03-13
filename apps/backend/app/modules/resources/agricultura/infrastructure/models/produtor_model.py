from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class ProdutorModel(Base):
    __tablename__ = 'agricultura_produtores'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cadastro_produtor: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    documento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    documento_tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    endereco: Mapped[str | None] = mapped_column(Text, nullable=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    empresa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    familiar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())