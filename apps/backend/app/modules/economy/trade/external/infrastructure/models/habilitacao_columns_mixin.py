from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

class HabilitacaoColumnsMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo_operador: Mapped[str] = mapped_column(String(32), nullable=False)
    tipo_pessoa: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=False)
    cnpj_cpf: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    numero_processo: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    data_solicitacao: Mapped[date] = mapped_column(Date, nullable=False)
    data_analise: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    numero_radar: Mapped[str | None] = mapped_column(String(64), nullable=True)
    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)