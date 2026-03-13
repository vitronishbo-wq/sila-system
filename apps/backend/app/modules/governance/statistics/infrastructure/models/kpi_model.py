from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class KPIModel(Base):
    __tablename__ = 'est_kpis'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    metrica_id: Mapped[int] = mapped_column(ForeignKey('est_metricas.id', ondelete='CASCADE'), nullable=False, index=True)
    valor_alvo: Mapped[float | None] = mapped_column(Float, nullable=True)
    valor_atual: Mapped[float | None] = mapped_column(Float, nullable=True)
    valor_anterior: Mapped[float | None] = mapped_column(Float, nullable=True)
    unidade: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default='ativo', index=True)
    peso: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    limite_inferior: Mapped[float | None] = mapped_column(Float, nullable=True)
    limite_superior: Mapped[float | None] = mapped_column(Float, nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())