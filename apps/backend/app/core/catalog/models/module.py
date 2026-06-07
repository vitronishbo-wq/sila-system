"""
Modelo de Módulo - SILA System 2026
Um módulo é uma unidade de domínio de negócio que agrupa serviços relacionados.
"""

import sys
from datetime import datetime

from apps.backend.app.core.catalog.models.service import Service
from apps.backend.app.core.db import Base
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

sys.modules.setdefault("apps.backend.app.core.catalog.models.module", sys.modules[__name__])


class Module(Base):
    """
    Representa um módulo administrativo do SILA.
    Exemplos: Identidade Civil, Registos, Território, Pagamentos
    """

    __tablename__ = "modules"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📦")
    color: Mapped[str] = mapped_column(String(20), default="#C8102E")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_foundational: Mapped[bool] = mapped_column(Boolean, default=False)
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    services: Mapped[list[Service]] = relationship(Service, lazy="selectin")

    def __repr__(self) -> str:
        return f"<Module {self.slug}: {self.title}>"
