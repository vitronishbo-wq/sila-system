from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class MarketplaceVacancyModel(Base):
    __tablename__ = "educacao_marketplace_vacancies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    ano_letivo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    classe: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    turno: Mapped[str] = mapped_column(String(32), nullable=False)
    vagas_totais: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vagas_ocupadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vagas_disponiveis: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("institution_id", "ano_letivo", "classe", "turno", name="uq_marketplace_vacancy"),
    )
