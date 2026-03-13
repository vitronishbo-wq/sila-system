from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class UnidadeManejoModel(Base):
    __tablename__ = 'florestas_unidades_manejo'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_um: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    area_total_ha: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    area_manejo_ha: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    area_preservacao_ha: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    tipo_manejo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    ciclo_corte: Mapped[str] = mapped_column(String(20), nullable=False)
    operador_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    imovel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    plano_manejo_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    licenca_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    data_criacao: Mapped[date] = mapped_column(Date, nullable=False)
    data_aprovacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    coordenadas_centroide: Mapped[str | None] = mapped_column(String(120), nullable=True)
    arquivo_shp: Mapped[str | None] = mapped_column(String(500), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())