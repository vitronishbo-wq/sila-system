from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.ports.document_repository_port import DocumentRepositoryPort
from ...infrastructure.models.document import Document


class DocumentRepository(DocumentRepositoryPort):
    """Repositório REAL de documentos (Async)"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, citizen_id: UUID, document_type: str, file_path: str) -> Document:
        """Persiste documento real"""
        document = Document(
            citizen_id=citizen_id,
            document_type=document_type,
            file_path=file_path,
            uploaded_at=datetime.utcnow(),
            verified=False,
        )
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def get_by_citizen(self, citizen_id: UUID) -> list[Document]:
        """Busca documentos reais do cidadão"""
        result = await self.db.execute(select(Document).where(Document.citizen_id == citizen_id))
        return result.scalars().all()

    async def get_by_id(self, document_id: UUID) -> Document | None:
        """Busca documento específico"""
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        return result.scalar_one_or_none()

    async def verify(self, document_id: UUID, verified_by: UUID) -> Document | None:
        """Verifica documento real"""
        document = await self.get_by_id(document_id)
        if document:
            document.verified = True
            document.verified_at = datetime.utcnow()
            document.verified_by = verified_by
            await self.db.commit()
            await self.db.refresh(document)
        return document
