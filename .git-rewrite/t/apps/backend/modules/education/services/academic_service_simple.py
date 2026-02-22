"""
Serviço acadêmico simplificado para testes de unidade.

Implementa lógica de negócio acadêmica básica para testes.
"""

import logging
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AcademicLevel(Enum):
    """Níveis acadêmicos."""

    ELEMENTARY = "ELEMENTARY"
    MIDDLE = "MIDDLE"
    HIGH_SCHOOL = "HIGH_SCHOOL"
    HIGHER = "HIGHER"
    GRADUATE = "GRADUATE"


class GradeStatus(Enum):
    """Status das notas."""

    APPROVED = "APPROVED"
    REPROVED = "REPROVED"
    IN_RECOVERY = "IN_RECOVERY"


class AcademicService:
    """Service class for academic operations."""

    async def create_enrollment(
        self, enrollment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new enrollment."""
        # Validação dos dados
        if not await self.validate_enrollment(enrollment_data):
            raise ValueError("Dados da matrícula inválidos")

        # Simulação de criação
        enrollment = {
            "id": 1,
            **enrollment_data,
            "created_at": datetime.now(timezone.utc),
        }

        logger.info(f"Matrícula criada: {enrollment['id']}")
        return enrollment

    async def validate_enrollment(self, enrollment_data: Dict[str, Any]) -> bool:
        """Validate enrollment data."""
        try:
            # Verifica campos obrigatórios
            if not enrollment_data.get("student_id"):
                return False

            if not enrollment_data.get("course_id"):
                return False

            # Verifica nível acadêmico
            level = enrollment_data.get("academic_level")
            if hasattr(level, "value"):
                level_value = level.value
            else:
                level_value = level

            if level_value not in [item.value for item in AcademicLevel]:
                return False

            # Verifica data da matrícula (não pode estar no passado)
            enrollment_date = enrollment_data.get("enrollment_date")
            if enrollment_date and isinstance(enrollment_date, datetime):
                if enrollment_date < datetime.now(timezone.utc):
                    return False

            # Verifica semestre (formato YYYY.N onde N é 1 ou 2)
            semester = enrollment_data.get("semester", "")
            if not semester or len(semester) != 6:
                return False

            # Verifica formato do semestre
            import re

            if not re.match(r"^\d{4}\.[12]$", semester):
                return False

            return True

        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return False

    async def create_grade(self, grade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new grade."""
        # Validação dos dados
        score = grade_data.get("score", 0)
        max_score = grade_data.get("max_score", 0)

        if score > max_score:
            raise ValueError("Nota excede pontuação máxima")

        if score < 0:
            raise ValueError("Nota não pode ser negativa")

        # Simulação de criação
        grade = {
            "id": 1,
            **grade_data,
            "created_at": datetime.now(timezone.utc),
        }

        logger.info(f"Nota criada: {grade['id']}")
        return grade

    async def calculate_final_average(self, enrollment_id: int) -> Decimal:
        """Calculate final average for enrollment."""
        # Simulação de cálculo - em produção buscaria notas do DB
        if enrollment_id == 999:
            return Decimal("0.0")

        # Dados simulados
        grades = [
            {"score": Decimal("8.0"), "weight": Decimal("0.3")},
            {"score": Decimal("7.5"), "weight": Decimal("0.3")},
            {"score": Decimal("9.0"), "weight": Decimal("0.4")},
        ]

        total_weight = Decimal("0.0")
        weighted_sum = Decimal("0.0")

        for grade in grades:
            weighted_sum += grade["score"] * grade["weight"]
            total_weight += grade["weight"]

        if total_weight == 0:
            return Decimal("0.0")

        return weighted_sum / total_weight

    async def determine_grade_status(self, average: Decimal) -> GradeStatus:
        """Determine grade status based on average."""
        if average >= Decimal("7.0"):
            return GradeStatus.APPROVED
        elif average >= Decimal("5.0"):
            return GradeStatus.IN_RECOVERY
        else:
            return GradeStatus.REPROVED

    async def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new course."""
        # Validação dos dados
        if not await self._validate_course_data(course_data):
            raise ValueError("Dados do curso inválidos")

        # Simulação de criação
        course = {
            "id": 1,
            **course_data,
            "created_at": datetime.now(timezone.utc),
        }

        logger.info(f"Curso criado: {course['id']}")
        return course

    async def _validate_course_data(self, course_data: Dict[str, Any]) -> bool:
        """Validate course data."""
        try:
            # Verifica carga horária
            workload = course_data.get("workload", 0)
            if workload <= 0 or workload > 200:
                return False

            # Verifica datas
            start_date = course_data.get("start_date")
            end_date = course_data.get("end_date")

            if start_date and end_date:
                if end_date <= start_date:
                    return False

            return True

        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return False

    async def check_course_availability(self, course_data: Dict[str, Any]) -> bool:
        """Check if course has available slots."""
        max_students = course_data.get("max_students", 0)
        current_enrollments = course_data.get("current_enrollments", 0)

        return current_enrollments < max_students

    async def calculate_gpa(self, grades: List[Dict[str, Any]]) -> Decimal:
        """Calculate Grade Point Average."""
        if not grades:
            return Decimal("0.0")

        total_credits = sum(grade["credits"] for grade in grades)
        if total_credits == 0:
            return Decimal("0.0")

        weighted_sum = sum(grade["score"] * grade["credits"] for grade in grades)
        return weighted_sum / total_credits

    async def calculate_academic_progress(
        self,
        student_id: int,
        total_required_credits: int,
        completed_credits: int = None,
    ) -> Dict[str, Any]:
        """Calculate academic progress."""
        if completed_credits is None:
            completed_credits = total_required_credits // 2  # Simulação

        percentage = (
            (completed_credits / total_required_credits) * 100
            if total_required_credits > 0
            else 0
        )

        if percentage >= 70:
            status = "ON_TRACK"
        elif percentage >= 30:
            status = "BEHIND"
        else:
            status = "CRITICAL"

        return {
            "percentage": percentage,
            "status": status,
            "remaining_credits": total_required_credits - completed_credits,
            "completed_credits": completed_credits,
        }

    async def can_enroll_in_level(
        self, student_id: int, student_level: AcademicLevel, course_level: AcademicLevel
    ) -> bool:
        """Check if student can enroll in course level."""
        # Regras de progressão
        level_order = [
            AcademicLevel.ELEMENTARY,
            AcademicLevel.MIDDLE,
            AcademicLevel.HIGH_SCHOOL,
            AcademicLevel.HIGHER,
            AcademicLevel.GRADUATE,
        ]

        student_index = level_order.index(student_level)
        course_index = level_order.index(course_level)

        # Permite matricular no mesmo nível ou um nível acima
        return course_index <= student_index + 1

    async def check_prerequisites(
        self,
        student_id: int,
        prerequisites: List[str],
        completed_courses: List[str] = None,
    ) -> bool:
        """Check if student has completed prerequisites."""
        if completed_courses is None:
            # Simulação - em produção buscaria do DB
            completed_courses = ["MAT101", "MAT102"]

        return all(prereq in completed_courses for prereq in prerequisites)

    async def generate_academic_report(
        self, student_id: int, semester: str
    ) -> Dict[str, Any]:
        """Generate academic report for student."""
        # Simulação de relatório
        return {
            "student_id": student_id,
            "semester": semester,
            "total_enrollments": 2,
            "courses_completed": 1,
            "gpa": Decimal("7.5"),
            "status": "ACTIVE",
            "generated_at": datetime.now(timezone.utc),
        }
