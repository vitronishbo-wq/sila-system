from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class EspacoCulturalModel(Base):
    __tablename__ = "cultura_espacos_culturais"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_espaco: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    area_m2: Mapped[float] = mapped_column(Float, nullable=False)
    administracao: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    responsavel_cpf: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    orgao_gestor: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ano_inauguracao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    acessibilidade: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    visitas_anuais: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
