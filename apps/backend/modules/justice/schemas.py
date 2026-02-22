"""
Justice Schemas Module

Schemas para entidades do módulo de Justiça no SILA system.
Inclui certificados judiciais, mediações, processos, tribunais e documentos legais.
"""

import re
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

# --- Judicial Certificate Schemas --- #


class CertificateType(str, Enum):
    GOOD_CONDUCT = "good_conduct"


class CertificateStatus(str, Enum):
    PENDING = "pending"
    ISSUED = "issued"
    COMPLETED = "completed"


class JudicialCertificateCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: CertificateType
    citizenId: int
    details: str

    @property
    def citizen_id(self):
        return getattr(self, "citizenId", None)

    @field_validator("details")
    def _details_min_length(cls, v: str):
        if not v or len(str(v).strip()) < 10:
            raise ValueError("pelo menos 10 caracteres")
        return v


class JudicialCertificate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    type: CertificateType
    status: Optional[str] = None
    issueDate: Optional[datetime] = None
    citizenId: Optional[int] = None
    documentPath: Optional[str] = None

    @property
    def issue_date(self):
        return getattr(self, "issueDate", None)

    @property
    def citizen_id(self):
        return getattr(self, "citizenId", None)

    @property
    def document_path(self):
        return getattr(self, "documentPath", None)


class JudicialCertificateUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: Optional[CertificateType] = None
    details: Optional[str] = None


# --- Mediation Request Schemas --- #


class MediationType(str, Enum):
    NEIGHBOR = "neighbor"


class MediationRequestCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: MediationType
    citizenId: int
    description: str

    @field_validator("description")
    def _description_min_length(cls, v: str):
        if not v or len(str(v).strip()) < 20:
            raise ValueError("pelo menos 20 caracteres")
        return v

    @property
    def citizen_id(self):
        return getattr(self, "citizenId", None)


# --- Judicial Process Schemas --- #


class ProcessStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"


class JudicialProcessCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    processNumber: str
    court: str
    citizenId: int
    status: ProcessStatus

    @field_validator("processNumber")
    def _validate_process_number(cls, v: str):
        pattern = re.compile(r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$")
        if not pattern.match(str(v)):
            raise ValueError("process number inválido")
        return v

    @property
    def process_number(self):
        return getattr(self, "processNumber", None)

    @property
    def citizen_id(self):
        return getattr(self, "citizenId", None)


class JudicialProcess(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    processNumber: str
    court: str
    status: ProcessStatus
    citizenId: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    @property
    def created_at(self):
        return getattr(self, "createdAt", None)

    @property
    def updated_at(self):
        return getattr(self, "updatedAt", None)


# --- Court Schemas --- #


class CourtCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: Optional[str] = None
    code: Optional[str] = None
    court_type: Optional[str] = None
    jurisdiction: Optional[str] = None


class CourtUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: Optional[str] = None
    code: Optional[str] = None


# --- Legal Document Schemas --- #


class LegalDocumentCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
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


class LegalDocumentUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    title: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None
    is_confidential: Optional[bool] = None
    is_public: Optional[bool] = None
