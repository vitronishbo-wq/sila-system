from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class ImovelModel(Base):
    __tablename__ = 'gestao_fundiaria_imoveis'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inscricao_imobiliaria: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    natureza: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    regime: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    situacao: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    area_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    area_privativa: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_construida: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_terreno: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    cep: Mapped[str | None] = mapped_column(String(20), nullable=True)
    coordenadas_lat: Mapped[Decimal | None] = mapped_column(Numeric(12, 8), nullable=True)
    coordenadas_long: Mapped[Decimal | None] = mapped_column(Numeric(12, 8), nullable=True)
    matricula_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    proprietario_atual_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)