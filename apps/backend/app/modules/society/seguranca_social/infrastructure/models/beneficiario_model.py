from __future__ import annotations
import uuid
from sqlalchemy import Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class BeneficiarioModel(Base):
    __tablename__ = 'seguranca_social_beneficiarios'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_beneficiario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    citizen_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_inscricao: Mapped[str] = mapped_column(Date, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    regime: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(24), nullable=False, default='pendente', index=True)
    data_ativacao: Mapped[str | None] = mapped_column(Date, nullable=True)
    data_suspensao: Mapped[str | None] = mapped_column(Date, nullable=True)
    data_cancelamento: Mapped[str | None] = mapped_column(Date, nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())