from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class DashboardModel(Base):
    __tablename__ = 'est_dashboards'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    configuracoes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    kpi_ids: Mapped[list[int]] = mapped_column(JSON, nullable=False, default=list)
    criado_por: Mapped[int | None] = mapped_column(nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())