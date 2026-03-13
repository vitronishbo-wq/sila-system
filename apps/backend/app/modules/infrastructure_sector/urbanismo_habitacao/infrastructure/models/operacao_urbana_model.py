from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class OperacaoUrbanaModel(Base):
    __tablename__ = 'urbanismo_habitacao_operacoes_urbanas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_operacao: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    plano_diretor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    orgao_responsavel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    municipio: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    area_intervencao: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    investimento_previsto: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    investimento_executado: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    data_inicio_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_inicio_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_fim_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    percentual_execucao: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal('0'))
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)