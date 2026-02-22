"""
Testes de unidade simplificados para o serviço de justiça.

Versão independente que testa a lógica de negócio diretamente
sem dependências externas como FastAPI.
"""

import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest

# Add backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import direto do arquivo de serviço
sys.path.insert(0, str(backend_dir / "modules" / "justice" / "services"))
from justice_service_simple import CasePriority, CaseStatus, CaseType, JusticeService


class TestJusticeServiceSimple:
    """Testes de unidade simplificados para JusticeService."""

    @pytest.fixture
    def service(self):
        """Instância do serviço para testes."""
        return JusticeService()

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

    # Testes de criação de casos
    @pytest.mark.asyncio
    async def test_create_legal_case_success(self, service, sample_case_data):
        """Testa criação bem-sucedida de caso jurídico."""
        # Act
        result = await service.create_case(sample_case_data)

        # Assert
        assert result is not None
        assert result["id"] == 1
        assert result["numero_processo"] == sample_case_data["numero_processo"]
        assert result["status"] == CaseStatus.REGISTERED

    @pytest.mark.asyncio
    async def test_create_legal_case_invalid_process_number(
        self, service, sample_case_data
    ):
        """Testa criação com número de processo inválido."""
        # Arrange
        sample_case_data["numero_processo"] = "123"  # formato inválido

        # Act & Assert
        with pytest.raises(ValueError, match="Dados do caso inválidos"):
            await service.create_case(sample_case_data)

    @pytest.mark.asyncio
    async def test_create_legal_case_invalid_value_range(
        self, service, sample_case_data
    ):
        """Testa criação com valor da causa fora do range permitido."""
        # Arrange
        sample_case_data["valor_causa"] = Decimal("1000000000.00")  # 1 bilhão

        # Act & Assert
        with pytest.raises(ValueError, match="Dados do caso inválidos"):
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
    async def test_update_case_status_valid_transition(self, service):
        """Testa transição válida de status."""
        # Act
        result = await service.update_case_status(1, CaseStatus.IN_PROGRESS)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_update_case_status_invalid_transition(self, service):
        """Testa transição inválida de status."""
        # Act
        result = await service.update_case_status(1, CaseStatus.REGISTERED)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_update_case_status_not_found(self, service):
        """Testa atualização de caso inexistente."""
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
    async def test_check_case_overdue_true(self, service):
        """Testa verificação de caso atrasado."""
        # Arrange
        past_date = datetime.now(timezone.utc) - timedelta(days=10)
        case_data = {"prazo_limite": past_date}

        # Act
        is_overdue = await service.check_case_overdue(case_data)

        # Assert
        assert is_overdue is True

    @pytest.mark.asyncio
    async def test_check_case_overdue_false(self, service):
        """Testa verificação de caso não atrasado."""
        # Arrange
        future_date = datetime.now(timezone.utc) + timedelta(days=10)
        case_data = {"prazo_limite": future_date}

        # Act
        is_overdue = await service.check_case_overdue(case_data)

        # Assert
        assert is_overdue is False

    # Testes de atribuição de advogado
    @pytest.mark.asyncio
    async def test_assign_lawyer_success(self, service):
        """Testa atribuição bem-sucedida de advogado."""
        # Arrange
        lawyer_id = str(uuid4())

        # Act
        result = await service.assign_lawyer_to_case(1, lawyer_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_assign_lawyer_case_not_found(self, service):
        """Testa atribuição para caso inexistente."""
        # Arrange
        lawyer_id = str(uuid4())

        # Act
        result = await service.assign_lawyer_to_case(999, lawyer_id)

        # Assert
        assert result is False

    # Testes de estatísticas
    @pytest.mark.asyncio
    async def test_get_case_statistics(self, service):
        """Testa obtenção de estatísticas."""
        # Act
        stats = await service.get_case_statistics()

        # Assert
        assert "total_cases" in stats
        assert "cases_by_status" in stats
        assert "cases_by_type" in stats
        assert stats["total_cases"] == 100

    # Testes de regras de negócio complexas
    @pytest.mark.asyncio
    async def test_can_appeal_case_true(self, service):
        """Testa se caso pode ser apelado."""
        # Arrange
        case_data = {
            "status": CaseStatus.CONCLUDED,
            "data_conclusao": datetime.now(timezone.utc) - timedelta(days=5),
        }

        # Act
        can_appeal = await service.can_appeal_case(case_data)

        # Assert
        assert can_appeal is True

    @pytest.mark.asyncio
    async def test_can_appeal_case_false_wrong_status(self, service):
        """Testa apelação com status incorreto."""
        # Arrange
        case_data = {
            "status": CaseStatus.IN_PROGRESS,
            "data_conclusao": datetime.now(timezone.utc) - timedelta(days=5),
        }

        # Act
        can_appeal = await service.can_appeal_case(case_data)

        # Assert
        assert can_appeal is False

    @pytest.mark.asyncio
    async def test_can_appeal_case_false_deadline_expired(self, service):
        """Testa apelação com prazo expirado."""
        # Arrange
        case_data = {
            "status": CaseStatus.CONCLUDED,
            "data_conclusao": datetime.now(timezone.utc)
            - timedelta(days=60),  # 60 dias atrás
        }

        # Act
        can_appeal = await service.can_appeal_case(case_data)

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
    async def test_generate_case_report(self, service):
        """Testa geração de relatório."""
        # Act
        report = await service.generate_case_report(
            start_date=datetime(2025, 10, 1, tzinfo=timezone.utc),
            end_date=datetime(2025, 10, 31, tzinfo=timezone.utc),
        )

        # Assert
        assert "total_cases" in report
        assert "cases_by_type" in report
        assert "success_rate" in report
        assert "period" in report
        assert report["total_cases"] == 3
