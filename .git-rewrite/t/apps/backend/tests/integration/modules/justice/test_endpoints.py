"""Testes de integração para os endpoints do módulo justice."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

# Test client
client = TestClient(app)


@pytest.fixture
def sample_legal_case():
    """Retorna um caso jurídico de exemplo."""
    return {
        "numero_processo": "2025.0001234-5",
        "tipo_caso": "CIVIL",
        "status": "REGISTERED",
        "prioridade": "MEDIUM",
        "titulo": "Cobrança de Dívida",
        "descricao": "Ação de cobrança de dívida contratual",
        "cliente_id": str(uuid4()),
        "advogado_id": str(uuid4()),
        "data_abertura": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture
def sample_legal_document():
    """Retorna um documento jurídico de exemplo."""
    return {
        "tipo_documento": "PETICAO_INICIAL",
        "numero_documento": "DOC-2025-001",
        "titulo": "Petição Inicial - Cobrança",
        "conteudo": "Exmo. Sr. Dr. Juiz de Direito...",
        "caso_id": str(uuid4()),
        "advogado_id": str(uuid4()),
        "data_documento": datetime.now(timezone.utc).isoformat(),
    }


class TestJusticeEndpoints:
    """Testes para os endpoints do módulo justice."""

    def test_ping_endpoint(self):
        """Testa o endpoint de health check do módulo justice."""
        response = client.get("/justice/ping")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok", "module": "justice"}

    def test_create_legal_case(self, sample_legal_case):
        """Testa a criação de um novo caso jurídico."""
        response = client.post("/justice/cases", json=sample_legal_case)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["numero_processo"] == sample_legal_case["numero_processo"]

    def test_get_legal_case(self, sample_legal_case):
        """Testa a recuperação de um caso jurídico por ID."""
        # cria primeiro
        create_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = create_resp.json()["id"]

        # busca
        response = client.get(f"/justice/cases/{case_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == case_id

    def test_list_legal_cases(self, sample_legal_case):
        """Testa a listagem de casos jurídicos."""
        # cria alguns casos
        for _ in range(3):
            client.post("/justice/cases", json=sample_legal_case)

        # lista
        response = client.get("/justice/cases")
        assert response.status_code == status.HTTP_200_OK
        cases = response.json()
        assert len(cases) >= 3

    def test_update_legal_case(self, sample_legal_case):
        """Testa a atualização de um caso jurídico."""
        # cria
        create_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = create_resp.json()["id"]

        # atualiza
        update_data = {"status": "IN_PROGRESS", "prioridade": "HIGH"}
        response = client.put(f"/justice/cases/{case_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        updated_case = response.json()
        assert updated_case["status"] == "IN_PROGRESS"

    def test_delete_legal_case(self, sample_legal_case):
        """Testa a exclusão de um caso jurídico."""
        # cria
        create_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = create_resp.json()["id"]

        # exclui
        response = client.delete(f"/justice/cases/{case_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verifica que foi excluído
        response = client.get(f"/justice/cases/{case_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_legal_document(self, sample_legal_document):
        """Testa a criação de um documento jurídico."""
        response = client.post("/justice/documents", json=sample_legal_document)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert (
            response_data["tipo_documento"] == sample_legal_document["tipo_documento"]
        )

    def test_list_case_documents(self, sample_legal_case, sample_legal_document):
        """Testa a listagem de documentos de um caso."""
        # cria um caso
        case_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = case_resp.json()["id"]

        # associa o documento ao caso
        sample_legal_document["caso_id"] = case_id

        # cria alguns documentos
        for _ in range(2):
            client.post("/justice/documents", json=sample_legal_document)

        # lista documentos do caso
        response = client.get(f"/justice/cases/{case_id}/documents")
        assert response.status_code == status.HTTP_200_OK
        documents = response.json()
        assert len(documents) >= 2

    def test_get_case_timeline(self, sample_legal_case):
        """Testa a obtenção da timeline de um caso."""
        # cria um caso
        case_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = case_resp.json()["id"]

        # obtém timeline
        response = client.get(f"/justice/cases/{case_id}/timeline")
        assert response.status_code == status.HTTP_200_OK
        timeline = response.json()
        assert "events" in timeline
        assert isinstance(timeline["events"], list)

    def test_search_legal_cases(self, sample_legal_case):
        """Testa a busca de casos jurídicos."""
        # cria alguns casos
        client.post("/justice/cases", json=sample_legal_case)

        # busca por número de processo
        response = client.get(
            "/justice/cases/search",
            params={"numero_processo": sample_legal_case["numero_processo"]},
        )
        assert response.status_code == status.HTTP_200_OK
        cases = response.json()
        assert len(cases) >= 1
        assert cases[0]["numero_processo"] == sample_legal_case["numero_processo"]

    def test_get_legal_statistics(self):
        """Testa a obtenção de estatísticas jurídicas."""
        response = client.get("/justice/statistics")
        assert response.status_code == status.HTTP_200_OK
        stats = response.json()
        assert "total_cases" in stats
        assert "cases_by_status" in stats
        assert "cases_by_type" in stats

    def test_invalid_legal_case(self):
        """Testa criação de caso com dados inválidos."""
        invalid_data = {
            "numero_processo": "",  # vazio
            "tipo_caso": "TIPO_INVALIDO",  # inválido
            "status": "STATUS_INVALIDO",  # inválido
            "cliente_id": "uuid-invalido",  # formato inválido
        }
        response = client.post("/justice/cases", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_nonexistent_legal_case(self):
        """Testa busca por caso inexistente."""
        fake_id = str(uuid4())
        response = client.get(f"/justice/cases/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_court_hearing(self, sample_legal_case):
        """Testa a criação de audiência judicial."""
        # cria um caso
        case_resp = client.post("/justice/cases", json=sample_legal_case)
        case_id = case_resp.json()["id"]

        hearing_data = {
            "caso_id": case_id,
            "tipo_audiencia": "INSTRUCAO",
            "data_audiencia": datetime.now(timezone.utc).isoformat(),
            "local": "Fórum Central - Sala 101",
            "juiz": "Dr. João da Silva",
            "observacoes": "Audiência de instrução e julgamento",
        }

        response = client.post("/justice/hearings", json=hearing_data)
        assert response.status_code == status.HTTP_201_CREATED
        hearing = response.json()
        assert "id" in hearing
        assert hearing["tipo_audiencia"] == "INSTRUCAO"

    def test_list_upcoming_hearings(self):
        """Testa a listagem de audiências futuras."""
        response = client.get("/justice/hearings/upcoming")
        assert response.status_code == status.HTTP_200_OK
        hearings = response.json()
        assert isinstance(hearings, list)
