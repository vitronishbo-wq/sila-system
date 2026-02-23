"""SQLAlchemy Prescription Model"""
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PrescriptionModel(Base):
    """Prescrição médica"""
    __tablename__ = "prescriptions"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    prescription_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    
    # Identidades
    citizen_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    doctor_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    appointment_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    # Dados da prescrição (armazenados como JSON)
    items: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=[])
    clinical_notes: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Validade
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="ATIVA")
    
    # Workflow
    workflow_instance_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Datas
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    dispensed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
