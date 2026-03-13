from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class InstituicaoPesquisaModel(Base):
    __tablename__ = 'ciencia_instituicoes_pesquisa'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sigla: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    nif: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    natureza_juridica: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    pais: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    email_institucional: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status_credenciamento: Mapped[str] = mapped_column(String(30), nullable=False, default='em_analise', index=True)
    data_credenciamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade_credenciamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    comite_etica_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    nucleo_inovacao_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())