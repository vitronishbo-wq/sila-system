"""SQLAlchemy Vaccine Models"""
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VaccineModel(Base):
    """Vacina"""
    __tablename__ = "vaccines"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Doses
    doses_required: Mapped[int] = mapped_column(Integer, default=1)
    dose_interval_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Idade (em meses)
    min_age_months: Mapped[int] = mapped_column(Integer, default=0)
    max_age_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Contra-indicações
    contraindications: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )


class VaccineDoseModel(Base):
    """Dose de vacina aplicada"""
    __tablename__ = "vaccine_doses"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Identidades
    citizen_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    vaccine_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    applied_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    # Dados da dose
    dose_number: Mapped[int] = mapped_column(Integer, nullable=False)
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False)
    application_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_dose_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="APLICADA")
    
    # Reações
    adverse_reactions: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
