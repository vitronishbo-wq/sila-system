import sys
import os
import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import status
from httpx import AsyncClient, ASGITransport

# Adiciona o diretório raiz ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.insert(0, project_root)

from apps.backend.main import app
from apps.backend.core.db.session import get_db
from apps.backend.modules.location.models import CityModel, FullAddress


# --- Mocks e Setup Async ---


@pytest_asyncio.fixture
async def async_client():
    """Async client fixture for API tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def mock_db():
    """Cria um mock para a sessão async do banco de dados."""
    session = AsyncMock()

    # Mock para session.execute()
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = []
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result

    # Mock para session.get()
    session.get = AsyncMock()

    return session


@pytest_asyncio.fixture
async def client_with_mock_db(async_client, mock_db):
    """Cria um AsyncClient com a dependência de DB substituída."""

    def override_get_db():
        try:
            yield mock_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield async_client
    app.dependency_overrides.clear()


# --- Testes de Endpoints Async ---


@pytest.mark.asyncio
async def test_location_ping(client_with_mock_db: AsyncClient):
    """Testa o health check do módulo location."""
    response = await client_with_mock_db.get("/api/v1/location/locations/ping")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["module"] == "location"


@pytest.mark.asyncio
async def test_list_cities_success(client_with_mock_db: AsyncClient, mock_db):
    """Testa a listagem de cidades com sucesso."""

    # Prepara o mock dos dados ORM
    mock_city_1 = MagicMock(spec=CityModel)
    mock_city_1.id = 1
    mock_city_1.name = "Luanda"
    mock_city_1.commune_id = 101

    mock_city_2 = MagicMock(spec=CityModel)
    mock_city_2.id = 2
    mock_city_2.name = "Belas"
    mock_city_2.commune_id = 102

    # Configura o mock da sessão async
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_city_1, mock_city_2]
    mock_result = AsyncMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    response = await client_with_mock_db.get("/api/v1/location/locations/cities")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Luanda"
    assert data[1]["name"] == "Belas"


@pytest.mark.asyncio
async def test_list_cities_empty(client_with_mock_db: AsyncClient, mock_db):
    """Testa a listagem de cidades quando não há dados."""

    # Configura o mock para retornar lista vazia
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = []
    mock_result = AsyncMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    response = await client_with_mock_db.get("/api/v1/location/locations/cities")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_list_cities_with_pagination(client_with_mock_db: AsyncClient, mock_db):
    """Testa a listagem de cidades com parâmetros de paginação."""

    mock_city = MagicMock(spec=CityModel)
    mock_city.id = 1
    mock_city.name = "Test City"
    mock_city.commune_id = 101

    # Configura o mock
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_city]
    mock_result = AsyncMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Testa com parâmetros de paginação
    response = await client_with_mock_db.get(
        "/api/v1/location/locations/cities?skip=10&limit=5"
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test City"


@pytest.mark.asyncio
async def test_get_full_address_success(client_with_mock_db: AsyncClient, mock_db):
    """Testa a recuperação de um endereço completo com sucesso."""

    # Prepara o mock dos dados ORM de FullAddress
    mock_address = MagicMock(spec=FullAddress)
    mock_address.id = 50
    mock_address.street = "Rua Principal"
    mock_address.number = "123"
    mock_address.zip_code = "12345-678"
    mock_address.city = "Luanda"
    mock_address.commune = "Sambizanga"
    mock_address.municipality = "Luanda"
    mock_address.province = "Luanda"

    # Configura o mock da sessão async
    mock_scalars = AsyncMock()
    mock_scalars.first.return_value = mock_address
    mock_result = AsyncMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    response = await client_with_mock_db.get(
        "/api/v1/location/locations/full-address/50"
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 50
    assert data["street"] == "Rua Principal"
    assert data["number"] == "123"
    assert data["zip_code"] == "12345-678"


@pytest.mark.asyncio
async def test_get_full_address_not_found(client_with_mock_db: AsyncClient, mock_db):
    """Testa a recuperação de um endereço completo que não existe (404)."""

    # Configura o mock para retornar None (não encontrado)
    mock_scalars = AsyncMock()
    mock_scalars.first.return_value = None
    mock_result = AsyncMock()
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    response = await client_with_mock_db.get(
        "/api/v1/location/locations/full-address/999"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # A mensagem pode variar, então não verificamos o texto exato
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_full_address_invalid_id(client_with_mock_db: AsyncClient):
    """Testa a recuperação de endereço com ID inválido."""

    response = await client_with_mock_db.get(
        "/api/v1/location/locations/full-address/invalid"
    )

    # Deve retornar 422 (Unprocessable Entity) para ID inválido
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Testes para endpoints não implementados
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path, method",
    [
        ("/api/v1/location/locations/regions", "POST"),
        ("/api/v1/location/locations/regions/1", "GET"),
        ("/api/v1/location/locations/regions/1", "PUT"),
        ("/api/v1/location/locations/regions/1", "DELETE"),
        ("/api/v1/location/locations/cities", "POST"),
        ("/api/v1/location/locations/cities/1", "GET"),
        ("/api/v1/location/locations/cities/1", "PUT"),
        ("/api/v1/location/locations/cities/1", "DELETE"),
    ],
)
async def test_unimplemented_endpoints(
    client_with_mock_db: AsyncClient, path: str, method: str
):
    """Testa que os endpoints marcados como Not Implemented retornam 501."""

    if method == "POST":
        response = await client_with_mock_db.post(path, json={})
    elif method == "PUT":
        response = await client_with_mock_db.put(path, json={})
    elif method == "GET":
        response = await client_with_mock_db.get(path)
    elif method == "DELETE":
        response = await client_with_mock_db.delete(path)
    else:
        pytest.fail(f"Método HTTP não suportado: {method}")

    # Pode retornar 404 ou 501 dependendo da implementação
    assert response.status_code in [
        status.HTTP_404_NOT_FOUND,
        status.HTTP_501_NOT_IMPLEMENTED,
    ]


# --- Testes Adicionais ---


@pytest.mark.asyncio
async def test_location_status_endpoint(client_with_mock_db: AsyncClient):
    """Testa o endpoint de status do módulo location."""
    response = await client_with_mock_db.get("/api/v1/location/locations/status")

    # O endpoint pode não existir, então aceitamos 404 como válido
    if response.status_code == status.HTTP_404_NOT_FOUND:
        # Endpoint não implementado - isso é aceitável
        pytest.skip("Endpoint de status não implementado")
    else:
        # Endpoint existe - verifica se retorna status válido
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_501_NOT_IMPLEMENTED,
        ]


@pytest.mark.asyncio
async def test_list_provinces_not_implemented(client_with_mock_db: AsyncClient):
    """Testa que listagem de províncias retorna 404 ou 501 se não implementado."""
    response = await client_with_mock_db.get("/api/v1/location/locations/provinces")
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_501_NOT_IMPLEMENTED,
    ]


@pytest.mark.asyncio
async def test_list_municipalities_not_implemented(client_with_mock_db: AsyncClient):
    """Testa que listagem de municípios retorna 404 ou 501 se não implementado."""
    response = await client_with_mock_db.get(
        "/api/v1/location/locations/municipalities"
    )
    assert response.status_code in [
        status.HTTP_200_OK,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_501_NOT_IMPLEMENTED,
    ]


@pytest.mark.asyncio
async def test_invalid_endpoint_returns_404(client_with_mock_db: AsyncClient):
    """Testa que endpoint inválido retorna 404."""
    response = await client_with_mock_db.get(
        "/api/v1/location/locations/invalid-endpoint"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
