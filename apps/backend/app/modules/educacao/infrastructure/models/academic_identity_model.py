from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class AcademicIdentityModel(Base):
    """
    NÚCLEO DO SISTEMA SILA — Academic Identity Model
    
    Armazena a identidade acadêmica de estudantes com rastreamento completo
    e conformidade com regulamentações educacionais.
    
    REGRA CRÍTICA: national_student_number é UNIQUE e imutável.
    """
    __tablename__ = "educacao_academic_identities"
    
    # Campos Mínimos Obrigatórios (PASSO 2)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    national_student_number: Mapped[str] = mapped_column(
        String(64), 
        unique=True,
        nullable=False, 
        index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(64), nullable=True)
    guardian_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
        nullable=True, 
        index=True
    )
    current_institution_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
        nullable=True, 
        index=True
    )
    current_grade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    academic_status: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    identity_status: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    
    # Auditoria Temporal
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "national_student_number", 
            name="uq_academic_identity_national_student_number"
        ),
    )
