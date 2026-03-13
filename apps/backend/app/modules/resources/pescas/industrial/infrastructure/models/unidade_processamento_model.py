from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class UnidadeProcessamentoModel(Base):
    __tablename__ = 'pescas_industriais_unidades'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False, index=True)
    razao_social: Mapped[str] = mapped_column(String(200), nullable=False)
    nome_fantasia: Mapped[str | None] = mapped_column(String(200), nullable=True)
    inscricao_estadual: Mapped[str | None] = mapped_column(String(20), nullable=True)
    inscricao_municipal: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tipo_processamento: Mapped[list[str]] = mapped_column(ARRAY(String(32)), nullable=False, default=list)
    classificacao: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    capacidade_kg_dia: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    area_total_m2: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    area_producao_m2: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    area_armazenagem_m2: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    capacidade_frigorifica_m3: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    temperatura_media: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    numero_funcionarios: Mapped[int] = mapped_column(Integer, nullable=False)
    responsavel_tecnico_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    responsavel_tecnico_registro: Mapped[str | None] = mapped_column(String(50), nullable=True)
    endereco: Mapped[str] = mapped_column(String(200), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(50), nullable=False)
    coordenadas_lat: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    coordenadas_long: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    armador_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    data_inauguracao: Mapped[date] = mapped_column(Date, nullable=False)
    licenca_operacao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    alvara_sanitario_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    certificacoes: Mapped[list[str] | None] = mapped_column(ARRAY(String(36)), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())