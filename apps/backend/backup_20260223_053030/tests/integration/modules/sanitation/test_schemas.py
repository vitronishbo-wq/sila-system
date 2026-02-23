"""Testes de integração para os schemas do módulo sanitation."""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from modules.sanitation.schemas import (
    SanitationRecordCreate,
    SanitationRecordResponse,
    SanitationRecordUpdate,
    SanitationStatistics,
    WaterTreatmentCreate,
    WaterTreatmentResponse,
)


@pytest.fixture
def sample_sanitation_data():
    """Dados válidos para teste de schemas de saneamento."""
    return {
        "tipo_servico": "Coleta de Lixo",
        "data_servico": datetime.now(timezone.utc),
        "localizacao": "Rua dos Testes, 123",
        "status": "PENDENTE",
        "observacoes": "Coleta programada",
        "cidadao_id": str(uuid4()),
    }


@pytest.fixture
def sample_water_treatment_data():
    """Dados válidos para teste de schemas de tratamento de água."""
    return {
        "tipo_tratamento": "Cloração",
        "data_tratamento": datetime.now(timezone.utc),
        "volume_tratado": 1000.0,
        "localizacao": "Estação de Tratamento Central",
        "responsavel_id": str(uuid4()),
    }


class TestSanitationRecordSchemas:
    """Testes para schemas de registros de saneamento."""

    def test_sanitation_record_create_valid(self, sample_sanitation_data):
        """Testa criação de schema com dados válidos."""
        schema = SanitationRecordCreate(**sample_sanitation_data)

        assert schema.tipo_servico == sample_sanitation_data["tipo_servico"]
        assert schema.localizacao == sample_sanitation_data["localizacao"]
        assert schema.status == sample_sanitation_data["status"]
        assert schema.cidadao_id == sample_sanitation_data["cidadao_id"]

    def test_sanitation_record_create_invalid_empty_tipo_servico(
        self, sample_sanitation_data
    ):
        """Testa validação com tipo_servico vazio."""
        sample_sanitation_data["tipo_servico"] = ""

        with pytest.raises(ValidationError) as exc_info:
            SanitationRecordCreate(**sample_sanitation_data)

        assert "tipo_servico" in str(exc_info.value)

    def test_sanitation_record_create_invalid_localizacao(self, sample_sanitation_data):
        """Testa validação com localização muito curta."""
        sample_sanitation_data["localizacao"] = "A"

        with pytest.raises(ValidationError) as exc_info:
            SanitationRecordCreate(**sample_sanitation_data)

        assert "localizacao" in str(exc_info.value)

    def test_sanitation_record_create_invalid_status(self, sample_sanitation_data):
        """Testa validação com status inválido."""
        sample_sanitation_data["status"] = "STATUS_INVALIDO"

        with pytest.raises(ValidationError) as exc_info:
            SanitationRecordCreate(**sample_sanitation_data)

        assert "status" in str(exc_info.value)

    def test_sanitation_record_create_invalid_cidadao_id(self, sample_sanitation_data):
        """Testa validação com cidadao_id inválido."""
        sample_sanitation_data["cidadao_id"] = "uuid-invalido"

        with pytest.raises(ValidationError) as exc_info:
            SanitationRecordCreate(**sample_sanitation_data)

        assert "cidadao_id" in str(exc_info.value)

    def test_sanitation_record_response_valid(self, sample_sanitation_data):
        """Testa schema de resposta com dados válidos."""
        response_data = {
            "id": 1,
            **sample_sanitation_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = SanitationRecordResponse(**response_data)

        assert schema.id == 1
        assert schema.tipo_servico == sample_sanitation_data["tipo_servico"]
        assert schema.criado_em is not None
        assert schema.atualizado_em is not None

    def test_sanitation_record_update_valid(self):
        """Testa schema de atualização com dados válidos."""
        update_data = {
            "status": "CONCLUIDO",
            "observacoes": "Serviço concluído com sucesso",
        }

        schema = SanitationRecordUpdate(**update_data)

        assert schema.status == "CONCLUIDO"
        assert schema.observacoes == "Serviço concluído com sucesso"

    def test_sanitation_record_update_partial(self):
        """Testa schema de atualização com dados parciais."""
        update_data = {"status": "EM_ANDAMENTO"}

        schema = SanitationRecordUpdate(**update_data)

        assert schema.status == "EM_ANDAMENTO"
        assert schema.observacoes is None

    def test_sanitation_record_update_invalid_status(self):
        """Testa validação de status inválido na atualização."""
        update_data = {"status": "STATUS_INVALIDO"}

        with pytest.raises(ValidationError) as exc_info:
            SanitationRecordUpdate(**update_data)

        assert "status" in str(exc_info.value)


class TestWaterTreatmentSchemas:
    """Testes para schemas de tratamento de água."""

    def test_water_treatment_create_valid(self, sample_water_treatment_data):
        """Testa criação de schema de tratamento com dados válidos."""
        schema = WaterTreatmentCreate(**sample_water_treatment_data)

        assert schema.tipo_tratamento == sample_water_treatment_data["tipo_tratamento"]
        assert schema.volume_tratado == sample_water_treatment_data["volume_tratado"]
        assert schema.localizacao == sample_water_treatment_data["localizacao"]

    def test_water_treatment_create_invalid_volume_negative(
        self, sample_water_treatment_data
    ):
        """Testa validação com volume negativo."""
        sample_water_treatment_data["volume_tratado"] = -100.0

        with pytest.raises(ValidationError) as exc_info:
            WaterTreatmentCreate(**sample_water_treatment_data)

        assert "volume_tratado" in str(exc_info.value)

    def test_water_treatment_create_invalid_tipo_tratamento(
        self, sample_water_treatment_data
    ):
        """Testa validação com tipo de tratamento inválido."""
        sample_water_treatment_data["tipo_tratamento"] = ""

        with pytest.raises(ValidationError) as exc_info:
            WaterTreatmentCreate(**sample_water_treatment_data)

        assert "tipo_tratamento" in str(exc_info.value)

    def test_water_treatment_response_valid(self, sample_water_treatment_data):
        """Testa schema de resposta de tratamento com dados válidos."""
        response_data = {
            "id": 1,
            **sample_water_treatment_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = WaterTreatmentResponse(**response_data)

        assert schema.id == 1
        assert schema.tipo_tratamento == sample_water_treatment_data["tipo_tratamento"]
        assert schema.criado_em is not None


class TestSanitationStatistics:
    """Testes para schema de estatísticas de saneamento."""

    def test_sanitation_statistics_valid(self):
        """Testa schema de estatísticas com dados válidos."""
        stats_data = {
            "total_records": 100,
            "pending_services": 25,
            "completed_services": 70,
            "cancelled_services": 5,
            "average_completion_time": 2.5,
            "services_by_type": {
                "Coleta de Lixo": 40,
                "Tratamento de Água": 30,
                "Limpeza Urbana": 30,
            },
        }

        schema = SanitationStatistics(**stats_data)

        assert schema.total_records == 100
        assert schema.pending_services == 25
        assert schema.completed_services == 70
        assert len(schema.services_by_type) == 3

    def test_sanitation_statistics_invalid_negative_values(self):
        """Testa validação com valores negativos."""
        stats_data = {
            "total_records": -10,  # inválido
            "pending_services": 25,
            "completed_services": 70,
            "cancelled_services": 5,
        }

        with pytest.raises(ValidationError) as exc_info:
            SanitationStatistics(**stats_data)

        assert "total_records" in str(exc_info.value)

    def test_sanitation_statistics_partial_data(self):
        """Testa schema com dados parciais (campos opcionais)."""
        stats_data = {
            "total_records": 100,
            "pending_services": 25,
            "completed_services": 70,
        }

        schema = SanitationStatistics(**stats_data)

        assert schema.total_records == 100
        assert schema.cancelled_services is None
        assert schema.average_completion_time is None


class TestSchemaSerialization:
    """Testes de serialização e desserialização dos schemas."""

    def test_sanitation_record_json_serialization(self, sample_sanitation_data):
        """Testa serialização JSON do schema de saneamento."""
        schema = SanitationRecordCreate(**sample_sanitation_data)
        json_data = schema.model_dump_json()

        assert "tipo_servico" in json_data
        assert "Coleta de Lixo" in json_data

    def test_sanitation_record_dict_serialization(self, sample_sanitation_data):
        """Testa serialização em dicionário do schema de saneamento."""
        schema = SanitationRecordCreate(**sample_sanitation_data)
        dict_data = schema.model_dump()

        assert dict_data["tipo_servico"] == sample_sanitation_data["tipo_servico"]
        assert dict_data["localizacao"] == sample_sanitation_data["localizacao"]

    def test_water_treatment_json_serialization(self, sample_water_treatment_data):
        """Testa serialização JSON do schema de tratamento de água."""
        schema = WaterTreatmentCreate(**sample_water_treatment_data)
        json_data = schema.model_dump_json()

        assert "tipo_tratamento" in json_data
        assert "Cloração" in json_data

    def test_schema_exclusion_fields(self, sample_sanitation_data):
        """Testa exclusão de campos na serialização."""
        response_data = {
            "id": 1,
            **sample_sanitation_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = SanitationRecordResponse(**response_data)

        # Serializa excluindo campos sensíveis
        dict_data = schema.model_dump(exclude={"cidadao_id"})

        assert "cidadao_id" not in dict_data
        assert "tipo_servico" in dict_data
