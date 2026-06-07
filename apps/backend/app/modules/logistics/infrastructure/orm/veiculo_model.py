from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class VeiculoModel(Base):
    __tablename__ = "transportes_logistica_veiculos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    placa: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    marca: Mapped[str] = mapped_column(String(80), nullable=False)
    modelo: Mapped[str] = mapped_column(String(80), nullable=False)
    ano_fabricacao: Mapped[int] = mapped_column(Integer, nullable=False)
    ano_modelo: Mapped[int] = mapped_column(Integer, nullable=False)
    proprietario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    proprietario_tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    data_aquisicao: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    capacidade_passageiros: Mapped[int | None] = mapped_column(Integer, nullable=True)
    capacidade_carga_kg: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    capacidade_carga_m3: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    comprimento: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    largura: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    altura: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    peso_bruto_total: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    numero_eixos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    combustivel: Mapped[str | None] = mapped_column(String(32), nullable=True)
    consumo_medio: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    operadora_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    licenciamento: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    seguro: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rastreador_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    data_ultima_manutencao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_proxima_manutencao: Mapped[date | None] = mapped_column(Date, nullable=True)
    quilometragem: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
