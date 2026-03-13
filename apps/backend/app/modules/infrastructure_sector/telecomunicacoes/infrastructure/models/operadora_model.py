from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class OperadoraModel(Base):
    __tablename__ = 'telecom_operadoras'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False, index=True)
    razao_social: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    nome_fantasia: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    servicos_autorizados: Mapped[list[str]] = mapped_column(ARRAY(String(40)), nullable=False, default=list)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    representante_legal: Mapped[str] = mapped_column(String(120), nullable=False)
    representante_documento: Mapped[str] = mapped_column(String(40), nullable=False)
    representante_cargo: Mapped[str] = mapped_column(String(80), nullable=False)
    outorga_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    data_autorizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True, default='requerida')
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())