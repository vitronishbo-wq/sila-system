from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class InstitutionCapacityModel(Base):
    """
    PASSO 4 — Institution Capacity Model
    
    Gerencia a capacidade de matrículas por série/turno em cada instituição.
    Rastreia vagas totais, utilizadas e reservadas.
    
    ⚠️  REGRA CRÍTICA — NUNCA fazer aritmética sem lock transacional:
    
    ❌ ERRADO (Race condition):
        available = capacity_total - capacity_used
        if available > 0:
            # Entre aqui e UPDATE, outro processo pode ter alocado
            UPDATE enrollment SET capacity_used = capacity_used + 1
    
    ✅ CORRETO (Com lock pessimista):
        SELECT * FROM institution_capacity 
        WHERE id = ? 
        FOR UPDATE  # ← LOCK TRANSACIONAL OBRIGATÓRIO
        
        available = row.capacity_total - row.capacity_used
        if available > 0:
            UPDATE capacity_used = capacity_used + 1
    
    Implementação: Use session.execute() com select().with_for_update()
    ou execute() com "FOR UPDATE" explícito em SQLAlchemy.
    """
    __tablename__ = "educacao_institution_capacities"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        nullable=False, 
        index=True
    )
    grade: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        index=True
    )
    shift: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        index=True
    )
    capacity_total: Mapped[int] = mapped_column(
        Integer, 
        nullable=False
    )
    capacity_used: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0
    )
    capacity_reserved: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0
    )
    
    # Auditoria Temporal
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "institution_id", 
            "grade", 
            "shift", 
            name="uq_institution_capacity"
        ),
        CheckConstraint(
            "capacity_total > 0",
            name="chk_capacity_total_positive"
        ),
        CheckConstraint(
            "capacity_used >= 0",
            name="chk_capacity_used_non_negative"
        ),
        CheckConstraint(
            "capacity_reserved >= 0",
            name="chk_capacity_reserved_non_negative"
        ),
        CheckConstraint(
            "capacity_used + capacity_reserved <= capacity_total",
            name="chk_capacity_total_not_exceeded"
        ),
    )
