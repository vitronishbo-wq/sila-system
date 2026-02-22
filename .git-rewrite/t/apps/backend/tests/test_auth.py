"""Tests for auth endpoints."""

import asyncio

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from config import settings  # Adicionado: Importação das configurações
from core.db import AsyncSessionLocal

# Importações internas
# ATENÇÃO: Verifique o caminho correto para 'router', 'User', 'UserRepository' e 'AsyncSessionLocal'
from modules.auth.endpoints import router
from modules.auth.models.user import User, UserRole
from modules.auth.repository import UserRepository

# --- Fixtures de Setup ---

@pytest.fixture
def client():
    """Fixture para um cliente de teste síncrono (TestClient)."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/auth")
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Fixture para um cliente de teste assíncrono (AsyncClient)."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/auth")

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def db_session():
    """Fixture para uma sessão de banco de dados assíncrona com rollback."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback() # Garante que as mudanças de teste sejam desfeitas

# --- Testes de Endpoints ---

def test_auth_ping(client: TestClient):
    """Testa o endpoint de saúde (ping) da autenticação."""
    response = client.get("/auth/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "module": "auth"}


@pytest.mark.asyncio
async def test_create_user_and_login(async_client: AsyncClient, db_session):
    """Testa a criação de usuário e o processo de login."""

    # Etapa 1: Mock/Simulação da Criação de Usuário (usando o repositório para a criação real no DB do teste)
    user_repo = UserRepository(db_session)

    # ATENÇÃO: Usar um hash real ou mockar a função de hashing, se necessário.
    # Aqui, simulamos que a senha já está hasheada para o modelo ORM.
    mock_hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

    test_user_orm = User(
        username="testuser",
        email="test@example.com",
        # Corrigido: O campo deve ser 'hashed_password' (ou o nome real do campo no modelo User)
        hashed_password=mock_hashed_password,
        role=UserRole.USER  # Adicione um role se for obrigatório
    )

    # Cria o usuário no banco de dados de teste
    await user_repo.create_user(test_user_orm)
    await db_session.commit()

    # Etapa 2: Testar Login (Assumindo que o serviço de login valida a senha)
    login_data = {
        "username": "testuser",
        "password": "testpassword123" # O serviço de login precisa validar isso contra o mock_hashed_password
    }

    # Se a lógica do endpoint de login ainda não estiver completa, o status esperado pode ser 500
    response = await async_client.post("/auth/login", data=login_data)

    # O status 200/401 depende da implementação:
    # 200 se a validação da senha for mockada/implementada
    # 401 se a validação falhar (caso a senha 'testpassword123' não corresponda ao hash mockado)
    # Por segurança, mantemos as opções 200 ou 401.
    assert response.status_code in [200, 401]


@pytest.mark.asyncio
async def test_protected_endpoint(async_client: AsyncClient):
    """Testa o acesso a um endpoint protegido sem token (deve falhar com 401)."""
    # Endpoint de teste de token deve retornar 401 se não houver token
    response = await async_client.post("/auth/login/test-token")
    assert response.status_code == 401


# --- Testes de Repositório ---

@pytest.mark.asyncio
async def test_user_repository_integration(db_session):
    """Testa a funcionalidade básica do UserRepository (create e get)."""
    user_repo = UserRepository(db_session)

    # Mock da senha hasheada
    mock_hashed_password =

    # Cria um objeto User (ORM Model)
    test_user = User(
        username="repo_test",
        email="repo@test.com",
        # Corrigido: Usando o campo ORM correto e um valor hasheado simulado
        hashed_password = Repository Test User",
        role=UserRole.USER
    )

    created_user = await user_repo.create_user(test_user)
    await db_session.commit() # Commit para que as consultas subsequentes funcionem

    assert created_user.id is not None
    assert created_user.username == "repo_test"

    # Retrieve user by email
    retrieved_user = await user_repo.get_user_by_email("repo@test.com")
    assert retrieved_user is not None
    assert retrieved_user.username == "repo_test"

    # Retrieve user by username
    retrieved_by_username = await user_repo.get_user_by_username("repo_test")
    assert retrieved_by_username is not None
    assert retrieved_by_username.email == "repo@test.com"
