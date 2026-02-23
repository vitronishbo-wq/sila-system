"""
Modelo de Módulo - SILA System 2026
Um módulo é uma unidade de domínio de negócio que agrupa serviços relacionados.
"""
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.core.catalog.models.service import Service

class Module(Base):
    """
    Representa um módulo administrativo do SILA.
    Exemplos: Identidade Civil, Registos, Território, Pagamentos
    """
    __tablename__ = "modules"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="📦")  # Emoji ou ícone
    color: Mapped[str] = mapped_column(String(20), default="#C8102E")  # Cor tema (vermelho SILA)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_foundational: Mapped[bool] = mapped_column(Boolean, default=False)  # Módulo fundador?
    order: Mapped[int] = mapped_column(Integer, default=0)  # Ordem de exibição
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com serviços
    services: Mapped[List["Service"]] = relationship("Service", back_populates="module", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Module {self.slug}: {self.title}>"
