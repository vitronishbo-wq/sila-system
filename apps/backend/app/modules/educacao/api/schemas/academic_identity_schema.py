from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class AcademicIdentityCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    birth_date: date
    gender: Optional[str] = Field(None, pattern=r"^(M|F|Outro)$")
    nationality: str = "ANGOLANA"
    guardian_id: Optional[uuid.UUID] = None


class AcademicIdentityUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, pattern=r"^(M|F|Outro)$")
    nationality: Optional[str] = None
    guardian_id: Optional[uuid.UUID] = None
    current_institution_id: Optional[uuid.UUID] = None
    current_grade: Optional[str] = None
    academic_status: Optional[str] = None


class AcademicIdentityResponse(BaseModel):
    id: uuid.UUID
    national_student_number: str
    full_name: str
    birth_date: date
    gender: Optional[str] = None
    nationality: str = "ANGOLANA"
    guardian_id: Optional[uuid.UUID] = None
    current_institution_id: Optional[uuid.UUID] = None
    current_grade: Optional[str] = None
    academic_status: Optional[str] = None
    identity_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GuardianCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    relationship: str = Field(..., pattern=r"^(pai|mae|tutor_legal|avo|outro)$")
    document_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    municipio: Optional[str] = None


class GuardianResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    relationship: str
    document_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    municipio: Optional[str] = None
    created_at: Optional[datetime] = None


class GuardianLinkRequest(BaseModel):
    guardian_id: uuid.UUID
    student_id: uuid.UUID
    relationship: str = Field(..., pattern=r"^(pai|mae|tutor_legal|avo|outro)$")


class DuplicateResponse(BaseModel):
    identity_id: uuid.UUID
    duplicate_of: uuid.UUID
    match_type: str
    confidence: str
    fields: list[str]


class MergeProposalCreate(BaseModel):
    primary_identity_id: uuid.UUID
    duplicate_identity_id: uuid.UUID
    reason: str
    confidence: str = "MEDIUM"


class MergeCandidateResponse(BaseModel):
    id: uuid.UUID
    primary_identity_id: uuid.UUID
    duplicate_identity_id: uuid.UUID
    reason: str
    confidence: str
    status: str
    resolved_by: Optional[str] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class MergeResolveRequest(BaseModel):
    action: str = Field(..., pattern=r"^(approve|reject)$")
    resolved_by: str


class IdentityMetricsResponse(BaseModel):
    total_identities: int = 0
    active_count: int = 0
    graduated_count: int = 0
    duplicates_found: int = 0
    pending_merges: int = 0
