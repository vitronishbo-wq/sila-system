from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class EditalModel(Base):
    __tablename__ = 'obras_publicas_editais'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_edital: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    objeto: Mapped[str] = mapped_column(Text, nullable=False)
    licitacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    data_publicacao: Mapped[date] = mapped_column(Date, nullable=False)
    data_abertura: Mapped[date] = mapped_column(Date, nullable=False)
    data_encerramento: Mapped[date] = mapped_column(Date, nullable=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    versao: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)