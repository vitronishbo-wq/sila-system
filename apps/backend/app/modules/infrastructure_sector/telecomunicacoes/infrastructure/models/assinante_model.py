from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class AssinanteModel(Base):
    __tablename__ = "telecom_assinantes"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_assinante: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo_plano: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    servico_principal: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    data_adesao: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    nome: Mapped[str | None] = mapped_column(String(200), nullable=True)
    citizen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    telefone_contato: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email_contato: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contrato_numero: Mapped[str | None] = mapped_column(String(60), nullable=True)
    valor_mensal: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
