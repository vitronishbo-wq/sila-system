from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class EmbarcacaoModel(Base):
    __tablename__ = 'pescas_embarcacoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    numero_inscricao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    modalidades: Mapped[list[str]] = mapped_column(ARRAY(String(32)), nullable=False, default=list)
    comprimento: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    arqueacao_bruta: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    potencia_motor: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    capacidade_porao: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tripulacao_minima: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    porto_registro: Mapped[str] = mapped_column(String(60), nullable=False)
    ano_construcao: Mapped[int] = mapped_column(Integer, nullable=False)
    material_casco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    armador_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    licenca_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    sistema_rastreio: Mapped[str | None] = mapped_column(String(60), nullable=True)
    data_inspecao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade_doc: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())