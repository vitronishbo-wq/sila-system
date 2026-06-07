"""
Educação (Education) Module Event Handlers
Handlers that process education domain events.
"""

import logging
from collections.abc import Awaitable, Callable

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.educacao.domain.events import (
    AcademicDegreeAwarded,
    EducationInstitutionRegistered,
    EducationInstitutionStatusChanged,
    StudentEnrolled,
    TeacherCertificationIssued,
)

logger = logging.getLogger(__name__)


async def handle_education_institution_registered(event: EducationInstitutionRegistered) -> None:
    """Handler for EducationInstitutionRegistered events."""
    logger.info(f"Education institution {event.institution_name} registered")
    pass


async def handle_student_enrolled(event: StudentEnrolled) -> None:
    """Handler for StudentEnrolled events."""
    logger.info(f"Student {event.aggregate_id} enrolled in program {event.program_code}")
    pass


async def handle_academic_degree_awarded(event: AcademicDegreeAwarded) -> None:
    """Handler for AcademicDegreeAwarded events (ACAO compliance)."""
    logger.info(f"Degree {event.certificate_number} awarded to student {event.aggregate_id}")
    pass


async def handle_education_institution_status_changed(
    event: EducationInstitutionStatusChanged,
) -> None:
    """Handler for EducationInstitutionStatusChanged events."""
    logger.info(f"Institution status changed: {event.old_status} -> {event.new_status}")
    pass


async def handle_teacher_certification_issued(event: TeacherCertificationIssued) -> None:
    """Handler for TeacherCertificationIssued events (ACAO compliance)."""
    logger.info(
        f"Certification {event.certification_number} issued to teacher {event.aggregate_id}"
    )
    pass


EDUCACAO_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {
    "EducationInstitutionRegistered": handle_education_institution_registered,
    "StudentEnrolled": handle_student_enrolled,
    "AcademicDegreeAwarded": handle_academic_degree_awarded,
    "EducationInstitutionStatusChanged": handle_education_institution_status_changed,
    "TeacherCertificationIssued": handle_teacher_certification_issued,
}
