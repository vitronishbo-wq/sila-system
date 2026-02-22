"""Testes de integração para os endpoints do módulo sanitation."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

# Test client
client = TestClient(app)


@pytest.fixture
def sample_sanitation_record():
    """Retorna um registro de saneamento de exemplo."""
    return {
        "tipo_servico": "Coleta de Lixo",
        "data_servico": datetime.now(timezone.utc).isoformat(),
        "localizacao": "Rua dos Testes, 123",
        "status": "PENDENTE",
        "observacoes": "Coleta programada",
        "cidadao_id": str(uuid4()),
    }


@pytest.fixture
def sample_water_treatment():
    """Retorna um registro de tratamento de água de exemplo."""
    return {
        "tipo_tratamento": "Cloração",
        "data_tratamento": datetime.now(timezone.utc).isoformat(),
        "volume_tratado": 1000.0,
        "localizacao": "Estação de Tratamento Central",
        "responsavel_id": str(uuid4()),
    }


class TestSanitationEndpoints:
    """Testes para os endpoints do módulo sanitation."""

    def test_ping_endpoint(self):
        """Testa o endpoint de health check do módulo sanitation."""
        response = client.get("/sanitation/ping")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok", "module": "sanitation"}

    def test_create_sanitation_record(self, sample_sanitation_record):
        """Testa a criação de um novo registro de saneamento."""
        response = client.post("/sanitation/", json=sample_sanitation_record)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["tipo_servico"] == sample_sanitation_record["tipo_servico"]

    def test_get_sanitation_record(self, sample_sanitation_record):
        """Testa a recuperação de um registro de saneamento por ID."""
        # cria primeiro
        create_resp = client.post("/sanitation/", json=sample_sanitation_record)
        record_id = create_resp.json()["id"]

        # busca
        response = client.get(f"/sanitation/{record_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == record_id

    def test_list_sanitation_records(self, sample_sanitation_record):
        """Testa a listagem de registros de saneamento."""
        # cria alguns registros
        for _ in range(3):
            client.post("/sanitation/", json=sample_sanitation_record)

        # lista
        response = client.get("/sanitation/")
        assert response.status_code == status.HTTP_200_OK
        records = response.json()
        assert len(records) >= 3

    def test_update_sanitation_record(self, sample_sanitation_record):
        """Testa a atualização de um registro de saneamento."""
        # cria
        create_resp = client.post("/sanitation/", json=sample_sanitation_record)
        record_id = create_resp.json()["id"]

        # atualiza
        update_data = {
            "status": "CONCLUIDO",
            "observacoes": "Serviço concluído com sucesso",
        }
        response = client.put(f"/sanitation/{record_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        updated_record = response.json()
        assert updated_record["status"] == "CONCLUIDO"

    def test_delete_sanitation_record(self, sample_sanitation_record):
        """Testa a exclusão de um registro de saneamento."""
        # cria
        create_resp = client.post("/sanitation/", json=sample_sanitation_record)
        record_id = create_resp.json()["id"]

        # exclui
        response = client.delete(f"/sanitation/{record_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verifica que foi excluído
        response = client.get(f"/sanitation/{record_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_water_treatment_record(self, sample_water_treatment):
        """Testa a criação de um registro de tratamento de água."""
        response = client.post(
            "/sanitation/water-treatment", json=sample_water_treatment
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert (
            response_data["tipo_tratamento"]
            == sample_water_treatment["tipo_tratamento"]
        )

    def test_list_water_treatment_records(self, sample_water_treatment):
        """Testa a listagem de registros de tratamento de água."""
        # cria alguns registros
        for _ in range(2):
            client.post("/sanitation/water-treatment", json=sample_water_treatment)

        # lista
        response = client.get("/sanitation/water-treatment")
        assert response.status_code == status.HTTP_200_OK
        records = response.json()
        assert len(records) >= 2

    def test_get_sanitation_statistics(self):
        """Testa a obtenção de estatísticas de saneamento."""
        response = client.get("/sanitation/statistics")
        assert response.status_code == status.HTTP_200_OK
        stats = response.json()
        assert "total_records" in stats
        assert "pending_services" in stats
        assert "completed_services" in stats

    def test_invalid_sanitation_record(self):
        """Testa criação de registro com dados inválidos."""
        invalid_data = {
            "tipo_servico": "",  # vazio
            "data_servico": "data-invalida",  # formato inválido
            "localizacao": "",  # vazio
        }
        response = client.post("/sanitation/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_nonexistent_sanitation_record(self):
        """Testa busca por registro inexistente."""
        fake_id = str(uuid4())
        response = client.get(f"/sanitation/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
