"""Citizen model for the citizenship module."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Citizen(Base):
    """
    Modelo representando um cidadão no módulo de Cidadania.
    Usado como base para serviços, pedidos de nacionalidade, atualização de BI, etc.
    """
    __tablename__ = "citizenship_citizens"
    __table_args__ = {"extend_existing": True}

    # ID como UUID – consistente com outros modelos
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    # Dados pessoais
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(
        String(200), unique=True, index=True, nullable=True
    )
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Controle
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps automáticos (com func.now() do SQL no banco)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Citizen id={self.id} name='{self.name}' email='{self.email}'>"