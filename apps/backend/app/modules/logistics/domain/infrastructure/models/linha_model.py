from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Integer, JSON, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class LinhaModel(Base):
    __tablename__ = 'transportes_logistica_linhas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    modal: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    tipo_viagem: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    origem: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    destino: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    itinerario: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    extensao_km: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    tempo_estimado_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    dias_operacao: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    horario_inicio: Mapped[str] = mapped_column(String(5), nullable=False)
    horario_fim: Mapped[str] = mapped_column(String(5), nullable=False)
    tarifa_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    frequencia_media_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    concessionaria_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    outorga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    data_inicio_operacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_autorizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade_autorizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    frota_necessaria: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frota_operante: Mapped[int | None] = mapped_column(Integer, nullable=True)
    demanda_media_diaria: Mapped[int | None] = mapped_column(Integer, nullable=True)
    oferta_media_diaria: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ocupacao_media: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    regularidade: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    pontualidade: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    acessivel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ar_condicionado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    wifi: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sanitario: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    veiculos_ativos: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    trilha_auditoria: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)