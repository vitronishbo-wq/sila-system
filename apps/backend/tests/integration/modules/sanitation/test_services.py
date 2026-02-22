"""Testes de integração para os serviços do módulo sanitation."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.sanitation.models.sanitation import SanitationRecord
from modules.sanitation.services import SanitationService


@pytest.fixture
def sanitation_service():
    """Retorna uma instância do serviço de saneamento."""
    return SanitationService()


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
    return session


@pytest.fixture
def sample_sanitation_data():
    """Dados de exemplo para registros de saneamento."""
    return {
        "tipo_servico": "Coleta de Lixo",
        "data_servico": datetime.now(timezone.utc),
        "localizacao": "Rua dos Testes, 123",
        "status": "PENDENTE",
        "observacoes": "Coleta programada",
        "cidadao_id": str(uuid4()),
    }


class TestSanitationService:
    """Testes para os serviços do módulo sanitation."""

    @patch("modules.sanitation.services.get_db")
    async def test_create_sanitation_record(
        self, mock_get_db, sanitation_service, sample_sanitation_data
    ):
        """Testa a criação de um registro de saneamento."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do objeto criado
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.tipo_servico = sample_sanitation_data["tipo_servico"]
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Executa
        result = await sanitation_service.create_record(sample_sanitation_data)

        # Verificações
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @patch("modules.sanitation.services.get_db")
    async def test_get_sanitation_record_by_id(
        self, mock_get_db, sanitation_service, sample_sanitation_data
    ):
        """Testa a busca de registro por ID."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do registro encontrado
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.tipo_servico = sample_sanitation_data["tipo_servico"]
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_record
        )

        # Executa
        result = await sanitation_service.get_record_by_id(1)

        # Verificações
        assert result is not None
        assert result.id == 1
        mock_session.query.assert_called_once()

    @patch("modules.sanitation.services.get_db")
    async def test_update_sanitation_record(
        self, mock_get_db, sanitation_service, sample_sanitation_data
    ):
        """Testa a atualização de um registro de saneamento."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do registro existente
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.status = "PENDENTE"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_record
        )

        # Dados de atualização
        update_data = {"status": "CONCLUIDO", "observacoes": "Serviço concluído"}

        # Executa
        result = await sanitation_service.update_record(1, update_data)

        # Verificações
        assert result is not None
        mock_session.commit.assert_called_once()

    @patch("modules.sanitation.services.get_db")
    async def test_delete_sanitation_record(self, mock_get_db, sanitation_service):
        """Testa a exclusão de um registro de saneamento."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do registro existente
        mock_record = MagicMock()
        mock_record.id = 1
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_record
        )

        # Executa
        result = await sanitation_service.delete_record(1)

        # Verificações
        assert result is True
        mock_session.delete.assert_called_once_with(mock_record)
        mock_session.commit.assert_called_once()

    @patch("modules.sanitation.services.get_db")
    async def test_list_sanitation_records(self, mock_get_db, sanitation_service):
        """Testa a listagem de registros de saneamento."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock da lista de registros
        mock_records = [MagicMock() for _ in range(3)]
        mock_session.query.return_value.all.return_value = mock_records

        # Executa
        result = await sanitation_service.list_records()

        # Verificações
        assert len(result) == 3
        mock_session.query.assert_called_once()

    @patch("modules.sanitation.services.get_db")
    async def test_get_sanitation_statistics(self, mock_get_db, sanitation_service):
        """Testa a obtenção de estatísticas de saneamento."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock das contagens
        mock_session.query.return_value.count.return_value = 10

        # Executa
        result = await sanitation_service.get_statistics()

        # Verificações
        assert "total_records" in result
        assert "pending_services" in result
        assert "completed_services" in result

    async def test_validate_sanitation_data_valid(
        self, sanitation_service, sample_sanitation_data
    ):
        """Testa validação de dados válidos."""
        # Executa
        is_valid = await sanitation_service.validate_record_data(sample_sanitation_data)

        # Verificações
        assert is_valid is True

    async def test_validate_sanitation_data_invalid(self, sanitation_service):
        """Testa validação de dados inválidos."""
        # Dados inválidos
        invalid_data = {
            "tipo_servico": "",  # vazio
            "data_servico": None,  # nulo
            "localizacao": "",  # vazio
        }

        # Executa
        is_valid = await sanitation_service.validate_record_data(invalid_data)

        # Verificações
        assert is_valid is False

    @patch("modules.sanitation.services.get_db")
    async def test_get_pending_services(self, mock_get_db, sanitation_service):
        """Testa a busca por serviços pendentes."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock dos registros pendentes
        mock_records = [MagicMock() for _ in range(2)]
        mock_records[0].status = "PENDENTE"
        mock_records[1].status = "PENDENTE"
        mock_session.query.return_value.filter.return_value.all.return_value = (
            mock_records
        )

        # Executa
        result = await sanitation_service.get_pending_services()

        # Verificações
        assert len(result) == 2
        for record in result:
            assert record.status == "PENDENTE"

    @patch("modules.sanitation.services.get_db")
    async def test_complete_service(self, mock_get_db, sanitation_service):
        """Testa a conclusão de um serviço."""
        # Configura mock
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Mock do registro
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.status = "PENDENTE"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_record
        )

        # Executa
        result = await sanitation_service.complete_service(1)

        # Verificações
        assert result is True
        assert mock_record.status == "CONCLUIDO"
        mock_session.commit.assert_called_once()
