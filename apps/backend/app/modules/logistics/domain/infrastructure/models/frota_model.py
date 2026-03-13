from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class FrotaModel(Base):
    __tablename__ = 'transportes_logistica_frotas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_frota: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    veiculos: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    manutencoes: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    fiscalizacoes: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    tarifas: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    trilha_auditoria: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)