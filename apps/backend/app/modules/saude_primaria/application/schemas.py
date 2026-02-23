from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, Any, Dict
from uuid import UUID
from app.modules.saude_primaria.domain.enums import HealthcareServiceType, AppointmentStatus, MaternalRiskLevel, ChronicSeverity, NotificationChannel

class MaternalRecordSchema(BaseModel):
    """Contrato para dados de Saúde Materna e Planeamento Familiar."""
    model_config = ConfigDict(from_attributes=True)

    gestational_weeks: Optional[int] = Field(None, ge=0, le=50)
    risk_level: Optional[MaternalRiskLevel] = None
    expected_delivery_date: Optional[date] = None
    parity: Optional[int] = Field(None, ge=0)
    prenatal_visits: int = Field(default=0, ge=0)

class PostNatalRecordSchema(BaseModel):
    """Contrato para dados de Puerpério."""
    model_config = ConfigDict(from_attributes=True)

    days_post_partum: int = Field(..., ge=0)
    healing_status: Optional[str] = None

class ChronicMonitoringSchema(BaseModel):
    """Contrato para acompanhamento de doentes crónicos."""
    model_config = ConfigDict(from_attributes=True)
    
    condition_name: str
    severity: ChronicSeverity
    medication_plan: Optional[str] = None
    monitoring_frequency: Optional[str] = None
    last_measurements: Optional[Dict[str, Any]] = None

class NutritionRecordSchema(BaseModel):
    """Contrato para registos de nutrição comunitária."""
    model_config = ConfigDict(from_attributes=True)
    
    weight: float
    height: float
    bmi: float
    nutritional_status: Optional[str] = None
    risk_category: Optional[str] = None
    diet_plan: Optional[str] = None

class PsychologySessionSchema(BaseModel):
    """Contrato para sessões de psicologia comunitária."""
    model_config = ConfigDict(from_attributes=True)
    
    session_type: str
    risk_assessment: Optional[str] = None
    referral_needed: bool = False
    suicide_risk_flag: bool = False

class HealthAlertSchema(BaseModel):
    """Contrato para configuração de alertas personalizados."""
    model_config = ConfigDict(from_attributes=True)
    
    alert_type: str
    threshold_value: Optional[str] = None
    notification_channel: NotificationChannel
    is_active: bool = True

# Request Schemas
class HealthcareRequestCreate(BaseModel):
    service_type: HealthcareServiceType
    preferred_date: Optional[datetime] = None
    health_unit_id: Optional[str] = None
    symptoms: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    # Dados especializados opcionais
    maternal_record: Optional[MaternalRecordSchema] = None
    post_natal_record: Optional[PostNatalRecordSchema] = None
    chronic_monitoring: Optional[ChronicMonitoringSchema] = None
    nutrition_record: Optional[NutritionRecordSchema] = None
    psychology_session: Optional[PsychologySessionSchema] = None
    health_alert: Optional[HealthAlertSchema] = None

class HealthcareScheduleUpdate(BaseModel):
    scheduled_date: datetime
    health_unit_id: str
    notes: Optional[str] = None

class HealthcareStatusUpdate(BaseModel):
    status: AppointmentStatus
    clinical_notes: Optional[str] = None

class HealthcareCancelRequest(BaseModel):
    reason: str

# Response Schemas
class HealthcareRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    citizen_id: UUID
    service_type: HealthcareServiceType
    status: AppointmentStatus
    preferred_date: Optional[datetime]
    scheduled_date: Optional[datetime]
    health_unit_id: Optional[str]
    clinical_notes: Optional[str]
    metadata: Optional[Dict[str, Any]]
    
    maternal_record: Optional[MaternalRecordSchema] = None
    post_natal_record: Optional[PostNatalRecordSchema] = None
    chronic_monitoring: Optional[ChronicMonitoringSchema] = None
    nutrition_record: Optional[NutritionRecordSchema] = None
    psychology_session: Optional[PsychologySessionSchema] = None
    health_alert: Optional[HealthAlertSchema] = None
    
    created_at: datetime
    updated_at: datetime