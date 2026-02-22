"""
Tests for Document Endpoints.
"""
from datetime import datetime, timezone
import pytest
import shutil
from pathlib import Path
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from core.db.session import get_async_db
from core.security import get_current_active_user
from modules.documents.endpoints.router import router
from modules.documents.models.documents import Document
from modules.documents.schemas.documents import DocumentStatus
from modules.identity.models.user import User
from modules.location.models.region import Region  # Register Region
from modules.identity.models.identity import Identity  # Register Identity

# Setup a test app including the router
app = FastAPI()
app.include_router(router, prefix="/api/v1/documents")

# Mock User
MOCK_USER_ID = uuid4()
MOCK_USER = User(id=MOCK_USER_ID, email="test@example.com", is_active=True)

# Dependency Overrides


async def override_get_async_db():
    yield AsyncMock()


async def override_get_current_active_user():
    return MOCK_USER

app.dependency_overrides[get_async_db] = override_get_async_db
app.dependency_overrides[get_current_active_user] = override_get_current_active_user

# Temporary test directory
TEST_ENDPOINT_DIR = Path("media/test_endpoints")


@pytest.fixture(autouse=True)
def setup_teardown_storage():
    with patch("modules.documents.services.document_service.UPLOAD_DIR", TEST_ENDPOINT_DIR):
        TEST_ENDPOINT_DIR.mkdir(parents=True, exist_ok=True)
        yield
        if TEST_ENDPOINT_DIR.exists():
            shutil.rmtree(TEST_ENDPOINT_DIR)


@pytest.fixture
def mock_service():
    """Mock the DocumentService methods."""
    with patch("modules.documents.endpoints.router.DocumentService") as mock:
        mock.upload_document = AsyncMock()
        mock.get_document_by_id = AsyncMock()
        mock.list_documents = AsyncMock()
        mock.delete_document = AsyncMock()
        yield mock


def create_mock_doc(doc_id=None, owner_id=MOCK_USER_ID, title="Test Doc"):
    return Document(
        id=doc_id or uuid4(),
        title=title,
        filename="test.txt",
        file_path="media/test_endpoints/test.txt",
        file_type="txt",
        file_size=100,
        owner_id=owner_id,
        is_public=False,
        status=DocumentStatus.ACTIVE,
        created_at=datetime.now(timezone.utc)
    )


@pytest.mark.asyncio
async def test_upload_document_endpoint(mock_service):
    """Test upload endpoint."""
    mock_doc = create_mock_doc(title="Uploaded via API")
    mock_service.upload_document.return_value = mock_doc

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {"file": ("test.txt", b"content", "text/plain")}
        data = {"title": "Uploaded via API"}
        response = await ac.post("/api/v1/documents/upload", files=files, data=data)

    assert response.status_code == 201
    assert response.json()["title"] == "Uploaded via API"


@pytest.mark.asyncio
async def test_get_document_endpoint(mock_service):
    """Test get document endpoint."""
    doc_id = uuid4()
    mock_service.get_document_by_id.return_value = create_mock_doc(doc_id=doc_id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/documents/{doc_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(doc_id)


@pytest.mark.asyncio
async def test_get_document_forbidden(mock_service):
    """Test forbidden access."""
    doc_id = uuid4()
    mock_service.get_document_by_id.return_value = create_mock_doc(doc_id=doc_id, owner_id=uuid4())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/documents/{doc_id}")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_documents_endpoint(mock_service):
    """Test listing documents."""
    mock_service.list_documents.return_value = ([create_mock_doc()], 1)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/documents/")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_delete_document_endpoint(mock_service):
    """Test delete endpoint."""
    doc_id = uuid4()
    mock_service.get_document_by_id.return_value = create_mock_doc(doc_id=doc_id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete(f"/api/v1/documents/{doc_id}")

    assert response.status_code == 204
    mock_service.delete_document.assert_called_once()
