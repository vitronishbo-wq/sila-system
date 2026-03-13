from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class ReclamacaoTelecomModel(Base):
    __tablename__ = 'telecom_reclamacoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    protocolo: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    assinante_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    prioridade: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_abertura: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_fechamento: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resposta: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())