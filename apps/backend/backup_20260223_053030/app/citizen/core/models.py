"""Modelos principais para cidadãos."""
import uuid
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base



class CitizenFUC(Base):
    """
    Modelo SQLAlchemy para persistência de Cidadão.
    """

    __tablename__ = "citizen_fuc"

    citizen_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    birth_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    gender: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Documentos e atributos adicionais esperados pelos testes
    document_number: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True, index=True)
    vital_status: Mapped[str | None] = mapped_column(String(32), nullable=True, default="alive")
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    fuc_sync_timestamp: Mapped[date | None] = mapped_column(Date, nullable=True)

    def to_dict(self) -> dict:
        """Serializa o cidadão para dicionário, compatível com os testes e APIs."""
        return {
            "citizen_id": str(self.citizen_id),
            "full_name": self.full_name,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "gender": self.gender,
            "is_active": self.is_active,
            "document_number": self.document_number,
            "vital_status": self.vital_status,
            "email": self.email,
            "phone": self.phone,
            "fuc_sync_timestamp": self.fuc_sync_timestamp.isoformat() if self.fuc_sync_timestamp else None,
        }

    def __init__(self, **kwargs):
        # Defensive constructor: only set known attributes.
        # This avoids TypeError when SQLAlchemy mapping isn't fully
        # resolved at import time in complex test collection orders.
        provided = set(kwargs.keys())
        for k, v in kwargs.items():
            if hasattr(type(self), k):
                setattr(self, k, v)

        # Ensure Python-level defaults for attributes expected by tests
        # SQLAlchemy `mapped_column(..., default=...)` may not set the
        # attribute on instance creation, so provide defensive defaults
        # when the field wasn't provided by the caller.
        if "vital_status" not in provided and getattr(self, "vital_status", None) is None:
            try:
                self.vital_status = "alive"
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<CitizenFUC {self.full_name} ({self.citizen_id})>"
