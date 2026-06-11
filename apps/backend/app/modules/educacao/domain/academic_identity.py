
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class AcademicStatus(str, Enum):
    ACTIVE = "ACTIVE"
    GRADUATED = "GRADUATED"
    TRANSFERRED = "TRANSFERRED"
    SUSPENDED = "SUSPENDED"
    DROPPED = "DROPPED"
    DECEASED = "DECEASED"


class IdentityStatus(str, Enum):
    VALID = "VALID"
    SUSPECT_DUPLICATE = "SUSPECT_DUPLICATE"
    MERGED = "MERGED"
    INACTIVE = "INACTIVE"


class GuardianRelationship(str, Enum):
    PAI = "pai"
    MAE = "mae"
    TUTOR_LEGAL = "tutor_legal"
    AVO = "avo"
    OUTRO = "outro"


@dataclass
class AcademicIdentity:
    id: UUID = field(default_factory=uuid4)
    national_student_number: str = ""
    full_name: str = ""
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    nationality: str = "ANGOLANA"
    guardian_id: Optional[UUID] = None
    territory_id: UUID  # Princípio 8
    created_by: UUID  # Princípio 8
    managed_by: UUID  # Princípio 8
    current_institution_id: Optional[UUID] = None
    current_grade: Optional[str] = None
    academic_status: AcademicStatus = AcademicStatus.ACTIVE
    identity_status: IdentityStatus = IdentityStatus.VALID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "national_student_number": self.national_student_number,
            "full_name": self.full_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "nationality": self.nationality,
            "guardian_id": self.guardian_id,
            "territory_id": self.territory_id,
            "created_by": self.created_by,
            "managed_by": self.managed_by,
            "current_institution_id": self.current_institution_id,
            "current_grade": self.current_grade,
            "academic_status": self.academic_status.value if self.academic_status else None,
            "identity_status": self.identity_status.value if self.identity_status else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class Guardian:
    id: UUID = field(default_factory=uuid4)
    full_name: str = ""
    relationship: GuardianRelationship = GuardianRelationship.OUTRO
    document_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    territory_id: UUID  # Princípio 8 e 9
    created_by: UUID  # Princípio 8
    managed_by: UUID  # Princípio 8
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class MergeCandidate:
    id: UUID = field(default_factory=uuid4)
    primary_identity_id: UUID = field(default_factory=uuid4)
    duplicate_identity_id: UUID = field(default_factory=uuid4)
    reason: str = ""
    confidence: str = "MEDIUM"
    status: str = "PENDING"
    resolved_by: Optional[str] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


@dataclass
class DuplicateResult:
    identity_id: UUID
    duplicate_of: UUID
    match_type: str
    confidence: str
    fields: list[str]
