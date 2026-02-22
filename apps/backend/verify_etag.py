import asyncio
from uuid import uuid4
from pathlib import Path
from sqlalchemy import select
from core.db.session import get_async_db
from modules.identity.models.user import User
from modules.documents.models.documents import Document, DocumentStatus
from datetime import datetime

async def verify():
    async for db in get_async_db():
        # 1. Ensure a user exists
        result = await db.execute(select(User).limit(1))
        user = result.scalars().first()
        if not user:
            user = User(
                id=uuid4(),
                email="test@example.com",
                full_name="Test User",
                hashed_password="...",
                is_active=True,
                administrative_level="CENTRAL"
            )
            db.add(user)
            await db.flush()
        
        # 2. Create a test document
        doc_id = uuid4()
        thumb_path = f"media/test_thumb_{doc_id}.png"
        ocr_path = f"media/test_ocr_{doc_id}.txt"
        
        # Ensure media dir exists
        Path("media").mkdir(exist_ok=True)
        with open(thumb_path, "wb") as f:
            f.write(b"fake image data")
        with open(ocr_path, "w") as f:
            f.write("fake ocr text")
            
        doc = Document(
            id=doc_id,
            title="Test ETag",
            filename="test.pdf",
            file_path="media/test.pdf",
            file_type="pdf",
            file_size=100,
            owner_id=user.id,
            status=DocumentStatus.COMPLETED,
            thumbnail_path=thumb_path,
            ocr_text_path=ocr_path,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(doc)
        await db.commit()
        print(f"CREATED_DOC_ID={doc_id}")
        break

if __name__ == "__main__":
    asyncio.run(verify())
