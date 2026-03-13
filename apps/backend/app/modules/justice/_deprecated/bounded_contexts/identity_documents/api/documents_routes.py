from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.models.iam_user import IamUser as User
from app.modules.justice.bounded_contexts.application.services.document_service import DocumentService
from app.modules.justice.bounded_contexts.infrastructure.repositories.document_repository import DocumentRepository
from app.core.bridges.citizen_repository_bridge import CitizenRepository
router = APIRouter(prefix='/documents', tags=['Documents'])

class DocumentCreate(BaseModel):
    citizen_id: str
    document_type: str
    service_id: Optional[str] = None
    notes: Optional[str] = None

class DocumentStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
    rejection_reason: Optional[str] = None

def get_document_service(db: AsyncSession=Depends(get_db)) -> DocumentService:
    """Provedor de dependência para DocumentService."""
    document_repo = DocumentRepository(db)
    citizen_repo = CitizenRepository(db)
    return DocumentService(session=db, document_repo=document_repo, citizen_repo=citizen_repo)

@router.get('/')
async def list_documents(skip: int=Query(0, ge=0), limit: int=Query(20, ge=1, le=100), current_user: User=Depends(get_current_user), service: DocumentService=Depends(get_document_service)):
    """Lista documentos com paginação."""
    return await service.list_documents(skip=skip, limit=limit)

@router.get('/{document_id}')
async def get_document(document_id: str, current_user: User=Depends(get_current_user), service: DocumentService=Depends(get_document_service)):
    """Obtém detalhes de um documento."""
    return await service.get_by_id(document_id)

@router.get('/citizen/{citizen_id}')
async def get_documents_by_citizen(citizen_id: str, current_user: User=Depends(get_current_user), service: DocumentService=Depends(get_document_service)):
    """Lista documentos de um cidadão."""
    return await service.get_by_citizen(citizen_id)

@router.post('/')
async def create_document(data: DocumentCreate, current_user: User=Depends(get_current_user), service: DocumentService=Depends(get_document_service)):
    """Cria solicitação de documento."""
    result = await service.create(data.model_dump())
    return {'id': result['id'], 'message': 'Solicitação de documento criada com sucesso'}

@router.patch('/{document_id}/status')
async def update_document_status(document_id: str, data: DocumentStatusUpdate, current_user: User=Depends(get_current_user), service: DocumentService=Depends(get_document_service)):
    """Atualiza status de um documento."""
    result = await service.update_status(document_id, data.status, data.notes, data.rejection_reason)
    return {'id': result['id'], 'new_status': result['status'], 'message': 'Estado atualizado com sucesso'}