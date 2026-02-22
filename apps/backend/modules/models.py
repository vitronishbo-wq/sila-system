"""
Core models module for the SILA system.

This module centralizes base models for all modules:
- Journeys
- Justice
- Location
- Services

It provides Pydantic base schemas, shared fields, and
placeholders for future SQLAlchemy ORM models.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

# -------------------------------
# Base Schemas
# -------------------------------


class BaseSchema(BaseModel):
    """Base schema with created_at and updated_at fields."""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Service Hub Status
# 

class ServiceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# Journeys Models
# -------------------------------


class JourneyStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"


class JourneyBase(BaseSchema):
    citizen_id: int
    title: str
    description: Optional[str] = None
    status: JourneyStatus = JourneyStatus.ACTIVE


class JourneyCreate(JourneyBase):
    start_date: Optional[datetime] = None


class JourneyUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[JourneyStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class JourneyStepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class JourneyStepBase(BaseSchema):
    journey_id: int
    title: str
    description: Optional[str] = None
    status: JourneyStepStatus = JourneyStepStatus.PENDING
    order: int
    estimated_duration: Optional[int] = None


class JourneyStepCreate(JourneyStepBase):
    pass


class JourneyStepUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[JourneyStepStatus] = None
    order: Optional[int] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None


# -------------------------------
# Justice Models
# -------------------------------


class CertificateType(str, Enum):
    GOOD_CONDUCT = "good_conduct"


class CertificateStatus(str, Enum):
    PENDING = "pending"
    ISSUED = "issued"
    COMPLETED = "completed"


class JudicialCertificateBase(BaseSchema):
    type: CertificateType
    citizen_id: int
    details: Optional[str] = None

    @field_validator("details")
    def check_details_length(cls, v: Optional[str]):
        if v and len(v.strip()) < 10:
            raise ValueError("Details must be at least 10 characters")
        return v


class JudicialCertificateCreate(JudicialCertificateBase):
    pass


class JudicialCertificateUpdate(BaseSchema):
    type: Optional[CertificateType] = None
    details: Optional[str] = None


class MediationType(str, Enum):
    NEIGHBOR = "neighbor"


class MediationRequestBase(BaseSchema):
    type: MediationType
    citizen_id: int
    description: str

    @field_validator("description")
    def check_description_length(cls, v: str):
        if len(v.strip()) < 20:
            raise ValueError("Description must be at least 20 characters")
        return v


class MediationRequestCreate(MediationRequestBase):
    pass


class ProcessStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"


class JudicialProcessBase(BaseSchema):
    process_number: str
    court: str
    citizen_id: int
    status: ProcessStatus

    @field_validator("process_number")
    def validate_process_number(cls, v: str):
        import re

        pattern = re.compile(r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$")
        if not pattern.match(v):
            raise ValueError("Invalid process number format")
        return v


class JudicialProcessCreate(JudicialProcessBase):
    pass


class CourtBase(BaseSchema):
    name: Optional[str] = None
    code: Optional[str] = None
    court_type: Optional[str] = None
    jurisdiction: Optional[str] = None


class CourtCreate(CourtBase):
    pass


class CourtUpdate(CourtBase):
    pass


class LegalDocumentBase(BaseSchema):
    case_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    file_name: Optional[str] = None
    issuing_authority: Optional[str] = None
    recipient: Optional[str] = None
    legal_basis: Optional[str] = None
    validity_period_days: Optional[int] = None
    effective_date: Optional[datetime] = None
    service_date: Optional[datetime] = None
    is_confidential: Optional[bool] = False
    is_public: Optional[bool] = True
    requires_signature: Optional[bool] = False


class LegalDocumentCreate(LegalDocumentBase):
    pass


class LegalDocumentUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None
    is_confidential: Optional[bool] = None
    is_public: Optional[bool] = None


# -------------------------------
# Location Models
# -------------------------------


class CountryBase(BaseSchema):
    name: str
    code: str


class ProvinceBase(BaseSchema):
    name: str
    country_id: int


class MunicipalityBase(BaseSchema):
    name: str
    province_id: int


class RegionBase(BaseSchema):
    name: str
    type: str  # "municipio" | "provincia" | "pais"
    parent_id: Optional[int] = None


class CommuneBase(BaseSchema):
    name: str
    city_id: int


class CityBase(BaseSchema):
    name: str
    region_id: int


class FullAddressBase(BaseSchema):
    street: Optional[str] = None
    number: Optional[str] = None
    zip_code: Optional[str] = None
    commune_id: int


# -------------------------------
# Services Models
# -------------------------------


class ServiceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ServiceItemBase(BaseSchema):
    name: str
    status: ServiceStatus
    description: Optional[str] = None


class ServicesListBase(BaseSchema):
    items: List[ServiceItemBase] = []
    total: int = 0


# -------------------------------
# Exports
# -------------------------------

__all__ = [
    # Base
    "BaseSchema",
    # Journeys
    "JourneyBase",
    "JourneyCreate",
    "JourneyUpdate",
    "JourneyStepBase",
    "JourneyStepCreate",
    "JourneyStepUpdate",
    "JourneyStatus",
    "JourneyStepStatus",
    # Justice
    "JudicialCertificateBase",
    "JudicialCertificateCreate",
    "JudicialCertificateUpdate",
    "MediationRequestBase",
    "MediationRequestCreate",
    "JudicialProcessBase",
    "JudicialProcessCreate",
    "ProcessStatus",
    "CourtBase",
    "CourtCreate",
    "CourtUpdate",
    "LegalDocumentBase",
    "LegalDocumentCreate",
    "LegalDocumentUpdate",
    "CertificateType",
    "CertificateStatus",
    "MediationType",
    # Location
    "CountryBase",
    "ProvinceBase",
    "MunicipalityBase",
    "RegionBase",
    "CommuneBase",
    "CityBase",
    "FullAddressBase",
    # Services
    "ServiceItemBase",
    "ServicesListBase",
    "ServiceStatus",
]
