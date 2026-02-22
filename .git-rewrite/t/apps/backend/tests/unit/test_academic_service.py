"""
Testes de unidade para o serviço acadêmico.

Foco na lógica de negócio educacional com mocking adequado para isolar
a camada de persistência e testar regras de negócio específicas.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.education.models.course import Course, CourseType
from modules.education.models.enrollment import Enrollment, EnrollmentStatus
from modules.education.models.grade import Grade
from modules.education.schemas import (
    AcademicStatistics,
    CourseCreate,
    EnrollmentCreate,
    EnrollmentUpdate,
    GradeCreate,
)
from modules.education.services.academic_service import (
    AcademicLevel,
    AcademicService,
    GradeStatus,
)


class TestAcademicServiceUnit:
    """Testes de unidade para AcademicService."""

    @pytest.fixture
    def service(self):
        """Instância do serviço para testes."""
        return AcademicService()

    @pytest.fixture
    def mock_db(self):
        """Mock do banco de dados."""
        db = AsyncMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()
        db.delete = MagicMock()

        # Mock para query
        query_mock = MagicMock()
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.first.return_value = None
        query_mock.all.return_value = []
        query_mock.count.return_value = 0
        db.query.return_value = query_mock

        return db

    @pytest.fixture
    def sample_enrollment_data(self):
        """Dados de exemplo para matrícula."""
        return {
            "student_id": str(uuid4()),
            "course_id": str(uuid4()),
            "enrollment_date": datetime.now(timezone.utc),
            "academic_level": AcademicLevel.HIGH_SCHOOL,
            "semester": "2025.1",
            "status": EnrollmentStatus.ACTIVE,
        }

    @pytest.fixture
    def sample_course_data(self):
        """Dados de exemplo para curso."""
        return {
            "name": "Matemática Avançada",
            "code": "MAT301",
            "description": "Curso de matemática avançada",
            "credits": 4,
            "workload": 60,  # horas
            "academic_level": AcademicLevel.HIGH_SCHOOL,
            "course_type": CourseType.MANDATORY,
            "max_students": 30,
            "start_date": datetime(2025, 2, 1, tzinfo=timezone.utc),
            "end_date": datetime(2025, 6, 30, tzinfo=timezone.utc),
        }

    @pytest.fixture
    def mock_enrollment(self):
        """Mock de matrícula."""
        enrollment = MagicMock()
        enrollment.id = 1
        enrollment.student_id = str(uuid4())
        enrollment.course_id = str(uuid4())
        enrollment.status = EnrollmentStatus.ACTIVE
        enrollment.academic_level = AcademicLevel.HIGH_SCHOOL
        enrollment.semester = "2025.1"
        enrollment.enrollment_date = datetime.now(timezone.utc)
        return enrollment

    @pytest.fixture
    def mock_course(self):
        """Mock de curso."""
        course = MagicMock()
        course.id = 1
        course.name = "Matemática Avançada"
        course.code = "MAT301"
        course.credits = 4
        course.workload = 60
        course.max_students = 30
        course.current_enrollments = 25
        course.academic_level = AcademicLevel.HIGH_SCHOOL
        return course

    # Testes de matrícula
    @pytest.mark.asyncio
    async def test_create_enrollment_success(
        self, service, mock_db, sample_enrollment_data
    ):
        """Testa criação bem-sucedida de matrícula."""
        # Arrange
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()

        # Act
        result = await service.create_enrollment(sample_enrollment_data)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_enrollment_duplicate_course(
        self, service, mock_db, sample_enrollment_data
    ):
        """Testa matrícula duplicada no mesmo curso."""
        # Arrange
        existing_enrollment = MagicMock()
        existing_enrollment.student_id = sample_enrollment_data["student_id"]
        existing_enrollment.course_id = sample_enrollment_data["course_id"]
        mock_db.query.return_value.filter.return_value.first.return_value = (
            existing_enrollment
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Aluno já matriculado neste curso"):
            await service.create_enrollment(sample_enrollment_data)

    @pytest.mark.asyncio
    async def test_create_enrollment_course_full(
        self, service, mock_db, sample_enrollment_data, mock_course
    ):
        """Testa matrícula em curso lotado."""
        # Arrange
        mock_course.current_enrollments = 30  # igual ao max_students
        mock_db.query.return_value.filter.return_value.first.return_value = mock_course

        # Act & Assert
        with pytest.raises(ValueError, match="Curso lotado"):
            await service.create_enrollment(sample_enrollment_data)

    @pytest.mark.asyncio
    async def test_create_enrollment_prerequisites_not_met(
        self, service, mock_db, sample_enrollment_data
    ):
        """Testa matrícula sem pré-requisitos."""
        # Arrange
        mock_course = MagicMock()
        mock_course.prerequisites = ["MAT101", "MAT102"]
        mock_db.query.return_value.filter.return_value.first.return_value = mock_course

        # Mock para verificar cursos concluídos
        mock_db.query.return_value.filter.return_value.all.return_value = (
            []
        )  # nenhum curso concluído

        # Act & Assert
        with pytest.raises(ValueError, match="Pré-requisitos não atendidos"):
            await service.create_enrollment(sample_enrollment_data)

    # Testes de validação de matrícula
    @pytest.mark.asyncio
    async def test_validate_enrollment_valid(self, service, sample_enrollment_data):
        """Testa validação de matrícula válida."""
        # Act
        result = await service.validate_enrollment(sample_enrollment_data)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_enrollment_invalid_level(
        self, service, sample_enrollment_data
    ):
        """Testa validação com nível acadêmico inválido."""
        # Arrange
        sample_enrollment_data["academic_level"] = "INVALID_LEVEL"

        # Act
        result = await service.validate_enrollment(sample_enrollment_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_enrollment_past_date(self, service, sample_enrollment_data):
        """Testa validação com data no passado."""
        # Arrange
        sample_enrollment_data["enrollment_date"] = datetime(
            2020, 1, 1, tzinfo=timezone.utc
        )

        # Act
        result = await service.validate_enrollment(sample_enrollment_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_enrollment_invalid_semester(
        self, service, sample_enrollment_data
    ):
        """Testa validação com semestre inválido."""
        # Arrange
        sample_enrollment_data["semester"] = "2025.3"  # semestre inválido

        # Act
        result = await service.validate_enrollment(sample_enrollment_data)

        # Assert
        assert result is False

    # Testes de notas
    @pytest.mark.asyncio
    async def test_create_grade_success(self, service, mock_db):
        """Testa criação bem-sucedida de nota."""
        # Arrange
        grade_data = {
            "enrollment_id": 1,
            "assessment_type": "Prova Final",
            "score": Decimal("8.5"),
            "max_score": Decimal("10.0"),
            "assessment_date": datetime.now(timezone.utc),
        }
        mock_grade = MagicMock()
        mock_grade.id = 1
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()

        # Act
        result = await service.create_grade(grade_data)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_grade_invalid_score(self, service, mock_db):
        """Testa criação de nota com pontuação inválida."""
        # Arrange
        grade_data = {
            "enrollment_id": 1,
            "assessment_type": "Prova Final",
            "score": Decimal("11.0"),  # acima do máximo
            "max_score": Decimal("10.0"),
            "assessment_date": datetime.now(timezone.utc),
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Nota excede pontuação máxima"):
            await service.create_grade(grade_data)

    @pytest.mark.asyncio
    async def test_create_grade_negative_score(self, service, mock_db):
        """Testa criação de nota com pontuação negativa."""
        # Arrange
        grade_data = {
            "enrollment_id": 1,
            "assessment_type": "Prova Final",
            "score": Decimal("-1.0"),  # negativa
            "max_score": Decimal("10.0"),
            "assessment_date": datetime.now(timezone.utc),
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Nota não pode ser negativa"):
            await service.create_grade(grade_data)

    # Testes de cálculo de média
    @pytest.mark.asyncio
    async def test_calculate_final_average_approved(self, service, mock_db):
        """Testa cálculo de média final com aprovação."""
        # Arrange
        grades = [
            MagicMock(score=Decimal("8.0"), weight=Decimal("0.3")),
            MagicMock(score=Decimal("7.5"), weight=Decimal("0.3")),
            MagicMock(score=Decimal("9.0"), weight=Decimal("0.4")),
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = grades

        # Act
        average = await service.calculate_final_average(1)

        # Assert
        expected = (
            Decimal("8.0") * Decimal("0.3")
            + Decimal("7.5") * Decimal("0.3")
            + Decimal("9.0") * Decimal("0.4")
        )
        assert average == expected
        assert average >= Decimal("7.0")  # aprovado

    @pytest.mark.asyncio
    async def test_calculate_final_average_reproved(self, service, mock_db):
        """Testa cálculo de média final com reprovação."""
        # Arrange
        grades = [
            MagicMock(score=Decimal("4.0"), weight=Decimal("0.3")),
            MagicMock(score=Decimal("5.0"), weight=Decimal("0.3")),
            MagicMock(score=Decimal("6.0"), weight=Decimal("0.4")),
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = grades

        # Act
        average = await service.calculate_final_average(1)

        # Assert
        expected = (
            Decimal("4.0") * Decimal("0.3")
            + Decimal("5.0") * Decimal("0.3")
            + Decimal("6.0") * Decimal("0.4")
        )
        assert average == expected
        assert average < Decimal("7.0")  # reprovado

    @pytest.mark.asyncio
    async def test_calculate_final_average_no_grades(self, service, mock_db):
        """Testa cálculo de média sem notas."""
        # Arrange
        mock_db.query.return_value.filter.return_value.all.return_value = []

        # Act
        average = await service.calculate_final_average(1)

        # Assert
        assert average == Decimal("0.0")

    # Testes de status de aprovação
    @pytest.mark.asyncio
    async def test_determine_grade_status_approved(self, service):
        """Testa determinação de status aprovado."""
        # Act
        status = await service.determine_grade_status(Decimal("8.5"))

        # Assert
        assert status == GradeStatus.APPROVED

    @pytest.mark.asyncio
    async def test_determine_grade_status_reproved(self, service):
        """Testa determinação de status reprovado."""
        # Act
        status = await service.determine_grade_status(Decimal("4.0"))

        # Assert
        assert status == GradeStatus.REPROVED

    @pytest.mark.asyncio
    async def test_determine_grade_status_recovery(self, service):
        """Testa determinação de status em recuperação."""
        # Act
        status = await service.determine_grade_status(Decimal("6.5"))

        # Assert
        assert status == GradeStatus.IN_RECOVERY

    # Testes de gestão de cursos
    @pytest.mark.asyncio
    async def test_create_course_success(self, service, mock_db, sample_course_data):
        """Testa criação bem-sucedida de curso."""
        # Arrange
        mock_course = MagicMock()
        mock_course.id = 1
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()

        # Act
        result = await service.create_course(sample_course_data)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_course_duplicate_code(
        self, service, mock_db, sample_course_data
    ):
        """Testa criação de curso com código duplicado."""
        # Arrange
        existing_course = MagicMock()
        existing_course.code = sample_course_data["code"]
        mock_db.query.return_value.filter.return_value.first.return_value = (
            existing_course
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Código de curso já existe"):
            await service.create_course(sample_course_data)

    @pytest.mark.asyncio
    async def test_create_course_invalid_workload(
        self, service, mock_db, sample_course_data
    ):
        """Testa criação de curso com carga horária inválida."""
        # Arrange
        sample_course_data["workload"] = 500  # muito alta

        # Act & Assert
        with pytest.raises(ValueError, match="Carga horária excede limite máximo"):
            await service.create_course(sample_course_data)

    @pytest.mark.asyncio
    async def test_create_course_invalid_dates(
        self, service, mock_db, sample_course_data
    ):
        """Testa criação de curso com datas inválidas."""
        # Arrange
        sample_course_data["end_date"] = datetime(
            2025, 1, 1, tzinfo=timezone.utc
        )  # antes do início

        # Act & Assert
        with pytest.raises(
            ValueError, match="Data de término deve ser posterior ao início"
        ):
            await service.create_course(sample_course_data)

    # Testes de verificação de vagas
    @pytest.mark.asyncio
    async def test_check_course_availability_available(self, service, mock_course):
        """Testa verificação de vagas disponíveis."""
        # Arrange
        mock_course.max_students = 30
        mock_course.current_enrollments = 25

        # Act
        available = await service.check_course_availability(mock_course)

        # Assert
        assert available is True

    @pytest.mark.asyncio
    async def test_check_course_availability_full(self, service, mock_course):
        """Testa verificação de vagas quando curso está lotado."""
        # Arrange
        mock_course.max_students = 30
        mock_course.current_enrollments = 30

        # Act
        available = await service.check_course_availability(mock_course)

        # Assert
        assert available is False

    @pytest.mark.asyncio
    async def test_check_course_availability_overbooked(self, service, mock_course):
        """Testa verificação de vagas quando curso está sobrecarregado."""
        # Arrange
        mock_course.max_students = 30
        mock_course.current_enrollments = 35

        # Act
        available = await service.check_course_availability(mock_course)

        # Assert
        assert available is False

    # Testes de cálculo acadêmico
    @pytest.mark.asyncio
    async def test_calculate_gpa_high_school(self, service):
        """Testa cálculo de GPA para ensino médio."""
        # Arrange
        grades = [
            {"score": Decimal("8.5"), "credits": 4},
            {"score": Decimal("7.0"), "credits": 3},
            {"score": Decimal("9.0"), "credits": 2},
        ]

        # Act
        gpa = await service.calculate_gpa(grades)

        # Assert
        total_credits = sum(grade["credits"] for grade in grades)
        weighted_sum = sum(grade["score"] * grade["credits"] for grade in grades)
        expected_gpa = weighted_sum / total_credits
        assert gpa == expected_gpa

    @pytest.mark.asyncio
    async def test_calculate_academic_progress_on_track(self, service, mock_db):
        """Testa cálculo de progresso acadêmico em dia."""
        # Arrange
        total_required_credits = 200
        completed_credits = 100
        mock_db.query.return_value.filter.return_value.count.return_value = (
            completed_credits
        )

        # Act
        progress = await service.calculate_academic_progress(1, total_required_credits)

        # Assert
        assert progress["percentage"] == 50.0
        assert progress["status"] == "ON_TRACK"
        assert progress["remaining_credits"] == 100

    @pytest.mark.asyncio
    async def test_calculate_academic_progress_behind(self, service, mock_db):
        """Testa cálculo de progresso acadêmico atrasado."""
        # Arrange
        total_required_credits = 200
        completed_credits = 40  # menos de 30%
        mock_db.query.return_value.filter.return_value.count.return_value = (
            completed_credits
        )

        # Act
        progress = await service.calculate_academic_progress(1, total_required_credits)

        # Assert
        assert progress["percentage"] == 20.0
        assert progress["status"] == "BEHIND"
        assert progress["remaining_credits"] == 160

    # Testes de regras de negócio complexas
    @pytest.mark.asyncio
    async def test_can_enroll_level_appropriate(self, service, mock_db):
        """Testa se aluno pode se matricular em nível apropriado."""
        # Arrange
        student_level = AcademicLevel.HIGH_SCHOOL
        course_level = AcademicLevel.HIGH_SCHOOL
        mock_db.query.return_value.filter.return_value.first.return_value = (
            None  # sem restrições
        )

        # Act
        can_enroll = await service.can_enroll_in_level(1, student_level, course_level)

        # Assert
        assert can_enroll is True

    @pytest.mark.asyncio
    async def test_can_enroll_level_inappropriate(self, service, mock_db):
        """Testa se aluno pode se matricular em nível inadequado."""
        # Arrange
        student_level = AcademicLevel.ELEMENTARY
        course_level = AcademicLevel.HIGHER  # salto muito grande
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act
        can_enroll = await service.can_enroll_in_level(1, student_level, course_level)

        # Assert
        assert can_enroll is False

    @pytest.mark.asyncio
    async def test_check_prerequisites_met(self, service, mock_db):
        """Testa verificação de pré-requisitos atendidos."""
        # Arrange
        prerequisites = ["MAT101", "MAT102"]
        completed_courses = ["MAT101", "MAT102", "MAT103"]
        mock_db.query.return_value.filter.return_value.all.return_value = (
            completed_courses
        )

        # Act
        met = await service.check_prerequisites(1, prerequisites)

        # Assert
        assert met is True

    @pytest.mark.asyncio
    async def test_check_prerequisites_not_met(self, service, mock_db):
        """Testa verificação de pré-requisitos não atendidos."""
        # Arrange
        prerequisites = ["MAT101", "MAT102", "MAT201"]
        completed_courses = ["MAT101", "MAT102"]  # falta MAT201
        mock_db.query.return_value.filter.return_value.all.return_value = (
            completed_courses
        )

        # Act
        met = await service.check_prerequisites(1, prerequisites)

        # Assert
        assert met is False

    @pytest.mark.asyncio
    async def test_generate_academic_report_empty(self, service, mock_db):
        """Testa geração de relatório acadêmico vazio."""
        # Arrange
        mock_db.query.return_value.all.return_value = []

        # Act
        report = await service.generate_academic_report(student_id=1, semester="2025.1")

        # Assert
        assert "total_enrollments" in report
        assert "gpa" in report
        assert "courses_completed" in report
        assert report["total_enrollments"] == 0

    @pytest.mark.asyncio
    async def test_generate_academic_report_with_data(self, service, mock_db):
        """Testa geração de relatório acadêmico com dados."""
        # Arrange
        mock_enrollments = [
            MagicMock(
                course__name="Matemática",
                final_grade=Decimal("8.5"),
                status=EnrollmentStatus.COMPLETED,
            ),
            MagicMock(
                course__name="Português",
                final_grade=Decimal("7.0"),
                status=EnrollmentStatus.COMPLETED,
            ),
            MagicMock(
                course__name="História",
                final_grade=None,
                status=EnrollmentStatus.ACTIVE,
            ),
        ]
        mock_db.query.return_value.all.return_value = mock_enrollments

        # Act
        report = await service.generate_academic_report(student_id=1, semester="2025.1")

        # Assert
        assert report["total_enrollments"] == 3
        assert report["courses_completed"] == 2
        assert report["gpa"] > 0
