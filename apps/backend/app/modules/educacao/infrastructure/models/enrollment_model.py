from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class EnrollmentModel(Base):
    """
    PASSO 3 — Enrollment Model
    
    Armazena histórico real de matrículas estudantis.
    Vincula estudantes a instituições em períodos acadêmicos específicos.
    Rastreia transferências e mudanças de série com timestamps precisos.
    
    Constraint Crítico:
    - Um estudante (student_id) pode ter apenas UM enrollment ativo por academic_year
    - Histórico completo via created_at/updated_at para auditoria
    """
    __tablename__ = "educacao_enrollments"
    
    # Campos Mínimos Obrigatórios (PASSO 3)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        nullable=False, 
        index=True
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        nullable=False, 
        index=True
    )
    academic_year: Mapped[str] = mapped_column(
        String(16), 
        nullable=False, 
        index=True
    )
    grade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    transfer_origin_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
        nullable=True, 
        index=True
    )
    transfer_destination_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
        nullable=True, 
        index=True
    )
    academic_identity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    
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
            "student_id", 
            "academic_year", 
            name="uq_enrollment_student_year"
        ),
    )
