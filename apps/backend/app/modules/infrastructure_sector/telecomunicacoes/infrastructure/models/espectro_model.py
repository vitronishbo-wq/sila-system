from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class EspectroModel(Base):
    __tablename__ = "telecom_espectro"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_espectro: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    frequencia_inicial_mhz: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    frequencia_final_mhz: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    largura_banda_mhz: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    servico_principal: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    outorga_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
