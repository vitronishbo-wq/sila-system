from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.citizen_document_model import CitizenDocumentModel, DocumentTypeEnum
from datetime import datetime

class CitizenDocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, citizen_id: UUID, doc_type: DocumentTypeEnum, file_path: str) -> CitizenDocumentModel:
        # Descobrir próxima versão
        result = await self.session.execute(
            select(CitizenDocumentModel)
            .where(CitizenDocumentModel.citizen_id == citizen_id)
            .where(CitizenDocumentModel.type == doc_type)
            .order_by(CitizenDocumentModel.version.desc())
        )
        last_doc = result.scalars().first()
        next_version = (last_doc.version + 1) if last_doc else 1
        doc = CitizenDocumentModel(
            citizen_id=citizen_id,
            type=doc_type,
            file_path=file_path,
            version=next_version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def get_latest(self, citizen_id: UUID, doc_type: DocumentTypeEnum) -> Optional[CitizenDocumentModel]:
        result = await self.session.execute(
            select(CitizenDocumentModel)
            .where(CitizenDocumentModel.citizen_id == citizen_id)
            .where(CitizenDocumentModel.type == doc_type)
            .order_by(CitizenDocumentModel.version.desc())
        )
        return result.scalars().first()

    async def list_versions(self, citizen_id: UUID, doc_type: DocumentTypeEnum) -> List[CitizenDocumentModel]:
        result = await self.session.execute(
            select(CitizenDocumentModel)
            .where(CitizenDocumentModel.citizen_id == citizen_id)
            .where(CitizenDocumentModel.type == doc_type)
            .order_by(CitizenDocumentModel.version.desc())
        )
        return result.scalars().all()
