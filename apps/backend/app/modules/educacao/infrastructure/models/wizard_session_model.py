from __future__ import annotations

import uuid

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class WizardSessionModel(Base):
    __tablename__ = "educacao_wizard_matricula"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    citizen_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(24), nullable=False, default="em_curso", index=True
    )
    passo_atual: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    dados_estudante: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    dados_encarregado: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    selecao_escola: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    documentos: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    resultado_elegibilidade: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    pagamento: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    matricula_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    expires_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
