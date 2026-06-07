from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class AtletaModel(Base):
    __tablename__ = "desporto_atletas"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_registro: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    naturalidade: Mapped[str] = mapped_column(String(100), nullable=False)
    nacionalidade: Mapped[str] = mapped_column(String(50), nullable=False, default="Angolana")
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    modalidades: Mapped[list[str]] = mapped_column(ARRAY(String(32)), nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True, default="ativo")
    posicoes: Mapped[list[str] | None] = mapped_column(ARRAY(String(32)), nullable=True)
    pe_preferencial: Mapped[str | None] = mapped_column(String(20), nullable=True)
    altura_cm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    peso_kg: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    clube_atual_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    numero_camisola: Mapped[int | None] = mapped_column(Integer, nullable=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    ultimo_exame_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
