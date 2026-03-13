from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class PlanoManejoFlorestalModel(Base):
    __tablename__ = 'florestas_planos_manejo'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_pmfs: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    unidade_manejo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    responsavel_tecnico_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    responsavel_tecnico_registro: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_submissao: Mapped[date] = mapped_column(Date, nullable=False)
    data_aprovacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    analista_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    volume_anual_estimado_m3: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    ciclo_corte_anos: Mapped[int] = mapped_column(Integer, nullable=False)
    area_anual_ha: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    parecer_tecnico: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())