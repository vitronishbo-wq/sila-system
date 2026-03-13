from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class RebanhoModel(Base):
    __tablename__ = 'pecuaria_rebanhos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_rebanho: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    propriedade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo_animal: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    quantidade_animais: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())