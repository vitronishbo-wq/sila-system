from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class CadastroUnicoModel(Base):
    __tablename__ = 'assistencia_social_cadastros_unicos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    citizen_id_responsavel: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    renda_per_capita: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    composicao_familiar: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    condicoes_moradia: Mapped[str] = mapped_column(String(120), nullable=False)
    acesso_agua: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    acesso_energia: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())