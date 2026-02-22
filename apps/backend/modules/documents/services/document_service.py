import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from uuid import UUID, uuid4

from fastapi import UploadFile, HTTPException
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession

from modules.notifications.services.notification_service import (
    NotificationService, NotificationType
)
from modules.documents.models.documents import (
    Document, DocumentFolder, DocumentVersion
)
from modules.documents.schemas.documents import (
    DocumentCreate,
    DocumentRead,
    DocumentSearchFilters,
    DocumentUpdate,
    DocumentStatus
)

# Configuration for file storage
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "media/documents"))
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.jpg', '.png'}
TEMP_UPLOAD_DIR = UPLOAD_DIR / "temp"


class DocumentService:
    """Service for managing documents with versioning."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_service = NotificationService(db)

    def _get_storage_path(self, filename: str, is_temp: bool = False) -> Path:
        """Generate storage path based on date or temp folder."""
        if is_temp:
            path = TEMP_UPLOAD_DIR
        else:
            today = datetime.now()
            path = UPLOAD_DIR / str(today.year) / str(today.month)

        path.mkdir(parents=True, exist_ok=True)
        # Unique filename to prevent overwrite
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid4().hex}{ext}"
        return path / unique_name

    async def _save_file(self, file: UploadFile, is_temp: bool = False) -> Tuple[str, int, str]:
        """Save file to storage and return path, size, and checksum."""
        file_path = self._get_storage_path(file.filename, is_temp=is_temp)
        sha256_hash = hashlib.sha256()

        try:
            with open(file_path, "wb") as buffer:
                while content := await file.read(1024 * 1024):  # 1MB chunks
                    buffer.write(content)
                    sha256_hash.update(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
        finally:
            await file.seek(0)

        file_size = file_path.stat().st_size
        checksum = sha256_hash.hexdigest()

        # Ensure correct permissions for Celery worker
        try:
            file_path.chmod(0o666)
        except Exception:
            pass

        return str(file_path), file_size, checksum

    async def create_single_document(
        self,
        file: UploadFile,
        metadata: DocumentCreate,
        owner_id: UUID
    ) -> Document:
        """
        Upload a file and create document record with version 1.
        """
        # Validate extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            # For now just log or allow "other", but ideally validate
            pass

        # Save file to temp for processing
        file_path, file_size, checksum = await self._save_file(file, is_temp=True)

        # Create DB record with PENDING status
        db_document = Document(
            title=metadata.title or file.filename,
            description=metadata.description,
            filename=os.path.basename(file_path),
            original_filename=file.filename,
            file_path=file_path,
            file_type=ext.replace('.', ''),
            file_size=file_size,
            mime_type=file.content_type,
            content_type=file.content_type,
            checksum=checksum,
            owner_id=owner_id,
            folder_id=metadata.folder_id,
            status=DocumentStatus.PENDING,
            is_public=metadata.is_public,
            metadata_info=metadata.metadata_info
        )

        self.db.add(db_document)
        await self.db.flush()

        # Trigger processing task
        from modules.documents.tasks import process_document_ocr_task
        process_document_ocr_task.delay(str(db_document.id), file_path)

        # Create first version
        version = DocumentVersion(
            document_id=db_document.id,
            version_number=1,
            file_path=file_path,
            file_size=file_size,
            changelog="Versão inicial",
            uploaded_by_id=owner_id,
        )
        self.db.add(version)
        await self.db.flush()

        # Update current version
        db_document.current_version_id = version.id

        await self.db.commit()
        await self.db.refresh(db_document)

        return db_document

    async def bulk_create_documents(
        self,
        files: List[UploadFile],
        owner_id: UUID,
        metadata: Optional[DocumentCreate] = None
    ) -> Dict[str, Any]:
        """Create multiple documents concurrently."""
        import asyncio
        if not metadata:
            metadata = DocumentCreate(title="")

        tasks = []
        for file in files:
            tasks.append(self.create_single_document(file, metadata, owner_id))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        errors = [r for r in results if isinstance(r, Exception)]
        if errors:
            # Log errors if needed
            raise HTTPException(
                status_code=400,
                detail=f"{len(errors)} erro(s) no upload: {[str(e) for e in errors]}"
            )

        return {"uploaded": len(files) - len(errors)}

    async def create_new_version(
        self,
        document_id: UUID,
        file: UploadFile,
        uploaded_by_id: UUID,
        changelog: str = None,
    ) -> DocumentVersion:
        """Create a new version for an existing document."""
        # Busca documento
        document = await self.db.get(Document, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Salva novo arquivo
        file_path, file_size, checksum = await self._save_file(file)

        # Conta versão atual
        result = await self.db.execute(
            select(func.count(DocumentVersion.id)).where(DocumentVersion.document_id == document_id)
        )
        version_number = result.scalar() + 1

        # Cria nova versão
        new_version = DocumentVersion(
            document_id=document_id,
            version_number=version_number,
            file_path=file_path,
            file_size=file_size,
            changelog=changelog or "Nova versão enviada",
            uploaded_by_id=uploaded_by_id,
        )
        self.db.add(new_version)
        await self.db.flush()

        # Atualiza current_version no documento principal
        document.current_version_id = new_version.id
        document.updated_at = datetime.utcnow()
        # Update main fields to reflect latest version
        document.file_path = file_path
        document.file_size = file_size
        document.checksum = checksum
        document.filename = file.filename

        await self.db.commit()
        await self.db.refresh(new_version)

        # Notifica owner
        try:
            from modules.identity.models.user import User
            uploaded_by = await self.db.get(User, uploaded_by_id)
            uploader_name = uploaded_by.full_name if uploaded_by else "Um utilizador"

            await self.notification_service.create_and_queue(
                user_id=document.owner_id,
                type_=NotificationType.DOCUMENT_SHARED,
                title="Nova versão do documento",
                message=f"O documento '{document.title}' foi atualizado para a versão {version_number} por {uploader_name}.",
                context={
                    # This is a bit confusing in the context of the notification, but following user's logic
                    "user_name": uploader_name,
                    "document_name": document.title,
                    "date": datetime.utcnow().strftime("%d/%m/%Y"),
                    "document_url": f"/documents/{document.id}"  # Placeholder
                },
                template_name="document_shared.html",
                metadata={"document_id": str(document.id), "version": version_number},
            )
        except Exception as e:
            # Don't fail the whole operation if notification fails
            print(f"Failed to send notification: {e}")

        return new_version

    async def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        query = select(Document).where(Document.id == document_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list_documents(
        self,
        filters: DocumentSearchFilters,
        page: int = 1,
        size: int = 20,
        owner_id: Optional[UUID] = None
    ) -> Tuple[List[Document], int]:
        """List documents with filters."""
        query = select(Document)

        if owner_id:
            query = query.where(Document.owner_id == owner_id)

        if filters.folder_id:
            query = query.where(Document.folder_id == filters.folder_id)

        if filters.search_text:
            query = query.where(Document.title.ilike(f"%{filters.search_text}%"))

        if filters.status:
            query = query.where(Document.status == filters.status)

        # Count total (simplified)
        count_query = select(func.count(Document.id))
        # ... repeat filters if needed for count, but for page-based it's better

        # Pagination
        query = query.order_by(desc(Document.created_at)).offset((page - 1) * size).limit(size)

        result = await self.db.execute(query)
        documents = result.scalars().all()

        return documents, len(documents)  # Placeholder for real count

    async def list_versions(self, document_id: UUID) -> List[DocumentVersion]:
        """List versions for a document."""
        result = await self.db.execute(
            select(DocumentVersion)
            .where(DocumentVersion.document_id == document_id)
            .order_by(desc(DocumentVersion.version_number))
        )
        return result.scalars().all()

    async def delete_document(self, document_id: UUID, hard_delete: bool = False) -> bool:
        """Delete a document (soft delete by default)."""
        document = await self.get_document_by_id(document_id)
        if not document:
            return False

        if hard_delete:
            # Remove file
            try:
                os.remove(document.file_path)
            except OSError:
                pass
            await self.db.delete(document)
        else:
            document.status = DocumentStatus.DELETED

        await self.db.commit()
        return True
