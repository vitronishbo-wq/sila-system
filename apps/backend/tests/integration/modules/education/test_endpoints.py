"""Testes de integração para os endpoints do módulo education."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

# Test client
client = TestClient(app)


@pytest.fixture
def sample_student_enrollment():
    """Retorna uma matrícula estudantil de exemplo."""
    return {
        "numero_matricula": "2025EDU001234",
        "nome_estudante": "João da Silva",
        "data_nascimento": "2010-05-15",
        "genero": "M",
        "nome_responsavel": "Maria da Silva",
        "contato_responsavel": "912345678",
        "escola_id": str(uuid4()),
        "serie": "5º Ano",
        "turma": "A",
        "turno": "MANHA",
        "data_matricula": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture
def sample_scholarship():
    """Retorna uma bolsa de estudos de exemplo."""
    return {
        "tipo_bolsa": "INTEGRAL",
        "motivo_bolsa": "BAIXA_RENDA",
        "percentual_desconto": 100.0,
        "estudante_id": str(uuid4()),
        "instituicao_id": str(uuid4()),
        "data_concessao": datetime.now(timezone.utc).isoformat(),
        "vigencia_inicio": "2025-01-01",
        "vigencia_fim": "2025-12-31",
        "status": "ATIVA",
    }


@pytest.fixture
def sample_school_meal():
    """Retorna um registro de merenda escolar de exemplo."""
    return {
        "data_refeicao": datetime.now(timezone.utc).isoformat(),
        "tipo_refeicao": "ALMOCO",
        "escola_id": str(uuid4()),
        "estudante_id": str(uuid4()),
        "nutricionista_responsavel": "Dr. Ana Nutricionista",
        "cardapio": "Arroz, feijão, carne, salada e fruta",
        "calorias": 650,
        "observacoes": "Refeição balanceada",
    }


class TestEducationEndpoints:
    """Testes para os endpoints do módulo education."""

    def test_ping_endpoint(self):
        """Testa o endpoint de health check do módulo education."""
        response = client.get("/education/ping")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok", "module": "education"}

    def test_create_student_enrollment(self, sample_student_enrollment):
        """Testa a criação de uma nova matrícula estudantil."""
        response = client.post("/education/enrollments", json=sample_student_enrollment)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert (
            response_data["numero_matricula"]
            == sample_student_enrollment["numero_matricula"]
        )

    def test_get_student_enrollment(self, sample_student_enrollment):
        """Testa a recuperação de uma matrícula por ID."""
        # cria primeiro
        create_resp = client.post(
            "/education/enrollments", json=sample_student_enrollment
        )
        enrollment_id = create_resp.json()["id"]

        # busca
        response = client.get(f"/education/enrollments/{enrollment_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == enrollment_id

    def test_list_student_enrollments(self, sample_student_enrollment):
        """Testa a listagem de matrículas estudantis."""
        # cria algumas matrículas
        for _ in range(3):
            client.post("/education/enrollments", json=sample_student_enrollment)

        # lista
        response = client.get("/education/enrollments")
        assert response.status_code == status.HTTP_200_OK
        enrollments = response.json()
        assert len(enrollments) >= 3

    def test_update_student_enrollment(self, sample_student_enrollment):
        """Testa a atualização de uma matrícula estudantil."""
        # cria
        create_resp = client.post(
            "/education/enrollments", json=sample_student_enrollment
        )
        enrollment_id = create_resp.json()["id"]

        # atualiza
        update_data = {"turma": "B", "turno": "TARDE"}
        response = client.put(
            f"/education/enrollments/{enrollment_id}", json=update_data
        )
        assert response.status_code == status.HTTP_200_OK
        updated_enrollment = response.json()
        assert updated_enrollment["turma"] == "B"

    def test_delete_student_enrollment(self, sample_student_enrollment):
        """Testa a exclusão de uma matrícula estudantil."""
        # cria
        create_resp = client.post(
            "/education/enrollments", json=sample_student_enrollment
        )
        enrollment_id = create_resp.json()["id"]

        # exclui
        response = client.delete(f"/education/enrollments/{enrollment_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verifica que foi excluído
        response = client.get(f"/education/enrollments/{enrollment_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_scholarship(self, sample_scholarship):
        """Testa a criação de uma bolsa de estudos."""
        response = client.post("/education/scholarships", json=sample_scholarship)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["tipo_bolsa"] == sample_scholarship["tipo_bolsa"]

    def test_list_scholarships_by_student(self, sample_scholarship):
        """Testa a listagem de bolsas por estudante."""
        # cria uma bolsa
        scholarship_resp = client.post(
            "/education/scholarships", json=sample_scholarship
        )
        student_id = sample_scholarship["estudante_id"]

        # lista bolsas do estudante
        response = client.get(f"/education/students/{student_id}/scholarships")
        assert response.status_code == status.HTTP_200_OK
        scholarships = response.json()
        assert len(scholarships) >= 1

    def test_create_school_meal_record(self, sample_school_meal):
        """Testa a criação de um registro de merenda escolar."""
        response = client.post("/education/school-meals", json=sample_school_meal)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["tipo_refeicao"] == sample_school_meal["tipo_refeicao"]

    def test_list_school_meals_by_date(self, sample_school_meal):
        """Testa a listagem de refeições por data."""
        # cria alguns registros
        for _ in range(2):
            client.post("/education/school-meals", json=sample_school_meal)

        # lista por data de hoje
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        response = client.get(f"/education/school-meals/date/{today}")
        assert response.status_code == status.HTTP_200_OK
        meals = response.json()
        assert len(meals) >= 2

    def test_get_student_academic_record(self, sample_student_enrollment):
        """Testa a obtenção do histórico acadêmico de um estudante."""
        # cria uma matrícula
        enrollment_resp = client.post(
            "/education/enrollments", json=sample_student_enrollment
        )
        student_id = enrollment_resp.json()["estudante_id"]

        # obtém histórico
        response = client.get(f"/education/students/{student_id}/academic-record")
        assert response.status_code == status.HTTP_200_OK
        record = response.json()
        assert "enrollments" in record
        assert "grades" in record
        assert "attendance" in record

    def test_create_school_transfer(self, sample_student_enrollment):
        """Testa a criação de uma transferência escolar."""
        # cria uma matrícula
        enrollment_resp = client.post(
            "/education/enrollments", json=sample_student_enrollment
        )
        enrollment_id = enrollment_resp.json()["id"]

        transfer_data = {
            "matricula_id": enrollment_id,
            "escola_origem_id": sample_student_enrollment["escola_id"],
            "escola_destino_id": str(uuid4()),
            "motivo_transferencia": "MUDANCA_DE_ENDERECO",
            "data_transferencia": datetime.now(timezone.utc).isoformat(),
            "status": "SOLICITADA",
        }

        response = client.post("/education/transfers", json=transfer_data)
        assert response.status_code == status.HTTP_201_CREATED
        transfer = response.json()
        assert "id" in transfer
        assert transfer["motivo_transferencia"] == "MUDANCA_DE_ENDERECO"

    def test_get_education_statistics(self):
        """Testa a obtenção de estatísticas educacionais."""
        response = client.get("/education/statistics")
        assert response.status_code == status.HTTP_200_OK
        stats = response.json()
        assert "total_enrollments" in stats
        assert "active_scholarships" in stats
        assert "schools_count" in stats

    def test_search_enrollments_by_name(self, sample_student_enrollment):
        """Testa a busca de matrículas por nome do estudante."""
        # cria uma matrícula
        client.post("/education/enrollments", json=sample_student_enrollment)

        # busca por nome
        response = client.get(
            "/education/enrollments/search", params={"nome_estudante": "João"}
        )
        assert response.status_code == status.HTTP_200_OK
        enrollments = response.json()
        assert len(enrollments) >= 1
        assert "João" in enrollments[0]["nome_estudante"]

    def test_invalid_student_enrollment(self):
        """Testa criação de matrícula com dados inválidos."""
        invalid_data = {
            "numero_matricula": "",  # vazio
            "nome_estudante": "",  # vazio
            "data_nascimento": "data-invalida",  # formato inválido
            "escola_id": "uuid-invalido",  # formato inválido
        }
        response = client.post("/education/enrollments", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_nonexistent_enrollment(self):
        """Testa busca por matrícula inexistente."""
        fake_id = str(uuid4())
        response = client.get(f"/education/enrollments/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_adult_literacy_record(self):
        """Testa a criação de registro de alfabetização de adultos."""
        literacy_data = {
            "participante_id": str(uuid4()),
            "nivel_alfabetizacao": "INICIANTE",
            "data_inscricao": datetime.now(timezone.utc).isoformat(),
            "turma_id": str(uuid4()),
            "instrutor_id": str(uuid4()),
            "frequencia": 85.5,
            "observacoes": "Progresso satisfatório",
        }

        response = client.post("/education/adult-literacy", json=literacy_data)
        assert response.status_code == status.HTTP_201_CREATED
        record = response.json()
        assert "id" in record
        assert record["nivel_alfabetizacao"] == "INICIANTE"

    def test_list_technical_courses(self):
        """Testa a listagem de cursos técnicos."""
        response = client.get("/education/technical-courses")
        assert response.status_code == status.HTTP_200_OK
        courses = response.json()
        assert isinstance(courses, list)
