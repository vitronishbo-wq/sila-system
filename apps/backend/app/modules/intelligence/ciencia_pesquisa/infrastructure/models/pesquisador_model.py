from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class PesquisadorModel(Base):
    __tablename__ = 'ciencia_pesquisadores'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_completo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    documento_identificacao: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    email_institucional: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    instituicao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    unidade_pesquisa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    area_conhecimento: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    nivel_formacao: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    tipo_vinculo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status_vinculo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    data_inicio_vinculo: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim_vinculo: Mapped[date | None] = mapped_column(Date, nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    orcid: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
    lattes_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    researcher_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    scopus_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())