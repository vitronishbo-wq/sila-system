"""SQLAlchemy Exam Request Model"""
from datetime import datetime, date
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ExamRequestModel(Base):
    """Pedido de exame"""
    __tablename__ = "exam_requests"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    request_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    
    # Identidades
    citizen_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    doctor_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    # Dados do exame
    exam_type: Mapped[str] = mapped_column(String(100), nullable=False)
    exam_description: Mapped[str] = mapped_column(String(1000), nullable=False)
    clinical_indication: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    # Status e prioridade
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="SOLICITADO")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIA")
    
    # Datas
    requested_date: Mapped[date] = mapped_column(Date, nullable=False)
    scheduled_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    collection_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    result_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Resultado
    result_file: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    result_notes: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    
    # Workflow
    workflow_instance_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
