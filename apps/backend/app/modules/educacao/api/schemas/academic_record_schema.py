from __future__ import annotations

from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, Field


class EnrollmentRecordHistory(BaseModel):
    id: str
    type: str
    institution_id: Optional[str] = None
    institution_name: Optional[str] = None
    academic_year: Optional[str] = None
    grade: Optional[str] = None
    status: str
    timestamp: str


class AcademicRecordResponse(BaseModel):
    identity_id: str
    current_class: Optional[str] = None
    completed_classes: list[Any] = []
    sanctions: list[Any] = []
    history: list[EnrollmentRecordHistory] = []
