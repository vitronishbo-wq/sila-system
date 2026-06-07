from __future__ import annotations

import unicodedata
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ============================================================================
# ENUMS
# ============================================================================


class SLAPriority(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BULK = "bulk"


class SLATier(StrEnum):
    PLATINUM = "platinum"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


class CitizenType(StrEnum):
    NORMAL = "normal"
    PRIORITARIO = "prioritario"
    EMPRESA = "empresa"
    GOVERNO = "governo"
    DIPLOMATA = "diplomata"


class ChannelType(StrEnum):
    ONLINE = "online"
    PRESENCIAL = "presencial"
    TELEFONE = "telefone"
    APP = "app"
    USSD = "ussd"


class Province(StrEnum):
    CABINDA = "cabinda"
    ZAIRE = "zaire"
    UIGE = "uige"
    BENGO = "bengo"
    ICOLO_E_BENGO = "icolo_e_bengo"
    LUANDA = "luanda"
    KUANZA_NORTE = "kuanza_norte"
    KUANZA_SUL = "kuanza_sul"
    MALANJE = "malanje"
    LUNDA_NORTE = "lunda_norte"
    LUNDA_SUL = "lunda_sul"
    BENGUELA = "benguela"
    HUAMBO = "huambo"
    BIE = "bie"
    MOXICO = "moxico"
    MOXICO_LESTE = "moxico_leste"
    HUILA = "huila"
    NAMIBE = "namibe"
    CUNENE = "cunene"
    CUBANGO = "cubango"
    CUANDO = "cuando"


class LoadLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SLAStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


# ============================================================================
# SQLAlchemy MODELS
# ============================================================================


class SLABaseDB(Base):
    __tablename__ = "sla_base"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    service_id = Column(String(100), unique=True, nullable=False, index=True)
    service_name = Column(String(200), nullable=False)
    service_description = Column(String(500))
    module = Column(String(50), nullable=False, index=True)
    base_hours = Column(Float, nullable=False)
    priority = Column(String(20), nullable=False)
    tier = Column(String(20), nullable=False)
    legal_basis = Column(String(200))
    version = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    metadata_json = Column("metadata", JSON, default=dict)


class SLAPolicyDB(Base):
    __tablename__ = "sla_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    scope = Column(String(20), nullable=False)
    scope_id = Column(String(100), nullable=False, index=True)
    service_id = Column(String(100), nullable=True, index=True)
    multiplier = Column(Float, default=1.0)
    max_hours = Column(Float, nullable=True)
    min_hours = Column(Float, nullable=True)
    enabled = Column(Boolean, default=True)
    reason = Column(String(500))
    effective_from = Column(DateTime, nullable=False)
    effective_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))


class SLAOverrideDB(Base):
    __tablename__ = "sla_overrides"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    conditions = Column(JSON, nullable=False)
    multiplier = Column(Float, default=1.0)
    priority = Column(Integer, default=0)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SLAVersionDB(Base):
    __tablename__ = "sla_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version = Column(String(10), nullable=False)
    service_id = Column(String(100), nullable=False, index=True)
    base_hours = Column(Float, nullable=False)
    changes = Column(JSON, default=list)
    approved_by = Column(String(100))
    approved_at = Column(DateTime, nullable=True)
    status = Column(String(20), default=SLAStatus.DRAFT.value)
    created_at = Column(DateTime, default=datetime.utcnow)


class SLAViolationDB(Base):
    __tablename__ = "sla_violations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    request_id = Column(String(100), unique=True, index=True)
    service_id = Column(String(100), nullable=False, index=True)
    target_hours = Column(Float, nullable=False)
    actual_hours = Column(Float, nullable=False)
    delta_hours = Column(Float, nullable=False)
    context = Column(JSON, default=dict)
    province = Column(String(50), index=True)
    citizen_type = Column(String(20))
    channel = Column(String(20))
    escalated = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=0)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# Pydantic MODELS
# ============================================================================


