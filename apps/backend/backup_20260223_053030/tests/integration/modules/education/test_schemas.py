"""Testes de integração para os schemas do módulo education."""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from modules.education.schemas import (
    AdultLiteracyCreate,
    EducationStatistics,
    ScholarshipCreate,
    ScholarshipResponse,
    SchoolMealCreate,
    SchoolMealResponse,
    SchoolTransferCreate,
    StudentEnrollmentCreate,
    StudentEnrollmentResponse,
    StudentEnrollmentUpdate,
)


@pytest.fixture
def sample_enrollment_data():
    """Dados válidos para teste de schemas educacionais."""
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
    """Dados válidos para teste de schemas de bolsas."""
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


@pytest.fixture
def sample_meal_data():
    """Dados válidos para teste de schemas de refeições."""
    return {
        "data_refeicao": datetime.now(timezone.utc),
        "tipo_refeicao": "ALMOCO",
        "escola_id": str(uuid4()),
        "estudante_id": str(uuid4()),
        "nutricionista_responsavel": "Dr. Ana Nutricionista",
        "cardapio": "Arroz, feijão, carne, salada e fruta",
        "calorias": 650,
        "observacoes": "Refeição balanceada",
    }


class TestStudentEnrollmentSchemas:
    """Testes para schemas de matrículas estudantis."""

    def test_student_enrollment_create_valid(self, sample_enrollment_data):
        """Testa criação de schema com dados válidos."""
        schema = StudentEnrollmentCreate(**sample_enrollment_data)

        assert schema.numero_matricula == sample_enrollment_data["numero_matricula"]
        assert schema.nome_estudante == sample_enrollment_data["nome_estudante"]
        assert schema.escola_id == sample_enrollment_data["escola_id"]
        assert schema.turno == sample_enrollment_data["turno"]

    def test_student_enrollment_create_invalid_empty_numero(
        self, sample_enrollment_data
    ):
        """Testa validação com número de matrícula vazio."""
        sample_enrollment_data["numero_matricula"] = ""

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentCreate(**sample_enrollment_data)

        assert "numero_matricula" in str(exc_info.value)

    def test_student_enrollment_create_invalid_name(self, sample_enrollment_data):
        """Testa validação com nome muito curto."""
        sample_enrollment_data["nome_estudante"] = "A"

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentCreate(**sample_enrollment_data)

        assert "nome_estudante" in str(exc_info.value)

    def test_student_enrollment_create_invalid_birth_date(self, sample_enrollment_data):
        """Testa validação com data de nascimento no futuro."""
        sample_enrollment_data["data_nascimento"] = datetime(
            2030, 1, 1, tzinfo=timezone.utc
        )

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentCreate(**sample_enrollment_data)

        assert "data_nascimento" in str(exc_info.value)

    def test_student_enrollment_create_invalid_genero(self, sample_enrollment_data):
        """Testa validação com gênero inválido."""
        sample_enrollment_data["genero"] = "X"

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentCreate(**sample_enrollment_data)

        assert "genero" in str(exc_info.value)

    def test_student_enrollment_create_invalid_escola_id(self, sample_enrollment_data):
        """Testa validação com escola_id inválido."""
        sample_enrollment_data["escola_id"] = "uuid-invalido"

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentCreate(**sample_enrollment_data)

        assert "escola_id" in str(exc_info.value)

    def test_student_enrollment_response_valid(self, sample_enrollment_data):
        """Testa schema de resposta com dados válidos."""
        response_data = {
            "id": 1,
            **sample_enrollment_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = StudentEnrollmentResponse(**response_data)

        assert schema.id == 1
        assert schema.numero_matricula == sample_enrollment_data["numero_matricula"]
        assert schema.criado_em is not None
        assert schema.atualizado_em is not None

    def test_student_enrollment_update_valid(self):
        """Testa schema de atualização com dados válidos."""
        update_data = {
            "turma": "B",
            "turno": "TARDE",
            "observacoes": "Transferido de turma",
        }

        schema = StudentEnrollmentUpdate(**update_data)

        assert schema.turma == "B"
        assert schema.turno == "TARDE"

    def test_student_enrollment_update_partial(self):
        """Testa schema de atualização com dados parciais."""
        update_data = {"turma": "C"}

        schema = StudentEnrollmentUpdate(**update_data)

        assert schema.turma == "C"
        assert schema.turno is None
        assert schema.observacoes is None

    def test_student_enrollment_update_invalid_turno(self):
        """Testa validação de turno inválido na atualização."""
        update_data = {"turno": "TURNO_INVALIDO"}

        with pytest.raises(ValidationError) as exc_info:
            StudentEnrollmentUpdate(**update_data)

        assert "turno" in str(exc_info.value)


class TestScholarshipSchemas:
    """Testes para schemas de bolsas de estudos."""

    def test_scholarship_create_valid(self, sample_scholarship_data):
        """Testa criação de schema de bolsa com dados válidos."""
        schema = ScholarshipCreate(**sample_scholarship_data)

        assert schema.tipo_bolsa == sample_scholarship_data["tipo_bolsa"]
        assert (
            schema.percentual_desconto == sample_scholarship_data["percentual_desconto"]
        )
        assert schema.estudante_id == sample_scholarship_data["estudante_id"]

    def test_scholarship_create_invalid_percentual_negative(
        self, sample_scholarship_data
    ):
        """Testa validação com percentual negativo."""
        sample_scholarship_data["percentual_desconto"] = -10.0

        with pytest.raises(ValidationError) as exc_info:
            ScholarshipCreate(**sample_scholarship_data)

        assert "percentual_desconto" in str(exc_info.value)

    def test_scholarship_create_invalid_percentual_above_100(
        self, sample_scholarship_data
    ):
        """Testa validação com percentual acima de 100%."""
        sample_scholarship_data["percentual_desconto"] = 150.0

        with pytest.raises(ValidationError) as exc_info:
            ScholarshipCreate(**sample_scholarship_data)

        assert "percentual_desconto" in str(exc_info.value)

    def test_scholarship_create_invalid_tipo_bolsa(self, sample_scholarship_data):
        """Testa validação com tipo de bolsa inválido."""
        sample_scholarship_data["tipo_bolsa"] = ""

        with pytest.raises(ValidationError) as exc_info:
            ScholarshipCreate(**sample_scholarship_data)

        assert "tipo_bolsa" in str(exc_info.value)

    def test_scholarship_create_invalid_vigencia_dates(self, sample_scholarship_data):
        """Testa validação com data de fim anterior à data de início."""
        sample_scholarship_data["vigencia_inicio"] = datetime(
            2025, 6, 1, tzinfo=timezone.utc
        )
        sample_scholarship_data["vigencia_fim"] = datetime(
            2025, 1, 1, tzinfo=timezone.utc
        )

        with pytest.raises(ValidationError) as exc_info:
            ScholarshipCreate(**sample_scholarship_data)

        assert "vigencia_fim" in str(exc_info.value)

    def test_scholarship_response_valid(self, sample_scholarship_data):
        """Testa schema de resposta de bolsa com dados válidos."""
        response_data = {
            "id": 1,
            **sample_scholarship_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = ScholarshipResponse(**response_data)

        assert schema.id == 1
        assert schema.tipo_bolsa == sample_scholarship_data["tipo_bolsa"]
        assert schema.criado_em is not None


class TestSchoolMealSchemas:
    """Testes para schemas de refeições escolares."""

    def test_school_meal_create_valid(self, sample_meal_data):
        """Testa criação de schema de refeição com dados válidos."""
        schema = SchoolMealCreate(**sample_meal_data)

        assert schema.tipo_refeicao == sample_meal_data["tipo_refeicao"]
        assert schema.calorias == sample_meal_data["calorias"]
        assert schema.escola_id == sample_meal_data["escola_id"]

    def test_school_meal_create_invalid_calorias_negative(self, sample_meal_data):
        """Testa validação com calorias negativas."""
        sample_meal_data["calorias"] = -100

        with pytest.raises(ValidationError) as exc_info:
            SchoolMealCreate(**sample_meal_data)

        assert "calorias" in str(exc_info.value)

    def test_school_meal_create_invalid_tipo_refeicao(self, sample_meal_data):
        """Testa validação com tipo de refeição inválido."""
        sample_meal_data["tipo_refeicao"] = ""

        with pytest.raises(ValidationError) as exc_info:
            SchoolMealCreate(**sample_meal_data)

        assert "tipo_refeicao" in str(exc_info.value)

    def test_school_meal_create_empty_cardapio(self, sample_meal_data):
        """Testa validação com cardápio vazio."""
        sample_meal_data["cardapio"] = ""

        with pytest.raises(ValidationError) as exc_info:
            SchoolMealCreate(**sample_meal_data)

        assert "cardapio" in str(exc_info.value)

    def test_school_meal_response_valid(self, sample_meal_data):
        """Testa schema de resposta de refeição com dados válidos."""
        response_data = {
            "id": 1,
            **sample_meal_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = SchoolMealResponse(**response_data)

        assert schema.id == 1
        assert schema.tipo_refeicao == sample_meal_data["tipo_refeicao"]
        assert schema.criado_em is not None


class TestSchoolTransferSchemas:
    """Testes para schemas de transferências escolares."""

    def test_school_transfer_create_valid(self):
        """Testa criação de schema de transferência com dados válidos."""
        transfer_data = {
            "matricula_id": 1,
            "escola_origem_id": str(uuid4()),
            "escola_destino_id": str(uuid4()),
            "motivo_transferencia": "MUDANCA_DE_ENDERECO",
            "data_transferencia": datetime.now(timezone.utc),
            "status": "SOLICITADA",
        }

        schema = SchoolTransferCreate(**transfer_data)

        assert schema.motivo_transferencia == "MUDANCA_DE_ENDERECO"
        assert schema.status == "SOLICITADA"

    def test_school_transfer_create_same_school(self):
        """Testa validação com mesma escola de origem e destino."""
        school_id = str(uuid4())
        transfer_data = {
            "matricula_id": 1,
            "escola_origem_id": school_id,
            "escola_destino_id": school_id,  # mesma escola
            "motivo_transferencia": "MUDANCA_DE_ENDERECO",
            "data_transferencia": datetime.now(timezone.utc),
            "status": "SOLICITADA",
        }

        with pytest.raises(ValidationError) as exc_info:
            SchoolTransferCreate(**transfer_data)

        assert "escola_destino_id" in str(exc_info.value)


class TestAdultLiteracySchemas:
    """Testes para schemas de alfabetização de adultos."""

    def test_adult_literacy_create_valid(self):
        """Testa criação de schema de alfabetização com dados válidos."""
        literacy_data = {
            "participante_id": str(uuid4()),
            "nivel_alfabetizacao": "INICIANTE",
            "data_inscricao": datetime.now(timezone.utc),
            "turma_id": str(uuid4()),
            "instrutor_id": str(uuid4()),
            "frequencia": 85.5,
            "observacoes": "Progresso satisfatório",
        }

        schema = AdultLiteracyCreate(**literacy_data)

        assert schema.nivel_alfabetizacao == "INICIANTE"
        assert schema.frequencia == 85.5

    def test_adult_literacy_create_invalid_frequencia(self):
        """Testa validação com frequência inválida."""
        literacy_data = {
            "participante_id": str(uuid4()),
            "nivel_alfabetizacao": "INICIANTE",
            "data_inscricao": datetime.now(timezone.utc),
            "turma_id": str(uuid4()),
            "instrutor_id": str(uuid4()),
            "frequencia": 150.0,  # inválido (> 100)
        }

        with pytest.raises(ValidationError) as exc_info:
            AdultLiteracyCreate(**literacy_data)

        assert "frequencia" in str(exc_info.value)


class TestEducationStatistics:
    """Testes para schema de estatísticas educacionais."""

    def test_education_statistics_valid(self):
        """Testa schema de estatísticas com dados válidos."""
        stats_data = {
            "total_enrollments": 1000,
            "active_scholarships": 150,
            "schools_count": 25,
            "students_per_school": {"Escola A": 400, "Escola B": 350, "Escola C": 250},
            "enrollments_by_grade": {
                "1º Ano": 200,
                "2º Ano": 180,
                "3º Ano": 160,
                "4º Ano": 140,
                "5º Ano": 120,
                "6º Ano": 100,
                "7º Ano": 60,
                "8º Ano": 40,
            },
            "average_daily_attendance": 0.92,
            "school_meals_served_daily": 850,
        }

        schema = EducationStatistics(**stats_data)

        assert schema.total_enrollments == 1000
        assert schema.active_scholarships == 150
        assert len(schema.students_per_school) == 3
        assert schema.average_daily_attendance == 0.92

    def test_education_statistics_invalid_negative_values(self):
        """Testa validação com valores negativos."""
        stats_data = {
            "total_enrollments": -10,  # inválido
            "active_scholarships": 150,
            "schools_count": 25,
        }

        with pytest.raises(ValidationError) as exc_info:
            EducationStatistics(**stats_data)

        assert "total_enrollments" in str(exc_info.value)

    def test_education_statistics_invalid_attendance_rate(self):
        """Testa validação com taxa de frequência inválida."""
        stats_data = {
            "total_enrollments": 1000,
            "active_scholarships": 150,
            "schools_count": 25,
            "average_daily_attendance": 1.5,  # inválido (> 1.0)
        }

        with pytest.raises(ValidationError) as exc_info:
            EducationStatistics(**stats_data)

        assert "average_daily_attendance" in str(exc_info.value)

    def test_education_statistics_partial_data(self):
        """Testa schema com dados parciais (campos opcionais)."""
        stats_data = {
            "total_enrollments": 1000,
            "active_scholarships": 150,
            "schools_count": 25,
        }

        schema = EducationStatistics(**stats_data)

        assert schema.total_enrollments == 1000
        assert schema.students_per_school is None
        assert schema.enrollments_by_grade is None
        assert schema.average_daily_attendance is None


class TestSchemaSerialization:
    """Testes de serialização e desserialização dos schemas."""

    def test_student_enrollment_json_serialization(self, sample_enrollment_data):
        """Testa serialização JSON do schema de matrícula."""
        schema = StudentEnrollmentCreate(**sample_enrollment_data)
        json_data = schema.model_dump_json()

        assert "numero_matricula" in json_data
        assert "2025EDU001234" in json_data

    def test_student_enrollment_dict_serialization(self, sample_enrollment_data):
        """Testa serialização em dicionário do schema de matrícula."""
        schema = StudentEnrollmentCreate(**sample_enrollment_data)
        dict_data = schema.model_dump()

        assert (
            dict_data["numero_matricula"] == sample_enrollment_data["numero_matricula"]
        )
        assert dict_data["nome_estudante"] == sample_enrollment_data["nome_estudante"]

    def test_scholarship_json_serialization(self, sample_scholarship_data):
        """Testa serialização JSON do schema de bolsa."""
        schema = ScholarshipCreate(**sample_scholarship_data)
        json_data = schema.model_dump_json()

        assert "tipo_bolsa" in json_data
        assert "INTEGRAL" in json_data

    def test_schema_exclusion_fields(self, sample_enrollment_data):
        """Testa exclusão de campos na serialização."""
        response_data = {
            "id": 1,
            **sample_enrollment_data,
            "criado_em": datetime.now(timezone.utc),
            "atualizado_em": datetime.now(timezone.utc),
        }

        schema = StudentEnrollmentResponse(**response_data)

        # Serializa excluindo campos sensíveis
        dict_data = schema.model_dump(exclude={"contato_responsavel"})

        assert "contato_responsavel" not in dict_data
        assert "numero_matricula" in dict_data

    def test_schema_datetime_serialization(self, sample_enrollment_data):
        """Testa serialização de campos datetime."""
        schema = StudentEnrollmentCreate(**sample_enrollment_data)
        dict_data = schema.model_dump()

        # Datetime deve ser serializado como ISO string
        assert isinstance(dict_data["data_nascimento"], str)
        assert isinstance(dict_data["data_matricula"], str)
