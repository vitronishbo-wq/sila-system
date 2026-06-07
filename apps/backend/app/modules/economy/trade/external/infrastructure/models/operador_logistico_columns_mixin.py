from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class OperadorLogisticoColumnsMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cadastro_radar: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    tipo_operador: Mapped[str] = mapped_column(String(32), nullable=False)
    tipo_pessoa: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_fantasia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cnpj_cpf: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    endereco: Mapped[str] = mapped_column(Text, nullable=False)
    numero: Mapped[str] = mapped_column(String(32), nullable=False)
    complemento: Mapped[str | None] = mapped_column(String(128), nullable=True)
    bairro: Mapped[str] = mapped_column(String(128), nullable=False)
    municipio: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(128), nullable=False)
    cep: Mapped[str] = mapped_column(String(16), nullable=False)
    pais: Mapped[str] = mapped_column(String(2), nullable=False, default="AO")
    telefone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    site: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_licenca: Mapped[str | None] = mapped_column(String(64), nullable=True)
    orgao_anuente: Mapped[str | None] = mapped_column(String(255), nullable=True)
    data_habilitacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_validade: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_suspensao: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_cancelamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
