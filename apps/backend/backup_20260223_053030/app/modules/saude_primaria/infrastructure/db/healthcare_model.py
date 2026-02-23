import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON, Integer, Date, Boolean, Float, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

# Importação absoluta da camada de domínio conforme padrões SILA
from app.modules.saude_primaria.domain.enums import (
    HealthcareServiceType, 
    AppointmentStatus, 
    MaternalRiskLevel, 
    ChronicSeverity, 
    NotificationChannel
)

class HealthcareRequestModel(Base):
    """
    Modelo central do workflow de Saúde Primária no SILA.
    Gerencia o estado da consulta e serve como âncora para registos clínicos especializados.
    """
    __tablename__ = "saude_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citizen_id = Column(UUID(as_uuid=True), ForeignKey("citizen_fuc.citizen_id"), nullable=False, index=True)
    
    service_type = Column(SQLEnum(HealthcareServiceType), nullable=False, index=True)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.PENDING, index=True)
    
    preferred_date = Column(DateTime, nullable=True)
    scheduled_date = Column(DateTime, nullable=True)
    health_unit_id = Column(String, nullable=True)
    
    clinical_notes = Column(Text, nullable=True)
    # 'metadata' é um nome reservado pela API Declarative; mapear para a coluna SQL 'metadata'
    # usando um nome de atributo diferente para evitar conflito.
    metadata_json = Column("metadata", JSON, nullable=True)

    # Auditoria SILA
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Relacionamentos 1:1 Especializados com Cascade Delete Total
    maternal_record = relationship("MaternalRecordModel", back_populates="request", uselist=False, cascade="all, delete-orphan")
    post_natal_record = relationship("PostNatalRecordModel", back_populates="request", uselist=False, cascade="all, delete-orphan")
    chronic_monitoring = relationship("ChronicMonitoringModel", back_populates="request", uselist=False, cascade="all, delete-orphan")
    nutrition_record = relationship("NutritionRecordModel", back_populates="request", uselist=False, cascade="all, delete-orphan")
    psychology_session = relationship("PsychologySessionModel", back_populates="request", uselist=False, cascade="all, delete-orphan")
    health_alert = relationship("HealthAlertModel", back_populates="request", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_saude_requests_citizen_status', 'citizen_id', 'status'),
    )

class MaternalRecordModel(Base):
    """
    Registo de Saúde Materna e Planeamento Familiar.
    Estabelece relação 1:1 com HealthcareRequestModel.
    """
    __tablename__ = "saude_maternal_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    gestational_weeks = Column(Integer, nullable=True)
    risk_level = Column(SQLEnum(MaternalRiskLevel), nullable=True)
    expected_delivery_date = Column(Date, nullable=True)
    parity = Column(Integer, nullable=True)
    prenatal_visits = Column(Integer, default=0)
    
    request = relationship("HealthcareRequestModel", back_populates="maternal_record")

class PostNatalRecordModel(Base):
    """Registo de acompanhamento Pós-Natal (Puerpério)."""
    __tablename__ = "saude_post_natal_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    days_post_partum = Column(Integer, nullable=False)
    healing_status = Column(String, nullable=True)
    
    request = relationship("HealthcareRequestModel", back_populates="post_natal_record")

class ChronicMonitoringModel(Base):
    """Monitorização de Doentes Crónicos."""
    __tablename__ = "saude_chronic_monitoring"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    condition_name = Column(String, nullable=False)
    severity = Column(SQLEnum(ChronicSeverity), nullable=False)
    medication_plan = Column(Text, nullable=True)
    monitoring_frequency = Column(String, nullable=True)
    last_measurements = Column(JSON, nullable=True)
    
    request = relationship("HealthcareRequestModel", back_populates="chronic_monitoring")

class NutritionRecordModel(Base):
    """Registo Nutricional Comunitário."""
    __tablename__ = "saude_nutrition_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    nutritional_status = Column(String, nullable=True)
    risk_category = Column(String, nullable=True)
    diet_plan = Column(Text, nullable=True)
    
    request = relationship("HealthcareRequestModel", back_populates="nutrition_record")

class PsychologySessionModel(Base):
    """Sessão de Apoio Psicológico Comunitário."""
    __tablename__ = "saude_psychology_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    session_type = Column(String, nullable=False)
    risk_assessment = Column(Text, nullable=True)
    referral_needed = Column(Boolean, default=False)
    suicide_risk_flag = Column(Boolean, default=False)
    
    request = relationship("HealthcareRequestModel", back_populates="psychology_session")

class HealthAlertModel(Base):
    """Configuração de Alertas de Saúde Personalizados."""
    __tablename__ = "saude_health_alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("saude_requests.id"), nullable=False, unique=True)
    
    alert_type = Column(String, nullable=False)
    threshold_value = Column(String, nullable=True)
    notification_channel = Column(SQLEnum(NotificationChannel), nullable=False)
    is_active = Column(Boolean, default=True)
    
    request = relationship("HealthcareRequestModel", back_populates="health_alert")