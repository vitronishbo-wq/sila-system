from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class DesapropriacaoModel(Base):
    __tablename__ = 'gestao_fundiaria_desapropriacoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_processo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    imovel_inscricao: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    ente_publico: Mapped[str] = mapped_column(String(255), nullable=False)
    finalidade: Mapped[str] = mapped_column(Text, nullable=False)
    valor_indenizacao: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    data_decreto: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_pagamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)