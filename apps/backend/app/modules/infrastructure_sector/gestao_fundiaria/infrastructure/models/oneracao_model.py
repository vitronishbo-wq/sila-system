from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class OneracaoModel(Base):
    __tablename__ = 'gestao_fundiaria_oneracoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_oneracao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    imovel_inscricao: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    credor_nome: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    documento_credor: Mapped[str | None] = mapped_column(String(64), nullable=True)
    moeda: Mapped[str] = mapped_column(String(3), nullable=False, default='AOA')
    data_vencimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)