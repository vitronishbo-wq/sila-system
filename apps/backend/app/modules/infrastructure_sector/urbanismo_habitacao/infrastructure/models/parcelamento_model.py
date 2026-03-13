from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class ParcelamentoModel(Base):
    __tablename__ = 'urbanismo_habitacao_parcelamentos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_parcelamento: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    plano_diretor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    zoneamento_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    area_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    quantidade_unidades_prevista: Mapped[int] = mapped_column(Integer, nullable=False)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    area_publica_prevista: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    area_sistema_viario_prevista: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    quantidade_unidades_resultante: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)