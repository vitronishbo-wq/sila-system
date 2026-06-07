"""Test attachments"""

from uuid import uuid4

import pytest

from apps.backend.app.modules.governance.service_requests.domain.models.attachment import Attachment


@pytest.mark.asyncio
async def test_create_attachment():
    """Test creating attachment"""
    request_id = uuid4()
    uploaded_by = uuid4()
    attachment = Attachment(
        request_id=request_id,
        filename="document.pdf",
        content_type="application/pdf",
        storage_url="s3://bucket/document.pdf",
        uploaded_by=uploaded_by,
        size_bytes=1024,
    )
    assert attachment.request_id == request_id
    assert attachment.filename == "document.pdf"
    assert attachment.size_bytes == 1024


@pytest.mark.asyncio
async def test_attachment_to_dict():
    """Test attachment serialization"""
    attachment = Attachment(
        request_id=uuid4(),
        filename="document.pdf",
        content_type="application/pdf",
        storage_url="s3://bucket/document.pdf",
        uploaded_by=uuid4(),
        size_bytes=1024,
    )
    data = attachment.to_dict()
    assert data["filename"] == "document.pdf"
    assert data["content_type"] == "application/pdf"
    assert data["size_bytes"] == 1024
