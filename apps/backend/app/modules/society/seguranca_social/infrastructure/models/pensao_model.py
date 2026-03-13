from __future__ import annotations
import uuid
from decimal import Decimal
from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class PensaoModel(Base):
    __tablename__ = 'seguranca_social_pensoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_processo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    beneficiario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    data_inicio: Mapped[str] = mapped_column(Date, nullable=False)
    valor_mensal: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    periodicidade: Mapped[str] = mapped_column(String(24), nullable=False, default='mensal')
    status: Mapped[str] = mapped_column(String(32), nullable=False, default='aguardando_aprovacao', index=True)
    data_fim: Mapped[str | None] = mapped_column(Date, nullable=True)
    conta_bancaria: Mapped[str | None] = mapped_column(String(64), nullable=True)
    iban: Mapped[str | None] = mapped_column(String(64), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())