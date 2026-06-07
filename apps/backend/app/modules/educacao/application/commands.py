"""
Educação (Education) Module Command Handlers
Shows the pattern for education operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.educacao.domain.events import (
    AcademicDegreeAwarded,
    EducationInstitutionRegistered,
    StudentEnrolled,
)

logger = logging.getLogger(__name__)


class RegisterEducationInstitutionCommandHandler:
    """Register education institution."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        institution_id: UUID,
        institution_name: str,
        institution_type: str,
        registration_number: str = "",
        location: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering education institution {institution_name}")
        try:
            event = EducationInstitutionRegistered(
                aggregate_id=institution_id,
                aggregate_type="EducationInstitution",
                event_type="EducationInstitutionRegistered",
                institution_id=institution_id,
                institution_name=institution_name,
                institution_type=institution_type,
                registration_number=registration_number,
                location=location,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterEducationInstitution",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Institution registered: {institution_id}")
        except Exception as e:
            logger.error(f"Error registering institution: {e}")
            raise


class EnrollStudentCommandHandler:
    """Enroll student."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        student_id: UUID,
        institution_id: UUID,
        program_code: str = "",
        grade_level: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Enrolling student {student_id}")
        try:
            event = StudentEnrolled(
                aggregate_id=student_id,
                aggregate_type="StudentEnrollment",
                event_type="StudentEnrolled",
                student_id=student_id,
                institution_id=institution_id,
                enrollment_date=date.today(),
                program_code=program_code,
                grade_level=grade_level,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "student_id": str(student_id),
                    "command_name": "EnrollStudent",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Student enrolled: {student_id}")
        except Exception as e:
            logger.error(f"Error enrolling student: {e}")
            raise


class AwardAcademicDegreeCommandHandler:
    """Award academic degree (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        student_id: UUID,
        degree_type: str,
        institution_id: UUID,
        certificate_number: str = "",
        issuing_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Awarding {degree_type} degree to student {student_id}")
        try:
            event = AcademicDegreeAwarded(
                aggregate_id=student_id,
                aggregate_type="AcademicDegree",
                event_type="AcademicDegreeAwarded",
                student_id=student_id,
                degree_type=degree_type,
                degree_date=date.today(),
                institution_id=institution_id,
                certificate_number=certificate_number,
                issuing_authority=issuing_authority,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "student_id": str(student_id),
                    "command_name": "AwardAcademicDegree",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Degree awarded to student {student_id}")
        except Exception as e:
            logger.error(f"Error awarding degree: {e}")
            raise
