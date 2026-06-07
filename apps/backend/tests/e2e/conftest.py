"""Configuração para testes E2E"""

import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient

# Para adicionar app quando estiver ready
# from apps.backend.app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Criar event loop para testes"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP para testes"""
    # Quando tiver app configurada:
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     yield ac

    # Para agora, retornar mock
    yield None


@pytest.fixture
async def auth_token() -> str:
    """Token de autenticação para testes"""
    return "test_token_e2e"


@pytest.fixture(scope="function")
async def clean_db():
    """Limpar base de dados antes/depois dos testes"""
    # Setup
    yield
    # Teardown - limpar dados de teste
    # Implementar limpeza específica por módulo
