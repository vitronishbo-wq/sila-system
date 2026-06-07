from apps.backend.app.modules.governance.statistics.tests._fakes import named_payload


def test_crud_relatorios(client):
    create = client.post("/api/v1/estatistica/relatorios/", json=named_payload("relatorio-a"))
    assert create.status_code == 201
    relatorio_id = create.json()["id"]
    listed = client.get("/api/v1/estatistica/relatorios/")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    detail = client.get(f"/api/v1/estatistica/relatorios/{relatorio_id}")
    assert detail.status_code == 200
    patched = client.patch(
        f"/api/v1/estatistica/relatorios/{relatorio_id}", json={"nome": "relatorio-b"}
    )
    assert patched.status_code == 200
    assert patched.json()["nome"] == "relatorio-b"
    deleted = client.delete(f"/api/v1/estatistica/relatorios/{relatorio_id}")
    assert deleted.status_code == 204
