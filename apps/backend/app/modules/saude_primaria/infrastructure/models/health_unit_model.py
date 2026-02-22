"""SQLAlchemy Health Unit Models"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HealthUnitModel(Base):
    """Unidade de saúde"""
    __tablename__ = "health_units"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Localização
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    municipality: Mapped[str] = mapped_column(String(100), nullable=False)
    commune: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Capacidade
    beds: Mapped[int] = mapped_column(Integer, default=0)
    has_emergency: Mapped[bool] = mapped_column(Boolean, default=False)
    has_laboratory: Mapped[bool] = mapped_column(Boolean, default=False)
    has_pharmacy: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Serviços
    specialties: Mapped[List[str]] = mapped_column(ARRAY(String), default=[])
    
    # Horário (armazenado como JSON)
    opening_hours: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Metadados
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )


class HealthProfessionalModel(Base):
    """Profissional de saúde"""
    __tablename__ = "health_professionals"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    health_unit_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    license_number: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(200), nullable=False)
    
    metadata_: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
