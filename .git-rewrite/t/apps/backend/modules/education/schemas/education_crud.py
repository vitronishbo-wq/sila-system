"""Pydantic schemas for education module with CRUD support."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


# Matricula Escolar schemas
class MatriculaBase(BaseModel):
    """Base schema for student enrollment."""

    student_id: str = Field(..., description="Student unique identifier")
    school_id: int = Field(..., description="School ID")
    grade: str = Field(..., description="Grade level")
    class_name: str = Field(..., description="Class name")
    enrollment_date: date = Field(..., description="Enrollment date")
    status: str = Field(default="ACTIVE", description="Enrollment status")
    academic_year: int = Field(..., description="Academic year")

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["ACTIVE", "INACTIVE", "TRANSFERRED", "GRADUATED", "DROPPED"]
        if v.upper() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v.upper()


class MatriculaCreate(MatriculaBase):
    """Schema for creating enrollment."""


class MatriculaUpdate(BaseModel):
    """Schema for updating enrollment."""

    grade: Optional[str] = None
    class_name: Optional[str] = None
    status: Optional[str] = None
    academic_year: Optional[int] = None

    @validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = [
                "ACTIVE",
                "INACTIVE",
                "TRANSFERRED",
                "GRADUATED",
                "DROPPED",
            ]
            if v.upper() not in allowed_statuses:
                raise ValueError(f"Status must be one of: {allowed_statuses}")
            return v.upper()
        return v


class MatriculaInDB(MatriculaBase):
    """Schema for enrollment as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MatriculaOut(MatriculaInDB):
    """Schema for enrollment output."""


class MatriculaFilter(BaseModel):
    """Schema for filtering enrollments."""

    student_id: Optional[str] = None
    school_id: Optional[int] = None
    grade: Optional[str] = None
    status: Optional[str] = None
    year: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    skip: Optional[int] = Field(0, ge=0)
    limit: Optional[int] = Field(100, ge=1, le=1000)


# Historico Escolar schemas
class HistoricoBase(BaseModel):
    """Base schema for academic history."""

    student_id: str = Field(..., description="Student unique identifier")
    subject: str = Field(..., description="Subject name")
    grade: float = Field(..., ge=0, le=20, description="Grade (0-20)")
    credits: int = Field(..., ge=1, description="Subject credits")
    semester: str = Field(..., description="Semester (e.g., '2024.1')")
    year: int = Field(..., description="Academic year")
    teacher_id: Optional[str] = Field(None, description="Teacher ID")

    @validator("semester")
    def validate_semester(cls, v):
        import re

        if not re.match(r"^\d{4}\.[12]$", v):
            raise ValueError("Semester must be in format YYYY.N where N is 1 or 2")
        return v


class HistoricoCreate(HistoricoBase):
    """Schema for creating academic history record."""


class HistoricoUpdate(BaseModel):
    """Schema for updating academic history record."""

    subject: Optional[str] = None
    grade: Optional[float] = Field(None, ge=0, le=20)
    credits: Optional[int] = Field(None, ge=1)
    semester: Optional[str] = None
    year: Optional[int] = None
    teacher_id: Optional[str] = None

    @validator("semester")
    def validate_semester(cls, v):
        if v is not None:
            import re

            if not re.match(r"^\d{4}\.[12]$", v):
                raise ValueError("Semester must be in format YYYY.N where N is 1 or 2")
            return v
        return v


