from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class CapturaModel(Base):
    __tablename__ = 'pescas_capturas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    embarcacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    licenca_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    zona_pesca_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    especie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    quantidade_kg: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    quantidade_unidades: Mapped[int | None] = mapped_column(Integer, nullable=True)
    arte_pesca_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    profundidade: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    coordenadas_inicio: Mapped[str | None] = mapped_column(String(120), nullable=True)
    coordenadas_fim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    condicoes_mar: Mapped[str | None] = mapped_column(String(120), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())