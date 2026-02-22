"""Testes de integração para os serviços do módulo justice."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.justice.models.case import Case, CasePriority, CaseStatus, CaseType
from modules.justice.services import JusticeService


@pytest.fixture
def justice_service():
    """Retorna uma instância do serviço jurídico."""
    return JusticeService()


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
def sample_case_data():
    """Dados de exemplo para casos jurídicos."""
    return {
        "numero_processo": "2025.0001234-5",
        "tipo_caso": CaseType.CIVIL,
        "status": CaseStatus.REGISTERED,
        "prioridade": CasePriority.MEDIUM,
        "titulo": "Cobrança de Dívida",
        "descricao": "Ação de cobrança de dívida contratual",
        "cliente_id": str(uuid4()),
        "advogado_id": str(uuid4()),
        "data_abertura": datetime.now(timezone.utc),
    }


class TestJusticeService:
    """Testes para os serviços do módulo justice."""

    @patch("modules.justice.services.get_db")
    async def test_create_legal_case(
        self, mock_get_db, justice_service, sample_case_data
    ):
        """Testa a criação de um caso jurídico."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do objeto criado
        mock_case = MagicMock()
        mock_case.id = 1
        mock_case.numero_processo = sample_case_data["numero_processo"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await justice_service.create_case(sample_case_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_get_case_by_id(self, mock_get_db, justice_service, sample_case_data):
        """Testa a busca de caso por ID."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso encontrado
        mock_case = MagicMock()
        mock_case.id = 1
        mock_case.numero_processo = sample_case_data["numero_processo"]
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        # Executa
        result = await justice_service.get_case_by_id(1)

        # Verificações
        assert result is not None
        assert result.id == 1
        mock_session.query.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_update_case_status(
        self, mock_get_db, justice_service, sample_case_data
    ):
        """Testa a atualização do status de um caso."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso existente
        mock_case = MagicMock()
        mock_case.id = 1
        mock_case.status = CaseStatus.REGISTERED
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        # Executa
        result = await justice_service.update_case_status(1, CaseStatus.IN_PROGRESS)

        # Verificações
        assert result is True
        assert mock_case.status == CaseStatus.IN_PROGRESS
        mock_session.commit.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_delete_legal_case(self, mock_get_db, justice_service):
        """Testa a exclusão de um caso jurídico."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso existente
        mock_case = MagicMock()
        mock_case.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        # Executa
        result = await justice_service.delete_case(1)

        # Verificações
        assert result is True
        mock_session.delete.assert_called_once_with(mock_case)
        mock_session.commit.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_list_cases_by_status(self, mock_get_db, justice_service):
        """Testa a listagem de casos por status."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da lista de casos
        mock_cases = [MagicMock() for _ in range(3)]
        for case in mock_cases:
            case.status = CaseStatus.IN_PROGRESS
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_cases
        )

        # Executa
        result = await justice_service.list_cases_by_status(CaseStatus.IN_PROGRESS)

        # Verificações
        assert len(result) == 3
        for case in result:
            assert case.status == CaseStatus.IN_PROGRESS

    @patch("modules.justice.services.get_db")
    async def test_search_cases_by_process_number(self, mock_get_db, justice_service):
        """Testa a busca de casos por número de processo."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso encontrado
        mock_case = MagicMock()
        mock_case.numero_processo = "2025.0001234-5"
        mock_session.query.return_value.filter.return_value.all.return_value = [
            mock_case
        ]

        # Executa
        result = await justice_service.search_cases_by_process_number("2025.0001234-5")

        # Verificações
        assert len(result) == 1
        assert result[0].numero_processo == "2025.0001234-5"

    @patch("modules.justice.services.get_db")
    async def test_get_case_statistics(self, mock_get_db, justice_service):
        """Testa a obtenção de estatísticas de casos."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock das contagens
        mock_session.query.return_value.count.return_value = 10

        # Executa
        result = await justice_service.get_case_statistics()

        # Verificações
        assert "total_cases" in result
        assert "cases_by_status" in result
        assert "cases_by_type" in result

    async def test_validate_case_data_valid(self, justice_service, sample_case_data):
        """Testa validação de dados válidos de caso."""
        # Executa
        is_valid = await justice_service.validate_case_data(sample_case_data)

        # Verificações
        assert is_valid is True

    async def test_validate_case_data_invalid_process_number(self, justice_service):
        """Testa validação com número de processo inválido."""
        # Dados inválidos
        invalid_data = {
            "numero_processo": "",  # vazio
            "tipo_caso": CaseType.CIVIL,
            "status": CaseStatus.REGISTERED,
        }

        # Executa
        is_valid = await justice_service.validate_case_data(invalid_data)

        # Verificações
        assert is_valid is False

    async def test_validate_case_data_invalid_type(self, justice_service):
        """Testa validação com tipo de caso inválido."""
        # Dados inválidos
        invalid_data = {
            "numero_processo": "2025.0001234-5",
            "tipo_caso": "TIPO_INVALIDO",  # inválido
            "status": CaseStatus.REGISTERED,
        }

        # Executa
        is_valid = await justice_service.validate_case_data(invalid_data)

        # Verificações
        assert is_valid is False

    @patch("modules.justice.services.get_db")
    async def test_create_case_event(self, mock_get_db, justice_service):
        """Testa a criação de evento em um caso."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso existente
        mock_case = MagicMock()
        mock_case.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        # Dados do evento
        event_data = {
            "tipo_evento": "AUDIENCIA_MARCADA",
            "descricao": "Audiência marcada para dia 15/12/2025",
            "data_evento": datetime.now(timezone.utc),
        }

        # Executa
        result = await justice_service.create_case_event(1, event_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called()
        mock_session.commit.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_get_case_timeline(self, mock_get_db, justice_service):
        """Testa a obtenção da timeline de um caso."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso existente
        mock_case = MagicMock()
        mock_case.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        # Mock dos eventos
        mock_events = [MagicMock() for _ in range(3)]
        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = (
            mock_events
        )

        # Executa
        result = await justice_service.get_case_timeline(1)

        # Verificações
        assert len(result) == 3
        mock_session.query.assert_called()

    @patch("modules.justice.services.get_db")
    async def test_assign_lawyer_to_case(self, mock_get_db, justice_service):
        """Testa a atribuição de advogado a um caso."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do caso existente
        mock_case = MagicMock()
        mock_case.id = 1
        mock_case.advogado_id = None
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_case
        )

        lawyer_id = str(uuid4())

        # Executa
        result = await justice_service.assign_lawyer_to_case(1, lawyer_id)

        # Verificações
        assert result is True
        assert mock_case.advogado_id == lawyer_id
        mock_session.commit.assert_called_once()

    @patch("modules.justice.services.get_db")
    async def test_get_high_priority_cases(self, mock_get_db, justice_service):
        """Testa a busca por casos de alta prioridade."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock dos casos de alta prioridade
        mock_cases = [MagicMock() for _ in range(2)]
        for case in mock_cases:
            case.prioridade = CasePriority.HIGH
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_cases
        )

        # Executa
        result = await justice_service.get_high_priority_cases()

        # Verificações
        assert len(result) == 2
        for case in result:
            assert case.prioridade == CasePriority.HIGH
