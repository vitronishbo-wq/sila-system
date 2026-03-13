from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from apps.backend.app.modules.documents.application.schemas.documents import (
    DocumentCreate,
    DocumentStatus,
)

UPLOAD_DIR = Path("media/documents")


class Document:
    def __init__(self, **kwargs: Any):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DocumentVersion:
    def __init__(self, **kwargs: Any):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DocumentService:
    def __init__(self, db):
        self.db = db

    async def _save_file(self, file: UploadFile) -> tuple[str, int, str]:
        data = await file.read()
        file.file.seek(0)
        checksum = hashlib.sha256(data).hexdigest()
        relative_path = UPLOAD_DIR / file.filename
        return str(relative_path), len(data), checksum

    async def create_single_document(
        self,
        file: UploadFile,
        metadata: DocumentCreate,
        owner_id,
    ):
        file_path, size_bytes, checksum = await self._save_file(file)
        document = Document(
            title=metadata.title,
            description=metadata.description,
            owner_id=owner_id,
            status=DocumentStatus.PENDING,
        )
        self.db.add(document)
        await self.db.flush()

        version = DocumentVersion(
            document_id=getattr(document, "id", None),
            file_path=file_path,
            file_size=size_bytes,
            checksum=checksum,
            content_type=file.content_type,
        )
        self.db.add(version)
        await self.db.flush()

        if hasattr(document, "current_version_id"):
            document.current_version_id = getattr(version, "id", None)

        await self.db.commit()
        await self.db.refresh(document)

        try:
            from apps.backend.app.modules.documents.tasks import process_document_ocr_task

            process_document_ocr_task.delay(getattr(document, "id", None))
        except Exception:
            pass

        return document

    async def get_document_by_id(self, document_id):
        result = await self.db.execute(("document_by_id", document_id))
        return result.scalars().first()

    async def delete_document(self, document_id, hard_delete: bool = False) -> bool:
        document = await self.get_document_by_id(document_id)
        if not document:
            return False

        if hard_delete:
            await self.db.delete(document)
        else:
            document.status = DocumentStatus.DELETED

        await self.db.commit()
        return True
