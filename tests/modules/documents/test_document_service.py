"""
Tests for DocumentService.
"""

import os
import shutil
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from pathlib import Path
from io import BytesIO

from fastapi import UploadFile

from modules.documents.services.document_service import DocumentService
from modules.documents.models.documents import Document
from modules.documents.schemas.documents import DocumentCreate, DocumentSearchFilters, DocumentStatus
from modules.identity.models.user import User  # Register User model
from modules.location.models.region import Region  # Register Region
from modules.identity.models.identity import Identity  # Register Identity

# Temporary test directory
TEST_UPLOAD_DIR = Path("media/test_documents")


@pytest.fixture(autouse=True)
def setup_teardown_storage():
    """Setup and teardown test storage."""
    # Patch the UPLOAD_DIR in the service
    with patch("modules.documents.services.document_service.UPLOAD_DIR", TEST_UPLOAD_DIR):
        TEST_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        yield
        if TEST_UPLOAD_DIR.exists():
            shutil.rmtree(TEST_UPLOAD_DIR)


@pytest.fixture
def mock_db_session():
    """Mock async database session."""
    session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    # Setup execute to return the mock result
    session.execute = AsyncMock(return_value=mock_result)
    session.add = MagicMock()

    # Store helpers
    session._mock_scalars = mock_scalars
    return session


@pytest.mark.asyncio
async def test_upload_document_success(mock_db_session):
    """Test successful document upload."""
    owner_id = uuid4()

    # Prepare create data
    doc_create = DocumentCreate(
        title="Test Doc",
        description="A test document",
        is_public=False
    )

    # Prepare mock file
    file_content = b"Content of the test file"
    file = UploadFile(filename="test.txt", file=BytesIO(
        file_content), headers={"content-type": "text/plain"})

    # Execute
    result = await DocumentService.upload_document(
        db=mock_db_session,
        file=file,
        metadata=doc_create,
        owner_id=owner_id
    )

    # Verify DB calls
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited()
    mock_db_session.refresh.assert_awaited()

    # Verify file saved
    assert result.title == "Test Doc"
    assert result.owner_id == owner_id
    assert os.path.exists(result.file_path)

    # Verify content
    with open(result.file_path, "rb") as f:
        saved_content = f.read()
        assert saved_content == file_content


@pytest.mark.asyncio
async def test_get_document_by_id(mock_db_session):
    """Test retrieving document by ID."""
    doc_id = uuid4()
    mock_doc = Document(id=doc_id, title="Found Doc")

    mock_db_session._mock_scalars.first.return_value = mock_doc

    result = await DocumentService.get_document_by_id(mock_db_session, doc_id)

    assert result.id == doc_id
    assert result.title == "Found Doc"


@pytest.mark.asyncio
async def test_delete_document_soft(mock_db_session):
    """Test soft deletion."""
    doc_id = uuid4()
    mock_doc = Document(id=doc_id, title="To Delete", status="active", file_path="dummy/path")

    mock_db_session._mock_scalars.first.return_value = mock_doc

    success = await DocumentService.delete_document(mock_db_session, doc_id, hard_delete=False)

    assert success is True
    assert mock_doc.status == DocumentStatus.DELETED
    mock_db_session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_delete_document_not_found(mock_db_session):
    """Test delete when doc not found."""
    mock_db_session._mock_scalars.first.return_value = None

    success = await DocumentService.delete_document(mock_db_session, uuid4())

    assert success is False
    mock_db_session.commit.assert_not_called()
