import uuid
from datetime import datetime

from apps.backend.app.infrastructure.models.citizen_document_model import CitizenDocumentModel, DocumentTypeEnum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/sila_system"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed():
    async with SessionLocal() as session:
        doc1 = CitizenDocumentModel(
            id=uuid.uuid4(),
            citizen_id=uuid.uuid4(),  # Use a real citizen_id in real tests
            type=DocumentTypeEnum.BI,
            file_path="/tmp/citizen_documents/test_bi.pdf",
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        doc2 = CitizenDocumentModel(
            id=uuid.uuid4(),
            citizen_id=uuid.uuid4(),
            type=DocumentTypeEnum.PASSPORT,
            file_path="/tmp/citizen_documents/test_passport.pdf",
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add_all([doc1, doc2])
        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed())
