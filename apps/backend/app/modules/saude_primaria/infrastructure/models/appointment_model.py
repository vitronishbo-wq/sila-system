"""SQLAlchemy Appointment Model"""
from datetime import datetime, date, time
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Date, Time, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AppointmentModel(Base):
    """Consulta médica"""
    __tablename__ = "appointments"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    appointment_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    
    # Identidades
    citizen_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    created_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    doctor_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    # Dados da consulta
    appointment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)
    appointment_time: Mapped[time] = mapped_column(Time, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="AGENDADA")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIA")
    
    # Motivo
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    symptoms: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Workflow
    workflow_instance_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    workflow_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    tags: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Datas
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    __table_args__ = (
        # Índices para performance
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
