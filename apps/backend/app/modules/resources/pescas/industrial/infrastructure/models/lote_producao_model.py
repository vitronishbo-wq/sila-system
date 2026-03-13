from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class LoteProducaoModel(Base):
    __tablename__ = 'pescas_industriais_lotes_producao'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_lote: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    unidade_processamento_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    produto_processado_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_producao: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    quantidade_kg: Mapped[Decimal] = mapped_column(Numeric(15, 3), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    destino_mercado: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    turno: Mapped[str | None] = mapped_column(String(20), nullable=True)
    temperatura_armazenamento_c: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())