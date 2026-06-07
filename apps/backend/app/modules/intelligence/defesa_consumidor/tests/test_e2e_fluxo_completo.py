import os

import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app

client = TestClient(app)


@pytest.mark.e2e
def test_fluxo_completo_reclamacao():
    if os.environ.get("RUN_DEFESA_CONSUMIDOR_E2E") != "1":
        pytest.skip("Defina RUN_DEFESA_CONSUMIDOR_E2E=1 para executar e2e do modulo")
    data = {
        "consumidor_id": 1,
        "estabelecimento_id": 1,
        "produto_servico": "Notebook XY",
        "descricao": "Produto nao funcionou apos 3 dias",
        "categoria": "produto_defectuoso",
        "valor_reclamado": 1500.0,
        "prioridade": "media",
    }
    resp = client.post("/api/v1/defesa_consumidor/reclamacoes/", json=data)
    assert resp.status_code == 201
    reclamacao = resp.json()
    rid = reclamacao["id"]
    resp = client.get(f"/api/v1/defesa_consumidor/reclamacoes/{rid}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "aberta"
    resp = client.patch(
        f"/api/v1/defesa_consumidor/reclamacoes/{rid}/status", params={"novo_status": "em_analise"}
    )
    assert resp.status_code == 200
    resp = client.patch(f"/api/v1/defesa_consumidor/reclamacoes/{rid}/escalar")
    assert resp.status_code == 200
    resp = client.patch(
        f"/api/v1/defesa_consumidor/reclamacoes/{rid}/finalizar", params={"resolvido": True}
    )
    assert resp.status_code == 200
