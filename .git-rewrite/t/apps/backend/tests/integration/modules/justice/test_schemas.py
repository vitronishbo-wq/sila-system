"""Testes de integração para os schemas do módulo justice."""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from modules.justice.models.case import CasePriority, CaseStatus, CaseType
from modules.justice.schemas import (
    CaseEventCreate,
    CaseStatistics,
    CourtHearingCreate,
    LegalCaseCreate,
    LegalCaseResponse,
    LegalCaseUpdate,
    LegalDocumentCreate,
    LegalDocumentResponse,
)


@pytest.fixture
def sample_case_data():
    """Dados válidos para teste de schemas jurídicos."""
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


@pytest.fixture
def sample_document_data():
    """Dados válidos para teste de schemas de documentos."""
    return {
        "tipo_documento": "PETICAO_INICIAL",
        "numero_documento": "DOC-2025-001",
        "titulo": "Petição Inicial - Cobrança",
        "conteudo": "Exmo. Sr. Dr. Juiz de Direito...",
        "caso_id": str(uuid4()),
        "advogado_id": str(uuid4()),
        "data_documento": datetime.now(timezone.utc),
    }


class TestLegalCaseSchemas:
    """Testes para schemas de casos jurídicos."""

    def test_legal_case_create_valid(self, sample_case_data):
        """Testa criação de schema com dados válidos."""
        schema = LegalCaseCreate(**sample_case_data)

        assert schema.numero_processo == sample_case_data["numero_processo"]
        assert schema.tipo_caso == sample_case_data["tipo_caso"]
        assert schema.status == sample_case_data["status"]
        assert schema.cliente_id == sample_case_data["cliente_id"]

    def test_legal_case_create_invalid_process_number(self, sample_case_data):
        """Testa validação com número de processo inválido."""
        sample_case_data["numero_processo"] = ""

        with pytest.raises(ValidationError) as exc_info:
            LegalCaseCreate(**sample_case_data)

        assert "numero_processo" in str(exc_info.value)

    def test_legal_case_create_invalid_tipo_caso(self, sample_case_data):
        """Testa validação com tipo de caso inválido."""
        sample_case_data["tipo_caso"] = "TIPO_INVALIDO"

        with pytest.raises(ValidationError) as exc_info:
            LegalCaseCreate(**sample_case_data)

        assert "tipo_caso" in str(exc_info.value)

    def test_legal_case_create_invalid_status(self, sample_case_data):
        """Testa validação com status inválido."""
        sample_case_data["status"] = "STATUS_INVALIDO"

        with pytest.raises(ValidationError) as exc_info:
            LegalCaseCreate(**sample_case_data)

        assert "status" in str(exc_info.value)

    def test_legal_case_create_invalid_cliente_id(self, sample_case_data):
        """Testa validação com cliente_id inválido."""
        sample_case_data["cliente_id"] = "uuid-invalido"

        with pytest.raises(ValidationError) as exc_info:
            LegalCaseCreate(**sample_case_data)

        assert "cliente_id" in str(exc_info.value)

    def test_legal_case_response_valid(self, sample_case_data):
        """Testa schema de resposta com dados válidos."""
        response_data = {
            "id": 1,
            **sample_case_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = LegalCaseResponse(**response_data)

        assert schema.id == 1
        assert schema.numero_processo == sample_case_data["numero_processo"]
        assert schema.criado_em is not None
        assert schema.atualizado_em is not None

    def test_legal_case_update_valid(self):
        """Testa schema de atualização com dados válidos."""
        update_data = {
            "status": CaseStatus.IN_PROGRESS,
            "prioridade": CasePriority.HIGH,
            "observacoes": "Caso em andamento com prioridade alta",
        }

        schema = LegalCaseUpdate(**update_data)

        assert schema.status == CaseStatus.IN_PROGRESS
        assert schema.prioridade == CasePriority.HIGH

    def test_legal_case_update_partial(self):
        """Testa schema de atualização com dados parciais."""
        update_data = {"status": CaseStatus.SUSPENDED}

        schema = LegalCaseUpdate(**update_data)

        assert schema.status == CaseStatus.SUSPENDED
        assert schema.prioridade is None
        assert schema.observacoes is None

    def test_legal_case_update_invalid_status(self):
        """Testa validação de status inválido na atualização."""
        update_data = {"status": "STATUS_INVALIDO"}

        with pytest.raises(ValidationError) as exc_info:
            LegalCaseUpdate(**update_data)

        assert "status" in str(exc_info.value)


class TestLegalDocumentSchemas:
    """Testes para schemas de documentos jurídicos."""

    def test_legal_document_create_valid(self, sample_document_data):
        """Testa criação de schema de documento com dados válidos."""
        schema = LegalDocumentCreate(**sample_document_data)

        assert schema.tipo_documento == sample_document_data["tipo_documento"]
        assert schema.numero_documento == sample_document_data["numero_documento"]
        assert schema.caso_id == sample_document_data["caso_id"]

    def test_legal_document_create_invalid_tipo_documento(self, sample_document_data):
        """Testa validação com tipo de documento inválido."""
        sample_document_data["tipo_documento"] = ""

        with pytest.raises(ValidationError) as exc_info:
            LegalDocumentCreate(**sample_document_data)

        assert "tipo_documento" in str(exc_info.value)

    def test_legal_document_create_invalid_conteudo(self, sample_document_data):
        """Testa validação com conteúdo vazio."""
        sample_document_data["conteudo"] = ""

        with pytest.raises(ValidationError) as exc_info:
            LegalDocumentCreate(**sample_document_data)

        assert "conteudo" in str(exc_info.value)

    def test_legal_document_response_valid(self, sample_document_data):
        """Testa schema de resposta de documento com dados válidos."""
        response_data = {
            "id": 1,
            **sample_document_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = LegalDocumentResponse(**response_data)

        assert schema.id == 1
        assert schema.tipo_documento == sample_document_data["tipo_documento"]
        assert schema.criado_em is not None


class TestCourtHearingSchemas:
    """Testes para schemas de audiências judiciais."""

    def test_court_hearing_create_valid(self):
        """Testa criação de schema de audiência com dados válidos."""
        hearing_data = {
            "caso_id": str(uuid4()),
            "tipo_audiencia": "INSTRUCAO",
            "data_audiencia": datetime.now(timezone.utc),
            "local": "Fórum Central - Sala 101",
            "juiz": "Dr. João da Silva",
            "observacoes": "Audiência de instrução e julgamento",
        }

        schema = CourtHearingCreate(**hearing_data)

        assert schema.tipo_audiencia == "INSTRUCAO"
        assert schema.local == hearing_data["local"]
        assert schema.juiz == hearing_data["juiz"]

    def test_court_hearing_create_invalid_data_passada(self):
        """Testa validação com data no passado."""
        hearing_data = {
            "caso_id": str(uuid4()),
            "tipo_audiencia": "INSTRUCAO",
            "data_audiencia": datetime(
                2020, 1, 1, tzinfo=timezone.utc
            ),  # data no passado
            "local": "Fórum Central - Sala 101",
            "juiz": "Dr. João da Silva",
        }

        with pytest.raises(ValidationError) as exc_info:
            CourtHearingCreate(**hearing_data)

        assert "data_audiencia" in str(exc_info.value)


class TestCaseEventSchemas:
    """Testes para schemas de eventos de casos."""

    def test_case_event_create_valid(self):
        """Testa criação de schema de evento com dados válidos."""
        event_data = {
            "tipo_evento": "AUDIENCIA_MARCADA",
            "descricao": "Audiência marcada para dia 15/12/2025",
            "data_evento": datetime.now(timezone.utc),
        }

        schema = CaseEventCreate(**event_data)

        assert schema.tipo_evento == "AUDIENCIA_MARCADA"
        assert schema.descricao == event_data["descricao"]

    def test_case_event_create_invalid_tipo_evento(self):
        """Testa validação com tipo de evento inválido."""
        event_data = {
            "tipo_evento": "",  # vazio
            "descricao": "Descrição do evento",
            "data_evento": datetime.now(timezone.utc),
        }

        with pytest.raises(ValidationError) as exc_info:
            CaseEventCreate(**event_data)

        assert "tipo_evento" in str(exc_info.value)


class TestCaseStatistics:
    """Testes para schema de estatísticas de casos."""

    def test_case_statistics_valid(self):
        """Testa schema de estatísticas com dados válidos."""
        stats_data = {
            "total_cases": 100,
            "cases_by_status": {"REGISTERED": 20, "IN_PROGRESS": 50, "CONCLUDED": 30},
            "cases_by_type": {"CIVIL": 40, "CRIMINAL": 35, "FAMILY": 25},
            "cases_by_priority": {"LOW": 30, "MEDIUM": 50, "HIGH": 20},
            "average_resolution_time": 45.5,
            "success_rate": 0.75,
        }

        schema = CaseStatistics(**stats_data)

        assert schema.total_cases == 100
        assert len(schema.cases_by_status) == 3
        assert schema.success_rate == 0.75

    def test_case_statistics_invalid_negative_values(self):
        """Testa validação com valores negativos."""
        stats_data = {
            "total_cases": -10,  # inválido
            "cases_by_status": {"REGISTERED": 20},
            "cases_by_type": {"CIVIL": 40},
            "cases_by_priority": {"LOW": 30},
        }

        with pytest.raises(ValidationError) as exc_info:
            CaseStatistics(**stats_data)

        assert "total_cases" in str(exc_info.value)

    def test_case_statistics_invalid_success_rate(self):
        """Testa validação com taxa de sucesso inválida."""
        stats_data = {
            "total_cases": 100,
            "cases_by_status": {"REGISTERED": 20},
            "cases_by_type": {"CIVIL": 40},
            "cases_by_priority": {"LOW": 30},
            "success_rate": 1.5,  # inválido (> 1.0)
        }

        with pytest.raises(ValidationError) as exc_info:
            CaseStatistics(**stats_data)

        assert "success_rate" in str(exc_info.value)

    def test_case_statistics_partial_data(self):
        """Testa schema com dados parciais (campos opcionais)."""
        stats_data = {
            "total_cases": 100,
            "cases_by_status": {"REGISTERED": 20},
            "cases_by_type": {"CIVIL": 40},
            "cases_by_priority": {"LOW": 30},
        }

        schema = CaseStatistics(**stats_data)

        assert schema.total_cases == 100
        assert schema.average_resolution_time is None
        assert schema.success_rate is None


class TestSchemaSerialization:
    """Testes de serialização e desserialização dos schemas."""

    def test_legal_case_json_serialization(self, sample_case_data):
        """Testa serialização JSON do schema de caso jurídico."""
        schema = LegalCaseCreate(**sample_case_data)
        json_data = schema.model_dump_json()

        assert "numero_processo" in json_data
        assert "2025.0001234-5" in json_data

    def test_legal_case_dict_serialization(self, sample_case_data):
        """Testa serialização em dicionário do schema de caso jurídico."""
        schema = LegalCaseCreate(**sample_case_data)
        dict_data = schema.model_dump()

        assert dict_data["numero_processo"] == sample_case_data["numero_processo"]
        assert dict_data["tipo_caso"] == sample_case_data["tipo_caso"]

    def test_legal_document_json_serialization(self, sample_document_data):
        """Testa serialização JSON do schema de documento."""
        schema = LegalDocumentCreate(**sample_document_data)
        json_data = schema.model_dump_json()

        assert "tipo_documento" in json_data
        assert "PETICAO_INICIAL" in json_data

    def test_schema_exclusion_fields(self, sample_case_data):
        """Testa exclusão de campos na serialização."""
        response_data = {
            "id": 1,
            **sample_case_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = LegalCaseResponse(**response_data)

        # Serializa excluindo campos sensíveis
        dict_data = schema.model_dump(exclude={"cliente_id", "advogado_id"})

        assert "cliente_id" not in dict_data
        assert "advogado_id" not in dict_data
        assert "numero_processo" in dict_data

    def test_schema_enum_serialization(self, sample_case_data):
        """Testa serialização de campos enum."""
        schema = LegalCaseCreate(**sample_case_data)
        dict_data = schema.model_dump()

        # Enums devem ser serializados como seus valores
        assert dict_data["tipo_caso"] == "CIVIL"
        assert dict_data["status"] == "REGISTERED"
        assert dict_data["prioridade"] == "MEDIUM"
