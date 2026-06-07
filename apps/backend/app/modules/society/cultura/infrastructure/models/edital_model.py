from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class EditalModel(Base):
    __tablename__ = "cultura_editais"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    orgao_responsavel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    valor_disponivel: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    data_publicacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, index=True
    )
    data_inicio_inscricoes: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    data_fim_inscricoes: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    vagas: Mapped[int] = mapped_column(Integer, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    fase: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    criterios: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    documentos_necessarios: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    inscricoes: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    projetos_selecionados: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
