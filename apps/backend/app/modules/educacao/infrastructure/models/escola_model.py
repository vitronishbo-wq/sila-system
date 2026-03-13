from __future__ import annotations
import uuid
from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class EscolaModel(Base):
    __tablename__ = 'educacao_escolas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_med: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(32), nullable=False)
    ciclos: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    provincia: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    comuna: Mapped[str] = mapped_column(String(128), nullable=False)
    bairro: Mapped[str] = mapped_column(String(128), nullable=False)
    endereco: Mapped[str] = mapped_column(Text, nullable=False)
    contacto: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())