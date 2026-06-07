from datetime import UTC, datetime, timedelta

from apps.backend.app.modules.governance.statistics.tests._fakes import metrica_payload


def test_registrar_e_listar_timeseries(client):
    m_resp = client.post("/api/v1/estatistica/metricas/", json=metrica_payload())
    metrica_id = m_resp.json()["id"]
    now = datetime.now(UTC)
    for i in range(3):
        payload = {
            "metrica_id": metrica_id,
            "timestamp": (now + timedelta(minutes=i)).isoformat(),
            "valor": float(i + 1),
        }
        resp = client.post("/api/v1/estatistica/timeseries/", json=payload)
        assert resp.status_code == 201
    list_resp = client.get(f"/api/v1/estatistica/timeseries/metrica/{metrica_id}")
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] == 3
    latest_resp = client.get(f"/api/v1/estatistica/timeseries/metrica/{metrica_id}/latest")
    assert latest_resp.status_code == 200
    assert latest_resp.json()["valor"] == 3.0
