from apps.backend.app.core.middleware.idempotency_middleware import IdempotencyMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient


def test_post_without_idempotency_key_returns_400():
    app = FastAPI()
    app.add_middleware(IdempotencyMiddleware)

    @app.post("/api/v1/educacao/matriculas")
    def create():
        return JSONResponse({"ok": True})

    with TestClient(app) as client:
        r = client.post("/api/v1/educacao/matriculas", json={"a": 1})

    assert r.status_code == 400
    assert "Idempotency-Key header is required" in r.text


def test_post_with_idempotency_key_allows_request():
    app = FastAPI()
    app.add_middleware(IdempotencyMiddleware)

    @app.post("/api/v1/educacao/matriculas")
    def create():
        return JSONResponse({"ok": True})

    with TestClient(app) as client:
        r = client.post(
            "/api/v1/educacao/matriculas", headers={"Idempotency-Key": "abc"}, json={}
        )

    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_get_without_idempotency_key_allowed():
    app = FastAPI()
    app.add_middleware(IdempotencyMiddleware)

    @app.get("/api/v1/educacao/matriculas")
    def list_():
        return JSONResponse({"ok": True})

    with TestClient(app) as client:
        r = client.get("/api/v1/educacao/matriculas")

    assert r.status_code == 200
    assert r.json() == {"ok": True}
