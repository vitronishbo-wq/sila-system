"""Testes de integração para os serviços do módulo education."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.education.services import EducationService


@pytest.fixture
def education_service():
    """Retorna uma instância do serviço educacional."""
    return EducationService()


@pytest.fixture
def mock_db_session():
    """Mock da sessão do banco de dados."""
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    session.query = MagicMock()
    session.filter = MagicMock()
    session.first = MagicMock()
    session.all = MagicMock()
    session.delete = MagicMock()
    return session


@pytest.fixture
def sample_enrollment_data():
    """Dados de exemplo para matrículas estudantis."""
    return {
        "numero_matricula": "2025EDU001234",
        "nome_estudante": "João da Silva",
        "data_nascimento": datetime(2010, 5, 15, tzinfo=timezone.utc),
        "genero": "M",
        "nome_responsavel": "Maria da Silva",
        "contato_responsavel": "912345678",
        "escola_id": str(uuid4()),
        "serie": "5º Ano",
        "turma": "A",
        "turno": "MANHA",
        "data_matricula": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_scholarship_data():
    """Dados de exemplo para bolsas de estudos."""
    return {
        "tipo_bolsa": "INTEGRAL",
        "motivo_bolsa": "BAIXA_RENDA",
        "percentual_desconto": 100.0,
        "estudante_id": str(uuid4()),
        "instituicao_id": str(uuid4()),
        "data_concessao": datetime.now(timezone.utc),
        "vigencia_inicio": datetime(2025, 1, 1, tzinfo=timezone.utc),
        "vigencia_fim": datetime(2025, 12, 31, tzinfo=timezone.utc),
        "status": "ATIVA",
    }


class TestEducationService:
    """Testes para os serviços do módulo education."""

    @patch("modules.education.services.get_db")
    async def test_create_student_enrollment(
        self, mock_get_db, education_service, sample_enrollment_data
    ):
        """Testa a criação de uma matrícula estudantil."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do objeto criado
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_enrollment.numero_matricula = sample_enrollment_data["numero_matricula"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await education_service.create_enrollment(sample_enrollment_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_get_enrollment_by_id(
        self, mock_get_db, education_service, sample_enrollment_data
    ):
        """Testa a busca de matrícula por ID."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da matrícula encontrada
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_enrollment.numero_matricula = sample_enrollment_data["numero_matricula"]
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_enrollment
        )

        # Executa
        result = await education_service.get_enrollment_by_id(1)

        # Verificações
        assert result is not None
        assert result.id == 1
        mock_session.query.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_update_enrollment(
        self, mock_get_db, education_service, sample_enrollment_data
    ):
        """Testa a atualização de uma matrícula estudantil."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da matrícula existente
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_enrollment.turma = "A"
        mock_enrollment.turno = "MANHA"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_enrollment
        )

        # Dados de atualização
        update_data = {"turma": "B", "turno": "TARDE"}

        # Executa
        result = await education_service.update_enrollment(1, update_data)

        # Verificações
        assert result is not None
        assert mock_enrollment.turma == "B"
        assert mock_enrollment.turno == "TARDE"
        mock_session.commit.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_delete_enrollment(self, mock_get_db, education_service):
        """Testa a exclusão de uma matrícula estudantil."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da matrícula existente
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_enrollment
        )

        # Executa
        result = await education_service.delete_enrollment(1)

        # Verificações
        assert result is True
        mock_session.delete.assert_called_once_with(mock_enrollment)
        mock_session.commit.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_list_enrollments_by_school(self, mock_get_db, education_service):
        """Testa a listagem de matrículas por escola."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da lista de matrículas
        mock_enrollments = [MagicMock() for _ in range(3)]
        for enrollment in mock_enrollments:
            enrollment.escola_id = str(uuid4())
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_enrollments
        )

        school_id = str(uuid4())

        # Executa
        result = await education_service.list_enrollments_by_school(school_id)

        # Verificações
        assert len(result) == 3
        mock_session.query.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_create_scholarship(
        self, mock_get_db, education_service, sample_scholarship_data
    ):
        """Testa a criação de uma bolsa de estudos."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do objeto criado
        mock_scholarship = MagicMock()
        mock_scholarship.id = 1
        mock_scholarship.tipo_bolsa = sample_scholarship_data["tipo_bolsa"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await education_service.create_scholarship(sample_scholarship_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_list_scholarships_by_student(self, mock_get_db, education_service):
        """Testa a listagem de bolsas por estudante."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da lista de bolsas
        mock_scholarships = [MagicMock() for _ in range(2)]
        for scholarship in mock_scholarships:
            scholarship.estudante_id = str(uuid4())
            scholarship.status = "ATIVA"
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_scholarships
        )

        student_id = str(uuid4())

        # Executa
        result = await education_service.list_scholarships_by_student(student_id)

        # Verificações
        assert len(result) == 2
        for scholarship in result:
            assert scholarship.estudante_id == student_id

    @patch("modules.education.services.get_db")
    async def test_get_education_statistics(self, mock_get_db, education_service):
        """Testa a obtenção de estatísticas educacionais."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock das contagens
        mock_session.query.return_value.count.return_value = 50

        # Executa
        result = await education_service.get_education_statistics()

        # Verificações
        assert "total_enrollments" in result
        assert "active_scholarships" in result
        assert "schools_count" in result

    async def test_validate_enrollment_data_valid(
        self, education_service, sample_enrollment_data
    ):
        """Testa validação de dados válidos de matrícula."""
        # Executa
        is_valid = await education_service.validate_enrollment_data(
            sample_enrollment_data
        )

        # Verificações
        assert is_valid is True

    async def test_validate_enrollment_data_invalid(self, education_service):
        """Testa validação com dados inválidos."""
        # Dados inválidos
        invalid_data = {
            "numero_matricula": "",  # vazio
            "nome_estudante": "",  # vazio
            "data_nascimento": None,  # nulo
            "escola_id": "uuid-invalido",  # formato inválido
        }

        # Executa
        is_valid = await education_service.validate_enrollment_data(invalid_data)

        # Verificações
        assert is_valid is False

    @patch("modules.education.services.get_db")
    async def test_search_enrollments_by_name(self, mock_get_db, education_service):
        """Testa a busca de matrículas por nome do estudante."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock das matrículas encontradas
        mock_enrollments = [MagicMock() for _ in range(2)]
        for enrollment in mock_enrollments:
            enrollment.nome_estudante = "João da Silva"
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_enrollments
        )

        # Executa
        result = await education_service.search_enrollments_by_name("João")

        # Verificações
        assert len(result) == 2
        for enrollment in result:
            assert "João" in enrollment.nome_estudante

    @patch("modules.education.services.get_db")
    async def test_create_school_transfer(self, mock_get_db, education_service):
        """Testa a criação de uma transferência escolar."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da matrícula existente
        mock_enrollment = MagicMock()
        mock_enrollment.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_enrollment
        )

        # Dados da transferência
        transfer_data = {
            "matricula_id": 1,
            "escola_origem_id": str(uuid4()),
            "escola_destino_id": str(uuid4()),
            "motivo_transferencia": "MUDANCA_DE_ENDERECO",
            "data_transferencia": datetime.now(timezone.utc),
            "status": "SOLICITADA",
        }

        # Executa
        result = await education_service.create_school_transfer(transfer_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called()
        mock_session.commit.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_get_student_academic_record(self, mock_get_db, education_service):
        """Testa a obtenção do histórico acadêmico de um estudante."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock das matrículas do estudante
        mock_enrollments = [MagicMock() for _ in range(2)]
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_enrollments
        )

        student_id = str(uuid4())

        # Executa
        result = await education_service.get_student_academic_record(student_id)

        # Verificações
        assert "enrollments" in result
        assert "grades" in result
        assert "attendance" in result
        assert len(result["enrollments"]) == 2

    @patch("modules.education.services.get_db")
    async def test_create_school_meal_record(self, mock_get_db, education_service):
        """Testa a criação de um registro de merenda escolar."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Dados da refeição
        meal_data = {
            "data_refeicao": datetime.now(timezone.utc),
            "tipo_refeicao": "ALMOCO",
            "escola_id": str(uuid4()),
            "estudante_id": str(uuid4()),
            "nutricionista_responsavel": "Dr. Ana Nutricionista",
            "cardapio": "Arroz, feijão, carne, salada e fruta",
            "calorias": 650,
            "observacoes": "Refeição balanceada",
        }

        # Mock do objeto criado
        mock_meal = MagicMock()
        mock_meal.id = 1
        mock_meal.tipo_refeicao = meal_data["tipo_refeicao"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await education_service.create_school_meal_record(meal_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_list_school_meals_by_date(self, mock_get_db, education_service):
        """Testa a listagem de refeições por data."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da lista de refeições
        mock_meals = [MagicMock() for _ in range(3)]
        for meal in mock_meals:
            meal.data_refeicao = datetime.now(timezone.utc).date()
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_meals
        )

        # Executa
        result = await education_service.list_school_meals_by_date(
            datetime.now(timezone.utc).date()
        )

        # Verificações
        assert len(result) == 3
        mock_session.query.assert_called_once()

    @patch("modules.education.services.get_db")
    async def test_create_adult_literacy_record(self, mock_get_db, education_service):
        """Testa a criação de registro de alfabetização de adultos."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Dados do registro
        literacy_data = {
            "participante_id": str(uuid4()),
            "nivel_alfabetizacao": "INICIANTE",
            "data_inscricao": datetime.now(timezone.utc),
            "turma_id": str(uuid4()),
            "instrutor_id": str(uuid4()),
            "frequencia": 85.5,
            "observacoes": "Progresso satisfatório",
        }

        # Mock do objeto criado
        mock_literacy = MagicMock()
        mock_literacy.id = 1
        mock_literacy.nivel_alfabetizacao = literacy_data["nivel_alfabetizacao"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await education_service.create_adult_literacy_record(literacy_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
