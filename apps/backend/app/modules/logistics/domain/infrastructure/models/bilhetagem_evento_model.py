from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, JSON, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class BilhetagemEventoModel(Base):
    __tablename__ = 'transportes_logistica_bilhetagem_eventos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_bilhete: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    viagem_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo_tarifa: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    valor_pago: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    forma_pagamento: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    data_evento: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    status_reconciliacao: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    lancamento_financeiro_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    referencia_externa: Mapped[str | None] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict] = mapped_column('metadata', JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)