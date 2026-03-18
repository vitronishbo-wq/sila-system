from __future__ import annotations
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.industry.api.router import router as industria_router

def test_http_catalogo_ramos_retorna_lista():
    app = FastAPI()
    app.include_router(industria_router)
    client = TestClient(app)
    response = client.get('/industria/ramos')
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert any((item['codigo'] == 'quimica' for item in payload))
    assert any(('descricao' in item for item in payload))

def test_http_catalogo_portes_retorna_lista():
    app = FastAPI()
    app.include_router(industria_router)
    client = TestClient(app)
    response = client.get('/industria/portes')
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert [item['codigo'] for item in payload] == ['micro', 'pequena', 'media', 'grande']