class SLAContext(BaseModel):
    province: Province = Province.LUANDA
    citizen_type: CitizenType = CitizenType.NORMAL
    channel: ChannelType = ChannelType.ONLINE
    load_level: LoadLevel = LoadLevel.MEDIUM
    is_holiday: bool = False
    business_hours: bool = True
    custom_factors: dict[str, float] = Field(default_factory=dict)

    @validator("province", pre=True)
    def normalize_province(cls, v):
        if isinstance(v, Province):
            return v
        if isinstance(v, str):
            normalized = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode("ascii")
            normalized = normalized.strip().lower().replace(" ", "_").replace("-", "_")
            legacy_map = {
                "cuanza_norte": "kuanza_norte",
                "cuanza_sul": "kuanza_sul",
                "kuando_kubango": "cubango",
                "cuando_cubango": "cubango",
            }
            return legacy_map.get(normalized, normalized)
        return v

    @validator("province")
    def validate_province(cls, v):
        if v not in Province.__members__.values():
            raise ValueError(f"Província inválida: {v}")
        return v


class SLARequest(BaseModel):
    service_id: str
    context: SLAContext = Field(default_factory=SLAContext)


class SLAPredictRequest(BaseModel):
    service_id: str
    elapsed_hours: float
    context: SLAContext = Field(default_factory=SLAContext)


class SLAResponse(BaseModel):
    service_id: str
    service_name: str
    base_hours: float
    calculated_hours: float
    applied_policies: list[dict[str, Any]]
    applied_overrides: list[dict[str, Any]]
    breakdown: dict[str, float]
    warnings: list[str] = []
    expires_at: datetime


class SLAPolicyCreate(BaseModel):
    scope: str
    scope_id: str
    service_id: str | None = None
    multiplier: float = 1.0
    max_hours: float | None = None
    min_hours: float | None = None
    reason: str
    effective_from: datetime
    effective_to: datetime | None = None


class SLAOverrideCreate(BaseModel):
    name: str
    description: str
    conditions: dict[str, Any]
    multiplier: float = 1.0
    priority: int = 0


class SLAViolationResponse(BaseModel):
    id: str
    request_id: str
    service_id: str
    service_name: str
    target_hours: float
    actual_hours: float
    delta_hours: float
    breach_percentage: float
    severity: str
    province: str | None
    citizen_type: str | None
    escalated: bool
    created_at: datetime


# ============================================================================
# GLOBAL CONSTANTS
# ============================================================================

PROVINCE_FACTORS = {
    Province.CABINDA: 1.3,
    Province.ZAIRE: 1.2,
    Province.UIGE: 1.1,
    Province.BENGO: 0.9,
    Province.ICOLO_E_BENGO: 0.9,
    Province.LUANDA: 0.8,
    Province.KUANZA_NORTE: 1.1,
    Province.KUANZA_SUL: 1.1,
    Province.MALANJE: 1.1,
    Province.LUNDA_NORTE: 1.2,
    Province.LUNDA_SUL: 1.2,
    Province.BENGUELA: 1.0,
    Province.HUAMBO: 1.0,
    Province.BIE: 1.2,
    Province.MOXICO: 1.4,
    Province.MOXICO_LESTE: 1.4,
    Province.HUILA: 1.0,
    Province.NAMIBE: 1.2,
    Province.CUNENE: 1.4,
    Province.CUBANGO: 1.5,
    Province.CUANDO: 1.5,
}

CITIZEN_TYPE_FACTORS = {
    CitizenType.NORMAL: 1.0,
    CitizenType.PRIORITARIO: 0.5,
    CitizenType.EMPRESA: 0.8,
    CitizenType.GOVERNO: 0.3,
    CitizenType.DIPLOMATA: 0.4,
}

CHANNEL_FACTORS = {
    ChannelType.ONLINE: 0.8,
    ChannelType.APP: 0.7,
    ChannelType.PRESENCIAL: 1.0,
    ChannelType.TELEFONE: 1.2,
    ChannelType.USSD: 1.5,
}

LOAD_FACTORS = {
    LoadLevel.LOW: 0.9,
    LoadLevel.MEDIUM: 1.0,
    LoadLevel.HIGH: 1.3,
    LoadLevel.CRITICAL: 1.6,
}
