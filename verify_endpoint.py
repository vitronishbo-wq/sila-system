import asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
import sys
import os

# Set PYTHONPATH
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))

from app.modules.administracao_local.api.router import router

async def test_get_administrador_endpoint():
    print("Running integration test...")
    app = FastAPI()
    app.include_router(router)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/administracao-local/administradores/123")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "123"
    assert data["nome"] == "Admin Teste"
    print("Endpoint test passed! ✔")

if __name__ == "__main__":
    asyncio.run(test_get_administrador_endpoint())