class HistoricoInDB(HistoricoBase):
    """Schema for academic history as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HistoricoOut(HistoricoInDB):
    """Schema for academic history output."""


# Ensino Superior schemas
class EnsinoSuperiorBase(BaseModel):
    """Base schema for higher education."""

    student_id: str = Field(..., description="Student unique identifier")
    institution_id: int = Field(..., description="Educational institution ID")
    course: str = Field(..., description="Course name")
    degree: str = Field(..., description="Degree type")
    start_date: date = Field(..., description="Course start date")
    expected_end_date: Optional[date] = Field(
        None, description="Expected completion date"
    )
    actual_end_date: Optional[date] = Field(None, description="Actual completion date")
    status: str = Field(default="ACTIVE", description="Enrollment status")
    gpa: Optional[float] = Field(None, ge=0, le=20, description="Grade Point Average")

    @validator("degree")
    def validate_degree(cls, v):
        allowed_degrees = ["BACHELOR", "MASTER", "PHD", "SPECIALIZATION", "TECHNICAL"]
        if v.upper() not in allowed_degrees:
            raise ValueError(f"Degree must be one of: {allowed_degrees}")
        return v.upper()

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["ACTIVE", "COMPLETED", "SUSPENDED", "DROPPED", "GRADUATED"]
        if v.upper() not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v.upper()


class EnsinoSuperiorCreate(EnsinoSuperiorBase):
    """Schema for creating higher education record."""


class EnsinoSuperiorUpdate(BaseModel):
    """Schema for updating higher education record."""

    course: Optional[str] = None
    degree: Optional[str] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0, le=20)

    @validator("degree")
    def validate_degree(cls, v):
        if v is not None:
            allowed_degrees = [
                "BACHELOR",
                "MASTER",
                "PHD",
                "SPECIALIZATION",
                "TECHNICAL",
            ]
            if v.upper() not in allowed_degrees:
                raise ValueError(f"Degree must be one of: {allowed_degrees}")
            return v.upper()
        return v

    @validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = [
                "ACTIVE",
                "COMPLETED",
                "SUSPENDED",
                "DROPPED",
                "GRADUATED",
            ]
            if v.upper() not in allowed_statuses:
                raise ValueError(f"Status must be one of: {allowed_statuses}")
            return v.upper()
        return v


class EnsinoSuperiorInDB(EnsinoSuperiorBase):
    """Schema for higher education as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnsinoSuperiorOut(EnsinoSuperiorInDB):
    """Schema for higher education output."""


# Statistics and Analytics schemas
class EducationStatistics(BaseModel):
    """Schema for education statistics."""

    total_enrollments: int
    unique_students: int
    by_grade: Dict[str, int]
    by_status: Dict[str, int]
    academic_year: Optional[int] = None
    last_updated: datetime


class StudentAcademicSummary(BaseModel):
    """Schema for student academic summary."""

    student_id: str
    current_enrollment: Optional[MatriculaOut]
    academic_history: List[HistoricoOut]
    higher_education: List[EnsinoSuperiorOut]
    gpa: Optional[float]
    total_credits: int
    enrollment_status: str


class SchoolEnrollmentReport(BaseModel):
    """Schema for school enrollment report."""

    school_id: int
    school_name: str
    total_enrollments: int
    by_grade: Dict[str, int]
    active_students: int
    new_enrollments_this_year: int
    graduation_rate: float


# Batch operation schemas
class MatriculaBatchCreate(BaseModel):
    """Schema for batch creating enrollments."""

    enrollments: List[MatriculaCreate] = Field(..., min_items=1, max_items=100)


class HistoricoBatchCreate(BaseModel):
    """Schema for batch creating academic history records."""

    records: List[HistoricoCreate] = Field(..., min_items=1, max_items=100)


# Response schemas
class EducationListResponse(BaseModel):
    """Schema for paginated list response."""

    items: List[Dict[str, Any]]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class EducationBatchResponse(BaseModel):
    """Schema for batch operation response."""

    successful: List[Dict[str, Any]]
    failed: List[Dict[str, Any]]
    total_attempted: int
    total_successful: int
    total_failed: int


# Certificate and Diploma schemas
class AcademicCertificateRequest(BaseModel):
    """Schema for academic certificate request."""

    student_id: str
    certificate_type: str = Field(
        ..., regex="^(ENROLLMENT|COMPLETION|TRANSCRIPT|DIPLOMA)$"
    )
    purpose: str
    requested_by: str
    contact_info: str


class AcademicCertificate(BaseModel):
    """Schema for academic certificate."""

    id: int
    student_id: str
    certificate_type: str
    issue_date: datetime
    expiry_date: Optional[datetime]
    issued_by: str
    verification_code: str
    status: str

    class Config:
        from_attributes = True


# Export all schemas
__all__ = [
    # Matricula schemas
    "MatriculaBase",
    "MatriculaCreate",
    "MatriculaUpdate",
    "MatriculaInDB",
    "MatriculaOut",
    "MatriculaFilter",
    # Historico schemas
    "HistoricoBase",
    "HistoricoCreate",
    "HistoricoUpdate",
    "HistoricoInDB",
    "HistoricoOut",
    # Ensino Superior schemas
    "EnsinoSuperiorBase",
    "EnsinoSuperiorCreate",
    "EnsinoSuperiorUpdate",
    "EnsinoSuperiorInDB",
    "EnsinoSuperiorOut",
    # Statistics schemas
    "EducationStatistics",
    "StudentAcademicSummary",
    "SchoolEnrollmentReport",
    # Batch operation schemas
    "MatriculaBatchCreate",
    "HistoricoBatchCreate",
    # Response schemas
    "EducationListResponse",
    "EducationBatchResponse",
    # Certificate schemas
    "AcademicCertificateRequest",
    "AcademicCertificate",
]
