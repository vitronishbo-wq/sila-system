import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.document_file import DocumentFile
from ..infrastructure.storage.local_storage import LocalStorage
from app.core.audit import audit_log

class DocumentService:
    """
    Serviço Transversal de Gestão de Documentos e Ficheiros.
    Controla o ciclo de vida de anexos biográficos e administrativos.
    """

    def __init__(self, db: AsyncSession, storage: Optional[LocalStorage] = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
        self.storage = storage or LocalStorage()

    async def upload_document(
        self,
        owner_id: uuid.UUID,
        owner_type: str,
        category: str,
        file_name: str,
        content: bytes,
        content_type: str = None,
        meta_data: dict = None
    ) -> DocumentFile:
        """
        Realiza o upload real de um ficheiro e regista a sua existência no banco.
        """
        # 1. Guardar no Storage
        sub_folder = f"{owner_type}/{owner_id}"
        file_path = self.storage.save_file(content, sub_folder, file_name)
        
        # 2. Registar no Banco
        doc_file = DocumentFile(
            id=uuid.uuid4(),
            owner_id=owner_id,
            owner_type=owner_type,
            category=category,
            file_name=file_name,
            file_path=file_path,
            content_type=content_type,
            file_size=len(content),
            meta_data=meta_data
        )
        
        self.db.add(doc_file)
        await self.db.flush()
        
        # 3. Auditoria
        await audit_log(
            action="FILE_UPLOADED",
            actor_id="SYSTEM", # Em produção seria o user ID do token
            resource_id=str(doc_file.id),
            resource_type="DocumentFile",
            new_value={
                "category": category,
                "owner_id": str(owner_id),
                "file_name": file_name
            },
            db=self.db
        )
        
        return doc_file

    async def get_owner_documents(self, owner_id: uuid.UUID) -> List[DocumentFile]:
        """Lista todos os anexos de um dono (Cidadão ou Request)."""
        result = await self.db.execute(
            select(DocumentFile).where(DocumentFile.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def has_document_category(self, owner_id: uuid.UUID, category: str) -> bool:
        """Verifica se um dono possui pelo menos um documento de uma categoria específica."""
        result = await self.db.execute(
            select(DocumentFile).where(
                DocumentFile.owner_id == owner_id,
                DocumentFile.category == category
            )
        )
        return result.scalar_one_or_none() is not None

    async def delete_document(self, document_id: uuid.UUID):
        """Remove registo e ficheiro físico."""
        res = await self.db.execute(select(DocumentFile).where(DocumentFile.id == document_id))
        doc = res.scalar_one_or_none()
        
        if doc:
            self.storage.delete_file(doc.file_path)
            await self.db.delete(doc)
            await self.db.flush()
            
            await audit_log(
                action="FILE_DELETED",
                actor_id="SYSTEM",
                resource_id=str(document_id),
                resource_type="DocumentFile",
                db=self.db
            )
