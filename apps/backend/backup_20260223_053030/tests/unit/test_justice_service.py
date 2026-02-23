"""
Testes de unidade para o serviço de justiça.

Foco na lógica de negócio jurídica com mocking adequado para isolar
a camada de persistência e testar regras de negócio específicas.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.justice.models.case import Case, CasePriority, CaseStatus, CaseType
from modules.justice.schemas import (
    CaseStatistics,
    CourtHearingCreate,
    LegalCaseCreate,
    LegalCaseUpdate,
)
from modules.justice.services.justice_service import JusticeService


class TestJusticeServiceUnit:
    """Testes de unidade para JusticeService."""

    @pytest.fixture
    def service(self):
        """Instância do serviço para testes."""
        return JusticeService()

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
    def sample_case_data(self):
        """Dados de exemplo para caso jurídico."""
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
            "valor_causa": Decimal("50000.00"),
        }

    @pytest.fixture
    def mock_case(self):
        """Mock de caso jurídico."""
        case = MagicMock()
        case.id = 1
        case.numero_processo = "2025.0001234-5"
        case.tipo_caso = CaseType.CIVIL
        case.status = CaseStatus.REGISTERED
        case.prioridade = CasePriority.MEDIUM
        case.data_abertura = datetime.now(timezone.utc)
        case.valor_causa = Decimal("50000.00")
        case.advogado_id = str(uuid4())
        return case

    # Testes de criação de casos
    @pytest.mark.asyncio
    async def test_create_legal_case_success(self, service, mock_db, sample_case_data):
        """Testa criação bem-sucedida de caso jurídico."""
        # Arrange
        mock_case = MagicMock()
        mock_case.id = 1
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()

        # Act
        result = await service.create_case(sample_case_data)

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert result is not None

    @pytest.mark.asyncio
    async def test_create_legal_case_duplicate_process_number(
        self, service, mock_db, sample_case_data
    ):
        """Testa criação com número de processo duplicado."""
        # Arrange
        existing_case = MagicMock()
        existing_case.numero_processo = sample_case_data["numero_processo"]
        mock_db.query.return_value.filter.return_value.first.return_value = (
            existing_case
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Número de processo já existe"):
            await service.create_case(sample_case_data)

    @pytest.mark.asyncio
    async def test_create_legal_case_invalid_value_range(
        self, service, mock_db, sample_case_data
    ):
        """Testa criação com valor da causa fora do range permitido."""
        # Arrange
        sample_case_data["valor_causa"] = Decimal("1000000000.00")  # 1 bilhão

        # Act & Assert
        with pytest.raises(ValueError, match="Valor da causa excede limite máximo"):
            await service.create_case(sample_case_data)

    # Testes de validação de dados
    @pytest.mark.asyncio
    async def test_validate_case_data_valid(self, service, sample_case_data):
        """Testa validação de dados válidos."""
        # Act
        result = await service.validate_case_data(sample_case_data)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_case_data_invalid_process_number(
        self, service, sample_case_data
    ):
        """Testa validação com número de processo inválido."""
        # Arrange
        sample_case_data["numero_processo"] = "123"  # formato inválido

        # Act
        result = await service.validate_case_data(sample_case_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_case_data_future_opening_date(
        self, service, sample_case_data
    ):
        """Testa validação com data de abertura no futuro."""
        # Arrange
        sample_case_data["data_abertura"] = datetime.now(timezone.utc) + timedelta(
            days=30
        )

        # Act
        result = await service.validate_case_data(sample_case_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_case_data_negative_value(self, service, sample_case_data):
        """Testa validação com valor negativo."""
        # Arrange
        sample_case_data["valor_causa"] = Decimal("-1000.00")

        # Act
        result = await service.validate_case_data(sample_case_data)

        # Assert
        assert result is False

    # Testes de transição de status
    @pytest.mark.asyncio
    async def test_update_case_status_valid_transition(
        self, service, mock_db, mock_case
    ):
        """Testa transição válida de status."""
        # Arrange
        mock_case.status = CaseStatus.REGISTERED
        mock_db.query.return_value.filter.return_value.first.return_value = mock_case
        new_status = CaseStatus.IN_PROGRESS

        # Act
        result = await service.update_case_status(1, new_status)

        # Assert
        assert result is True
        assert mock_case.status == new_status
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_case_status_invalid_transition(
        self, service, mock_db, mock_case
    ):
        """Testa transição inválida de status."""
        # Arrange
        mock_case.status = CaseStatus.ARCHIVED
        mock_db.query.return_value.filter.return_value.first.return_value = mock_case
        new_status = CaseStatus.REGISTERED  # Não pode voltar

        # Act
        result = await service.update_case_status(1, new_status)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_update_case_status_not_found(self, service, mock_db):
        """Testa atualização de caso inexistente."""
        # Arrange
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = await service.update_case_status(999, CaseStatus.IN_PROGRESS)

        # Assert
        assert result is False

    # Testes de cálculo de custas
    @pytest.mark.asyncio
    async def test_calculate_court_fees_civil_case(self, service):
        """Testa cálculo de custas para caso cível."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.CIVIL,
            "valor_causa": Decimal("50000.00"),
        }

        # Act
        fees = await service.calculate_court_fees(case_data)

        # Assert
        assert isinstance(fees, Decimal)
        assert fees > 0
        # Para casos cíveis, geralmente 1% do valor da causa
        expected_min = Decimal("500.00")  # 1% de 50000
        assert fees >= expected_min

    @pytest.mark.asyncio
    async def test_calculate_court_fees_family_case(self, service):
        """Testa cálculo de custas para caso familiar."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.FAMILY,
            "valor_causa": Decimal("10000.00"),
        }

        # Act
        fees = await service.calculate_court_fees(case_data)

        # Assert
        assert isinstance(fees, Decimal)
        # Casos familiares geralmente têm custas reduzidas
        civil_fees = await service.calculate_court_fees(
            {
                "tipo_caso": CaseType.CIVIL,
                "valor_causa": Decimal("10000.00"),
            }
        )
        assert fees < civil_fees

    @pytest.mark.asyncio
    async def test_calculate_court_fees_high_value_case(self, service):
        """Testa cálculo de custas para caso de alto valor."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.COMMERCIAL,
            "valor_causa": Decimal("1000000.00"),  # 1 milhão
        }

        # Act
        fees = await service.calculate_court_fees(case_data)

        # Assert
        assert isinstance(fees, Decimal)
        # Deve haver teto máximo para custas
        max_fees = Decimal("50000.00")  # exemplo de teto
        assert fees <= max_fees

    # Testes de prazos processuais
    @pytest.mark.asyncio
    async def test_calculate_deadline_civil_case(self, service):
        """Testa cálculo de prazo para caso cível."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.CIVIL,
            "data_abertura": datetime(2025, 1, 1, tzinfo=timezone.utc),
        }

        # Act
        deadline = await service.calculate_case_deadline(case_data)

        # Assert
        assert isinstance(deadline, datetime)
        # Prazo para contestação em casos cíveis geralmente 15 dias
        expected_deadline = datetime(2025, 1, 16, tzinfo=timezone.utc)
        assert deadline.date() == expected_deadline.date()

    @pytest.mark.asyncio
    async def test_calculate_deadline_criminal_case(self, service):
        """Testa cálculo de prazo para caso criminal."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.CRIMINAL,
            "data_abertura": datetime(2025, 1, 1, tzinfo=timezone.utc),
        }

        # Act
        deadline = await service.calculate_case_deadline(case_data)

        # Assert
        assert isinstance(deadline, datetime)
        # Prazos criminais geralmente mais curtos
        civil_deadline = await service.calculate_case_deadline(
            {
                "tipo_caso": CaseType.CIVIL,
                "data_abertura": datetime(2025, 1, 1, tzinfo=timezone.utc),
            }
        )
        assert deadline < civil_deadline

    @pytest.mark.asyncio
    async def test_check_case_overdue_true(self, service, mock_case):
        """Testa verificação de caso atrasado."""
        # Arrange
        past_date = datetime.now(timezone.utc) - timedelta(days=10)
        mock_case.prazo_limite = past_date

        # Act
        is_overdue = await service.check_case_overdue(mock_case)

        # Assert
        assert is_overdue is True

    @pytest.mark.asyncio
    async def test_check_case_overdue_false(self, service, mock_case):
        """Testa verificação de caso não atrasado."""
        # Arrange
        future_date = datetime.now(timezone.utc) + timedelta(days=10)
        mock_case.prazo_limite = future_date

        # Act
        is_overdue = await service.check_case_overdue(mock_case)

        # Assert
        assert is_overdue is False

    # Testes de atribuição de advogado
    @pytest.mark.asyncio
    async def test_assign_lawyer_success(self, service, mock_db, mock_case):
        """Testa atribuição bem-sucedida de advogado."""
        # Arrange
        lawyer_id = str(uuid4())
        mock_case.advogado_id = None
        mock_db.query.return_value.filter.return_value.first.return_value = mock_case

        # Act
        result = await service.assign_lawyer_to_case(1, lawyer_id)

        # Assert
        assert result is True
        assert mock_case.advogado_id == lawyer_id
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_assign_lawyer_already_assigned(self, service, mock_db, mock_case):
        """Testa atribuição quando já existe advogado."""
        # Arrange
        existing_lawyer = str(uuid4())
        mock_case.advogado_id = existing_lawyer
        mock_db.query.return_value.filter.return_value.first.return_value = mock_case
        new_lawyer = str(uuid4())

        # Act
        result = await service.assign_lawyer_to_case(1, new_lawyer)

        # Assert
        assert result is False  # Não deve permitir reatribuição
        assert mock_case.advogado_id == existing_lawyer

    # Testes de estatísticas
    @pytest.mark.asyncio
    async def test_get_case_statistics_empty(self, service, mock_db):
        """Testa obtenção de estatísticas com dados vazios."""
        # Arrange
        mock_db.query.return_value.count.return_value = 0

        # Act
        stats = await service.get_case_statistics()

        # Assert
        assert isinstance(stats, CaseStatistics)
        assert stats.total_cases == 0
        assert stats.cases_by_status == {}
        assert stats.cases_by_type == {}

    @pytest.mark.asyncio
    async def test_get_case_statistics_with_data(self, service, mock_db):
        """Testa obtenção de estatísticas com dados."""

        # Arrange
        def mock_count_side_effect():
            if hasattr(mock_count_side_effect, "call_count"):
                mock_count_side_effect.call_count += 1
            else:
                mock_count_side_effect.call_count = 1

            counts = [100, 30, 50, 20]  # total, registered, in_progress, concluded
            return counts[mock_count_side_effect.call_count - 1]

        mock_db.query.return_value.count.side_effect = mock_count_side_effect

        # Act
        stats = await service.get_case_statistics()

        # Assert
        assert stats.total_cases == 100
        assert stats.cases_by_status["REGISTERED"] == 30
        assert stats.cases_by_status["IN_PROGRESS"] == 50
        assert stats.cases_by_status["CONCLUDED"] == 20

    # Testes de regras de negócio complexas
    @pytest.mark.asyncio
    async def test_can_appeal_case_true(self, service, mock_case):
        """Testa se caso pode ser apelado."""
        # Arrange
        mock_case.status = CaseStatus.CONCLUDED
        mock_case.data_conclusao = datetime.now(timezone.utc) - timedelta(days=5)

        # Act
        can_appeal = await service.can_appeal_case(mock_case)

        # Assert
        assert can_appeal is True

    @pytest.mark.asyncio
    async def test_can_appeal_case_false_wrong_status(self, service, mock_case):
        """Testa apelação com status incorreto."""
        # Arrange
        mock_case.status = CaseStatus.IN_PROGRESS

        # Act
        can_appeal = await service.can_appeal_case(mock_case)

        # Assert
        assert can_appeal is False

    @pytest.mark.asyncio
    async def test_can_appeal_case_false_deadline_expired(self, service, mock_case):
        """Testa apelação com prazo expirado."""
        # Arrange
        mock_case.status = CaseStatus.CONCLUDED
        mock_case.data_conclusao = datetime.now(timezone.utc) - timedelta(
            days=60
        )  # 60 dias atrás

        # Act
        can_appeal = await service.can_appeal_case(mock_case)

        # Assert
        assert can_appeal is False

    @pytest.mark.asyncio
    async def test_calculate_case_complexity_simple(self, service):
        """Testa cálculo de complexidade para caso simples."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.CIVIL,
            "valor_causa": Decimal("10000.00"),
            "numero_partes": 2,
            "tem_testemunhas": False,
            "tem_pericias": False,
        }

        # Act
        complexity = await service.calculate_case_complexity(case_data)

        # Assert
        assert complexity == "SIMPLES"

    @pytest.mark.asyncio
    async def test_calculate_case_complexity_complex(self, service):
        """Testa cálculo de complexidade para caso complexo."""
        # Arrange
        case_data = {
            "tipo_caso": CaseType.COMMERCIAL,
            "valor_causa": Decimal("500000.00"),
            "numero_partes": 5,
            "tem_testemunhas": True,
            "tem_pericias": True,
        }

        # Act
        complexity = await service.calculate_case_complexity(case_data)

        # Assert
        assert complexity == "COMPLEXO"

    @pytest.mark.asyncio
    async def test_generate_case_report_empty(self, service, mock_db):
        """Testa geração de relatório com dados vazios."""
        # Arrange
        mock_db.query.return_value.all.return_value = []

        # Act
        report = await service.generate_case_report(
            start_date=datetime(2025, 10, 1, tzinfo=timezone.utc),
            end_date=datetime(2025, 10, 31, tzinfo=timezone.utc),
        )

        # Assert
        assert "total_cases" in report
        assert "cases_by_type" in report
        assert "success_rate" in report
        assert report["total_cases"] == 0

    @pytest.mark.asyncio
    async def test_generate_case_report_with_data(self, service, mock_db):
        """Testa geração de relatório com dados."""
        # Arrange
        mock_cases = [
            MagicMock(tipo_caso=CaseType.CIVIL, status=CaseStatus.CONCLUDED),
            MagicMock(tipo_caso=CaseType.CIVIL, status=CaseStatus.CONCLUDED),
            MagicMock(tipo_caso=CaseType.CRIMINAL, status=CaseStatus.IN_PROGRESS),
        ]
        mock_db.query.return_value.all.return_value = mock_cases

        # Act
        report = await service.generate_case_report(
            start_date=datetime(2025, 10, 1, tzinfo=timezone.utc),
            end_date=datetime(2025, 10, 31, tzinfo=timezone.utc),
        )

        # Assert
        assert report["total_cases"] == 3
        assert report["success_rate"] == 2 / 3  # 2 de 3 concluídos
        assert str(CaseType.CIVIL) in report["cases_by_type"]
