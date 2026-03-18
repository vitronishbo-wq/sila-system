"""
Educação (Education) Module Domain Events
ACAO Compliance: All events track educational records and certifications.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class EducationInstitutionRegistered(AuditableEvent):
    """Emitted when an education institution is registered."""
    institution_id: UUID
    institution_name: str
    institution_type: str
    registration_number: str = ''
    location: str = ''

    def __post_init__(self):
        self.aggregate_type = 'EducationInstitution'
        self.event_type = 'EducationInstitutionRegistered'
        super().__post_init__()

class StudentEnrolled(AuditableEvent):
    """Emitted when a student is enrolled."""
    student_id: UUID
    institution_id: UUID
    enrollment_date: date
    program_code: str = ''
    grade_level: str = ''

    def __post_init__(self):
        self.aggregate_type = 'StudentEnrollment'
        self.event_type = 'StudentEnrolled'
        super().__post_init__()

class AcademicDegreeAwarded(ComplianceEvent):
    """Emitted when academic degree is awarded (ACAO compliance)."""
    student_id: UUID
    degree_type: str
    degree_date: date
    institution_id: UUID
    certificate_number: str = ''
    issuing_authority: str = ''

    def __post_init__(self):
        self.aggregate_type = 'AcademicDegree'
        self.event_type = 'AcademicDegreeAwarded'
        super().__post_init__()

class EducationInstitutionStatusChanged(StatusChangeEvent):
    """Track education institution status transitions."""
    institution_id: UUID
    reason: str = ''

    def __post_init__(self):
        self.aggregate_type = 'EducationInstitution'
        self.event_type = 'EducationInstitutionStatusChanged'
        super().__post_init__()

class TeacherCertificationIssued(ComplianceEvent):
    """Emitted when teacher certification is issued."""
    teacher_id: UUID
    certification_number: str
    subject_area: str
    certification_date: date
    expiry_date: Optional[date] = None
    issuing_authority: str = ''

    def __post_init__(self):
        self.aggregate_type = 'TeacherCertification'
        self.event_type = 'TeacherCertificationIssued'
        super().__post_init__()