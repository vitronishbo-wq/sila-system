from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Integer, JSON, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class ObraModel(Base):
    __tablename__ = 'obras_publicas_obras'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_obra: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    natureza: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    orgao_responsavel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    orgao_responsavel_tipo: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    valor_orcado: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    data_inicio_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim_prevista: Mapped[date] = mapped_column(Date, nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    bairro: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    prazo_original_dias: Mapped[int] = mapped_column(Integer, nullable=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    gestor_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    fiscal_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    empreiteira_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    contrato_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    projeto_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    valor_contratado: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    valor_executado: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    valor_pago: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    data_inicio_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_entrega: Mapped[date | None] = mapped_column(Date, nullable=True)
    coordenadas_lat: Mapped[Decimal | None] = mapped_column(Numeric(12, 8), nullable=True)
    coordenadas_long: Mapped[Decimal | None] = mapped_column(Numeric(12, 8), nullable=True)
    imovel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    percentual_executado: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal('0'))
    prazo_adicionado_dias: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dias_corridos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dias_atraso: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    medicoes: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    aditivos: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    fiscalizacoes: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    termos_recebimento: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    trilha_auditoria: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)