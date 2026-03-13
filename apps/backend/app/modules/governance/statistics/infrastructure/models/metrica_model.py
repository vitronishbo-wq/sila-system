from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class MetricaModel(Base):
    __tablename__ = 'est_metricas'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    unidade: Mapped[str] = mapped_column(String(50), nullable=False)
    fonte_dados: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    periodicidade: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    formula: Mapped[str | None] = mapped_column(String(500), nullable=True)
    parametros: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    valor_atual: Mapped[float | None] = mapped_column(Float, nullable=True)
    valor_anterior: Mapped[float | None] = mapped_column(Float, nullable=True)
    variacao_percentual: Mapped[float | None] = mapped_column(Float, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    ultima_atualizacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)