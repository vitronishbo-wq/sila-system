"""Unit tests for DocumentService with isolated dependencies."""

import types
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import UploadFile

from apps.backend.app.modules.documents.application.schemas.documents import (
    DocumentCreate,
    DocumentStatus,
)
from apps.backend.app.modules.documents.application.services.document_service import (
    DocumentService,
)

TEST_UPLOAD_DIR = Path("media/test_documents")


class FakeDocument:
    """Lightweight stand-in for ORM Document model."""

    _next_id = 1

    def __init__(self, **kwargs):
        self.id = FakeDocument._next_id
        FakeDocument._next_id += 1
        self.current_version_id = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class FakeDocumentVersion:
    """Lightweight stand-in for ORM DocumentVersion model."""

    _next_id = 1

    def __init__(self, **kwargs):
        self.id = FakeDocumentVersion._next_id
        FakeDocumentVersion._next_id += 1
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    session.execute = AsyncMock(return_value=mock_result)
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session._mock_scalars = mock_scalars
    return session


@pytest.fixture(autouse=True)
def patch_upload_dir():
    with patch(
        "apps.backend.app.modules.documents.application.services.document_service.UPLOAD_DIR",
        TEST_UPLOAD_DIR,
    ):
        yield


@pytest.mark.asyncio
async def test_create_single_document_success(mock_db_session):
    owner_id = uuid4()
    file = UploadFile(
        filename="test.txt",
        file=BytesIO(b"abc"),
        headers={"content-type": "text/plain"},
    )
    metadata = DocumentCreate(title="Test Doc", description="A test document")
    service = DocumentService(mock_db_session)

    fake_ocr_task = SimpleNamespace(delay=MagicMock())
    fake_tasks_module = types.SimpleNamespace(process_document_ocr_task=fake_ocr_task)

    with (
        patch.object(
            service,
            "_save_file",
            AsyncMock(return_value=("media/test_documents/temp/test.txt", 3, "checksum")),
        ),
        patch(
            "apps.backend.app.modules.documents.application.services.document_service.Document",
            FakeDocument,
        ),
        patch(
            "apps.backend.app.modules.documents.application.services.document_service.DocumentVersion",
            FakeDocumentVersion,
        ),
        patch.dict(
            "sys.modules",
            {"apps.backend.app.modules.documents.tasks": fake_tasks_module},
        ),
    ):
        result = await service.create_single_document(
            file=file, metadata=metadata, owner_id=owner_id
        )

    assert result.title == "Test Doc"
    assert result.owner_id == owner_id
    assert result.status == DocumentStatus.PENDING
    assert result.current_version_id is not None
    assert mock_db_session.add.call_count == 2
    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once()
    fake_ocr_task.delay.assert_called_once()


@pytest.mark.asyncio
async def test_get_document_by_id(mock_db_session):
    doc_id = uuid4()
    expected = SimpleNamespace(id=doc_id, title="Found Doc")
    mock_db_session._mock_scalars.first.return_value = expected
    service = DocumentService(mock_db_session)

    result = await service.get_document_by_id(doc_id)

    assert result is expected
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_document_soft(mock_db_session):
    doc_id = uuid4()
    mock_doc = SimpleNamespace(id=doc_id, title="To Delete", status=DocumentStatus.PENDING)
    service = DocumentService(mock_db_session)
    service.get_document_by_id = AsyncMock(return_value=mock_doc)

    success = await service.delete_document(doc_id, hard_delete=False)

    assert success is True
    assert mock_doc.status == DocumentStatus.DELETED
    mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_document_not_found(mock_db_session):
    service = DocumentService(mock_db_session)
    service.get_document_by_id = AsyncMock(return_value=None)

    success = await service.delete_document(uuid4())

    assert success is False
    mock_db_session.commit.assert_not_called()
