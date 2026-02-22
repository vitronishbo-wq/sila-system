"""Testes de integração para os endpoints do módulo de saúde."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

# Test client
client = TestClient(app)


@pytest.fixture
def sample_record():
    """Retorna um registro de saúde de exemplo."""
    return {
        "tipo_consulta": "Consulta de rotina",
        "data_consulta": datetime.now(timezone.utc).isoformat(),
        "diagnostico": "Hipertensão",
        "tratamento": "Medicação",
        "observacoes": "Retornar em 30 dias",
        "cidadao_id": str(uuid4()),
    }


class TestHealthEndpoints:
    def test_create_health_record(self, sample_record):
        """Testa a criação de um novo registro de saúde."""
        response = client.post("/health/", json=sample_record)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["tipo_consulta"] == sample_record["tipo_consulta"]

    def test_get_health_record(self, sample_record):
        """Testa a recuperação de um registro de saúde por ID."""
        # cria primeiro
        create_resp = client.post("/health/", json=sample_record)
        record_id = create_resp.json()["id"]

        # busca
        response = client.get(f"/health/{record_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == record_id

    def test_list_health_records(self, sample_record):
        """Testa a listagem de registros de saúde."""
        client.post("/health/", json=sample_record)
        response = client.get("/health/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1

    def test_update_health_record(self, sample_record):
        """Testa a atualização de um registro de saúde."""
        create_resp = client.post("/health/", json=sample_record)
        record_id = create_resp.json()["id"]

        update_data = {
            "tratamento": "Nova medicação",
            "observacoes": "Retornar em 15 dias",
        }

        response = client.put(f"/health/{record_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["tratamento"] == "Nova medicação"

    def test_delete_health_record(self, sample_record):
        """Testa a exclusão de um registro de saúde."""
        create_resp = client.post("/health/", json=sample_record)
        record_id = create_resp.json()["id"]

        response = client.delete(f"/health/{record_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # confirmação de remoção
        resp_check = client.get(f"/health/{record_id}")
        assert resp_check.status_code == status.HTTP_404_NOT_FOUND
