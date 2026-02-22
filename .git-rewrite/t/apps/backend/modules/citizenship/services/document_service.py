"""Document upload and management service."""

from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.storage import save_uploaded_file
from modules.citizenship.models import AtualizacaoBIDocument


class DocumentService:
    @staticmethod
    async def upload_documents(
        db: Session, bi_id: int, files: List[UploadFile]
    ) -> List[str]:
        """Upload documents and save their references."""
        uploaded_paths = []
        for file in files:
            # Generate unique filename
            filename = f"docs/bi_{bi_id}/{file.filename}"

            # Save file
            path = await save_uploaded_file(file, filename)
            uploaded_paths.append(path)

            # Save document reference
            doc = AtualizacaoBIDocument(
                bi_update_id=bi_id,
                path=path,
                original_name=file.filename,
                content_type=file.content_type,
            )
            db.add(doc)

        db.commit()
        return uploaded_paths
