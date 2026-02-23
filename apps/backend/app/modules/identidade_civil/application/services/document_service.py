from app.core.observability import trace
"""
Serviço de Documentos - Módulo Identidade Civil

REFATORADO: Agora usa DocumentRepository em vez de acesso direto ao ORM.
"""
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identidade_civil.exceptions import NotFoundException, BusinessRuleException
from app.modules.identidade_civil.infrastructure.repositories.document_repository import DocumentRepository
from app.modules.identidade_civil.infrastructure.repositories.citizen_repository import CitizenRepository
from app.modules.identidade_civil.domain.models.document import Document, DocumentStatus
from app.core.constants import EntityStatus
from app.core.helpers import safe_get, safe_isoformat

logger = logging.getLogger("identidade_civil.service.document")


class DocumentService:
    """
    Serviço de Documentos refatorado para padrão Repository.
    Application layer NÃO conhece SQLAlchemy diretamente.
    """

    def __init__(self, session: AsyncSession):
        self.document_repo = DocumentRepository(session)
        self.citizen_repo = CitizenRepository(session)
        self.session = session

    @trace()
    async def _format_document_short(self, document: Document) -> Dict[str, Any]:
        """Formata documento para listagens (sem dados do cidadão)."""
        return {
            "id": str(document.id),
            "citizen_id": str(document.citizen_id),
            "document_type": document.document_type,
            "status": document.status,
            "request_date": safe_isoformat(document.request_date),
            "document_number": document.document_number,
        }

    @trace()
    async def _format_document_full(self, document: Document) -> Dict[str, Any]:
        """Formata documento com detalhes completos incluindo cidadão."""
        citizen = await self.citizen_repo.get_by_id(document.citizen_id)
        return {
            "id": str(document.id),
            "citizen_id": str(document.citizen_id),
            "citizen_name": safe_get(citizen, "full_name") if citizen else None,
            "citizen_bi": safe_get(citizen, "document_number") if citizen else None,
            "document_type": document.document_type,
            "status": document.status,
            "document_number": document.document_number,
            "request_date": safe_isoformat(document.request_date),
            "processing_date": safe_isoformat(document.processing_date),
            "completion_date": safe_isoformat(document.completion_date),
            "expiry_date": safe_isoformat(document.expiry_date),
            "notes": document.notes,
            "rejection_reason": document.rejection_reason,
        }

    @trace()
    async def list_documents(
        self, skip: int = 0, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Lista documentos com paginação."""
        documents = await self.document_repo.list_all(limit=limit, offset=skip)
        return [await self._format_document_short(doc) for doc in documents]

    @trace()
    async def get_by_id(self, document_id: str) -> Dict[str, Any]:
        """Recupera documento por ID com detalhes completos."""
        try:
            did = UUID(document_id)
        except ValueError:
            raise BusinessRuleException("ID de documento inválido")

        document = await self.document_repo.get_by_id(did)
        if not document:
            raise NotFoundException("Documento não encontrado")
        
        return await self._format_document_full(document)

    @trace()
    async def get_by_citizen(self, citizen_id: str) -> List[Dict[str, Any]]:
        """Lista documentos de um cidadão."""
        try:
            cid = UUID(citizen_id)
        except ValueError:
            raise BusinessRuleException("ID de cidadão inválido")

        documents = await self.document_repo.get_by_citizen(cid)
        return [await self._format_document_short(doc) for doc in documents]

    @trace()
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo pedido de documento."""
        try:
            citizen_id = UUID(data["citizen_id"])
        except (ValueError, KeyError):
            raise BusinessRuleException("ID do cidadão é obrigatório e deve ser válido")

        citizen = await self.citizen_repo.get_by_id(citizen_id)
        if not citizen:
            raise NotFoundException("Cidadão não encontrado")

        document = Document(
            id=uuid.uuid4(),
            citizen_id=citizen_id,
            document_type=data.get("document_type", "OTHER"),
            service_id=UUID(data["service_id"]) if data.get("service_id") else None,
            notes=data.get("notes"),
            status=EntityStatus.PENDING.value,
            request_date=datetime.utcnow(),
        )

        created = await self.document_repo.create(document)
        logger.info("Document request created", extra={
            "document_id": str(created.id),
            "citizen_id": str(citizen_id),
            "type": document.document_type
        })
        return await self._format_document_full(created)

    @trace()
    async def update_status(
        self, document_id: str, status: str, 
        notes: Optional[str] = None, 
        rejection_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Atualiza status de um documento."""
        try:
            did = UUID(document_id)
        except ValueError:
            raise BusinessRuleException("ID de documento inválido")

        document = await self.document_repo.get_by_id(did)
        if not document:
            raise NotFoundException("Documento não encontrado")

        document.status = status
        if status == DocumentStatus.PROCESSING.value:
            document.processing_date = datetime.utcnow()
        elif status in [DocumentStatus.APPROVED.value, DocumentStatus.REJECTED.value]:
            document.completion_date = datetime.utcnow()
            if rejection_reason:
                document.rejection_reason = rejection_reason

        if notes:
            document.notes = notes

        await self.session.commit()
        await self.session.refresh(document)
        
        logger.info("Document status updated", extra={
            "document_id": str(did),
            "new_status": status
        })
        return await self._format_document_full(document)
