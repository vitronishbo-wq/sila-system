from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class HabiteSeModel(Base):
    __tablename__ = "urbanismo_habitacao_habite_se"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_habite_se: Mapped[str] = mapped_column(
        String(40), unique=True, nullable=False, index=True
    )
    numero_processo: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    alvara_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    requerente_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    endereco_imovel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    area_vistoriada: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    data_requerimento: Mapped[date] = mapped_column(Date, nullable=False)
    data_vistoria: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_emissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    tecnico_vistoriador_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
