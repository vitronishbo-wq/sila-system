"""SQLAlchemy Medical Record Model"""
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Date, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MedicalRecordModel(Base):
    """Registro médico"""
    __tablename__ = "medical_records"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    record_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    
    # Identidades
    citizen_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    appointment_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    doctor_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    # Anamnese
    chief_complaint: Mapped[str] = mapped_column(String(500), nullable=False)
    history_of_present_illness: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    past_medical_history: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    family_history: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    social_history: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    allergies: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Exame físico (armazenado como JSON)
    vital_signs: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    physical_exam: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Diagnóstico
    diagnosis: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    diagnosis_codes: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Conduta
    treatment_plan: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    follow_up_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Referências
    prescription_ids: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    exam_request_ids: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Datas
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
