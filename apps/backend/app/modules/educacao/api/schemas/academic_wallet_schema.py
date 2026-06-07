from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class WalletIdentity(BaseModel):
    id: str
    national_student_number: str
    full_name: str
    academic_status: Optional[str] = None
    identity_status: Optional[str] = None


class WalletEnrollment(BaseModel):
    id: Optional[str] = None
    institution_id: Optional[str] = None
    academic_year: Optional[str] = None
    grade: Optional[str] = None


class WalletEnrollmentHistory(BaseModel):
    id: str
    institution_id: str
    academic_year: str
    grade: Optional[str] = None
    status: str
    started_at: Optional[str] = None
    ended_at: Optional[str] = None


class WalletGuardian(BaseModel):
    id: str
    full_name: str
    relationship: str


class WalletRecord(BaseModel):
    completed_classes: list[Any] = []
    sanctions: list[Any] = []


class AcademicWalletResponse(BaseModel):
    identity: WalletIdentity
    active_enrollment: Optional[WalletEnrollment] = None
    enrollment_history: list[WalletEnrollmentHistory] = []
    record: WalletRecord
    guardians: list[WalletGuardian] = []
