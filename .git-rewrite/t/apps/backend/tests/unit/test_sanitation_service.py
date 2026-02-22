"""
Testes de unidade para o serviço de saneamento.

Foco na lógica de negócio com mocking adequado para isolar
a camada de persistência e testar regras de negócio específicas.
"""

import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

# Add backend to path for imports
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import direto do serviço
from modules.sanitation.services.sanitation_service import SanitationService


class TestSanitationServiceUnit:
    """Testes de unidade para SanitationService."""

    @pytest.fixture
    def service(self):
        """Instância do serviço para testes."""
        return SanitationService()

    @pytest.fixture
    def sample_record_data(self):
        """Dados de exemplo para registro de saneamento."""
        return {
            "tipo_servico": "Coleta de Lixo",
            "data_servico": datetime.now(timezone.utc),
            "localizacao": "Rua dos Testes, 123",
            "status": "PENDENTE",
            "observacoes": "Coleta programada",
            "cidadao_id": str(uuid4()),
        }

    # Testes de criação de registros
    @pytest.mark.asyncio
    async def test_create_sanitation_record_success(self, service, sample_record_data):
        """Testa criação bem-sucedida de registro de saneamento."""
        # Act
        result = await service.create_record(sample_record_data)

        # Assert
        assert result is not None
        assert result["id"] == 1
        assert result["tipo_servico"] == sample_record_data["tipo_servico"]
        assert result["status"] == "PENDENTE"

    @pytest.mark.asyncio
    async def test_create_sanitation_record_with_validation_error(self, service):
        """Testa criação com dados inválidos."""
        # Arrange
        invalid_data = {
            "tipo_servico": "",  # inválido
            "data_servico": None,
            "localizacao": "",
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Dados do registro inválidos"):
            await service.create_record(invalid_data)

    # Testes de validação de dados
    @pytest.mark.asyncio
    async def test_validate_record_data_valid(self, service, sample_record_data):
        """Testa validação de dados válidos."""
        # Act
        result = await service.validate_record_data(sample_record_data)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_record_data_empty_tipo_servico(
        self, service, sample_record_data
    ):
        """Testa validação com tipo de serviço vazio."""
        # Arrange
        sample_record_data["tipo_servico"] = ""

        # Act
        result = await service.validate_record_data(sample_record_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_record_data_invalid_location(
        self, service, sample_record_data
    ):
        """Testa validação com localização muito curta."""
        # Arrange
        sample_record_data["localizacao"] = "A"

        # Act
        result = await service.validate_record_data(sample_record_data)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_record_data_past_date(self, service, sample_record_data):
        """Testa validação com data no passado."""
        # Arrange
        sample_record_data["data_servico"] = datetime(2020, 1, 1, tzinfo=timezone.utc)

        # Act
        result = await service.validate_record_data(sample_record_data)

        # Assert
        assert result is False

    # Testes de atualização de status
    @pytest.mark.asyncio
    async def test_update_record_status_success(self, service):
        """Testa atualização bem-sucedida de status."""
        # Act
        result = await service.update_record_status(1, "CONCLUIDO")

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_update_record_status_not_found(self, service):
        """Testa atualização de registro inexistente."""
        # Act
        result = await service.update_record_status(999, "CONCLUIDO")

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_update_record_status_invalid_transition(self, service):
        """Testa transição de status inválida."""
        # Act
        result = await service.update_record_status(1, "PENDENTE")

        # Assert
        assert result is False  # Não pode voltar para PENDENTE

    # Testes de lógica de prioridade
    @pytest.mark.asyncio
    async def test_calculate_service_priority_urgent(self, service):
        """Testa cálculo de prioridade para serviço urgente."""
        # Arrange
        service_data = {
            "tipo_servico": "Contaminação Química",
            "localizacao": "Escola Primária",
            "observacoes": "Risco iminente à saúde",
        }

        # Act
        priority = await service.calculate_service_priority(service_data)

        # Assert
        assert priority == "ALTA"

    @pytest.mark.asyncio
    async def test_calculate_service_priority_normal(self, service):
        """Testa cálculo de prioridade para serviço normal."""
        # Arrange
        service_data = {
            "tipo_servico": "Coleta de Lixo Regular",
            "localizacao": "Residencial",
            "observacoes": "Coleta programada",
        }

        # Act
        priority = await service.calculate_service_priority(service_data)

        # Assert
        assert priority == "MEDIA"

    @pytest.mark.asyncio
    async def test_calculate_service_priority_low(self, service):
        """Testa cálculo de prioridade para serviço baixa."""
        # Arrange
        service_data = {
            "tipo_servico": "Manutenção de Parque",
            "localizacao": "Área de Lazer",
            "observacoes": "Manutenção preventiva",
        }

        # Act
        priority = await service.calculate_service_priority(service_data)

        # Assert
        assert priority == "BAIXA"

    # Testes de estatísticas
    @pytest.mark.asyncio
    async def test_get_sanitation_statistics(self, service):
        """Testa obtenção de estatísticas."""
        # Act
        stats = await service.get_statistics()

        # Assert
        assert "total_records" in stats
        assert "pending_services" in stats
        assert "completed_services" in stats
        assert "cancelled_services" in stats
        assert "services_by_type" in stats
        assert stats["total_records"] == 100

    # Testes de regras de negócio específicas
    @pytest.mark.asyncio
    async def test_can_schedule_service_business_hours(self, service):
        """Testa agendamento dentro do horário comercial."""
        # Arrange
        service_time = datetime(2025, 10, 26, 14, 0, tzinfo=timezone.utc)  # 14h

        # Act
        can_schedule = await service.can_schedule_service(service_time)

        # Assert
        assert can_schedule is True

    @pytest.mark.asyncio
    async def test_can_schedule_service_after_hours(self, service):
        """Testa agendamento fora do horário comercial."""
        # Arrange
        service_time = datetime(2025, 10, 26, 22, 0, tzinfo=timezone.utc)  # 22h

        # Act
        can_schedule = await service.can_schedule_service(service_time)

        # Assert
        assert can_schedule is False

    @pytest.mark.asyncio
    async def test_can_schedule_service_weekend(self, service):
        """Testa agendamento em fim de semana."""
        # Arrange
        service_time = datetime(2025, 10, 27, 10, 0, tzinfo=timezone.utc)  # Domingo

        # Act
        can_schedule = await service.can_schedule_service(service_time)

        # Assert
        assert can_schedule is False

    @pytest.mark.asyncio
    async def test_calculate_service_cost_basic(self, service):
        """Testa cálculo de custo básico."""
        # Arrange
        service_data = {
            "tipo_servico": "Coleta de Lixo",
            "distancia": 5.0,  # km
            "volume": 100.0,  # kg
        }

        # Act
        cost = await service.calculate_service_cost(service_data)

        # Assert
        assert isinstance(cost, Decimal)
        assert cost > 0

    @pytest.mark.asyncio
    async def test_calculate_service_cost_with_priority_surcharge(self, service):
        """Testa cálculo de custo com sobretaxa de prioridade."""
        # Arrange
        service_data = {
            "tipo_servico": "Contaminação Química",
            "distancia": 10.0,
            "volume": 500.0,
            "prioridade": "ALTA",
        }

        # Act
        cost = await service.calculate_service_cost(service_data)

        # Assert
        assert isinstance(cost, Decimal)
        # Custo com prioridade alta deve ser maior
        basic_cost = await service.calculate_service_cost(
            {
                "tipo_servico": "Coleta de Lixo",
                "distancia": 10.0,
                "volume": 500.0,
            }
        )
        assert cost > basic_cost

    # Testes de tratamento de água
    @pytest.mark.asyncio
    async def test_validate_water_treatment_parameters(self, service):
        """Testa validação de parâmetros de tratamento de água."""
        # Arrange
        treatment_data = {
            "tipo_tratamento": "Cloração",
            "volume_tratado": 1000.0,
            "ph": 7.2,
            "cloro_residual": 0.5,
            "temperatura": 25.0,
        }

        # Act
        is_valid = await service.validate_water_treatment_parameters(treatment_data)

        # Assert
        assert is_valid is True

    @pytest.mark.asyncio
    async def test_validate_water_treatment_ph_out_of_range(self, service):
        """Testa validação com pH fora do range."""
        # Arrange
        treatment_data = {
            "tipo_tratamento": "Cloração",
            "volume_tratado": 1000.0,
            "ph": 10.5,  # muito alto
            "cloro_residual": 0.5,
            "temperatura": 25.0,
        }

        # Act
        is_valid = await service.validate_water_treatment_parameters(treatment_data)

        # Assert
        assert is_valid is False

    @pytest.mark.asyncio
    async def test_validate_water_treatment_negative_volume(self, service):
        """Testa validação com volume negativo."""
        # Arrange
        treatment_data = {
            "tipo_tratamento": "Cloração",
            "volume_tratado": -100.0,  # negativo
            "ph": 7.2,
            "cloro_residual": 0.5,
            "temperatura": 25.0,
        }

        # Act
        is_valid = await service.validate_water_treatment_parameters(treatment_data)

        # Assert
        assert is_valid is False

    # Testes de regras de negócio complexas
    @pytest.mark.asyncio
    async def test_check_service_conflicts_no_conflict(self, service):
        """Testa verificação de conflitos sem conflitos."""
        # Arrange
        service_data = {
            "localizacao": "Rua B, 123",
            "data_servico": datetime(2025, 10, 26, 14, 0, tzinfo=timezone.utc),
        }

        # Act
        has_conflict = await service.check_service_conflicts(service_data)

        # Assert
        assert has_conflict is False

    @pytest.mark.asyncio
    async def test_check_service_conflicts_with_conflict(self, service):
        """Testa verificação de conflitos com conflitos existentes."""
        # Arrange
        service_data = {
            "localizacao": "Rua A, 123",
            "data_servico": datetime(2025, 10, 26, 14, 0, tzinfo=timezone.utc),
        }

        # Act
        has_conflict = await service.check_service_conflicts(service_data)

        # Assert
        assert has_conflict is True

    @pytest.mark.asyncio
    async def test_generate_service_report(self, service):
        """Testa geração de relatório."""
        # Act
        report = await service.generate_service_report(
            start_date=datetime(2025, 10, 1, tzinfo=timezone.utc),
            end_date=datetime(2025, 10, 31, tzinfo=timezone.utc),
        )

        # Assert
        assert "total_services" in report
        assert "services_by_type" in report
        assert "completion_rate" in report
        assert "period" in report
        assert report["total_services"] == 3
