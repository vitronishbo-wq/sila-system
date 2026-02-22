"""
Document Endpoints using FastAPI.
"""
import hashlib
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query, Request, Response
from fastapi.responses import FileResponse, Response
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db
from core.security import get_current_active_user, get_current_superuser
from modules.identity.models.user import User
from modules.documents.services.document_service import DocumentService
from modules.audit.service import log_action
from modules.documents.schemas.documents import (
    DocumentRead,
    DocumentCreate,
    DocumentSearchFilters,
    DocumentStatus,
    DocumentVersionRead
)
from modules.documents.models.documents import Document
from modules.documents.endpoints.realtime import router as realtime_router
from modules.documents.endpoints.search import router as search_router

router = APIRouter(tags=["documents"])
router.include_router(realtime_router)
router.include_router(search_router)


def get_document_service(db: AsyncSession = Depends(get_async_db)) -> DocumentService:
    return DocumentService(db)


def _get_etag(file_path: Path, last_modified: float) -> str:
    """ETag baseado no tamanho e timestamp do ficheiro."""
    return hashlib.md5(f"{file_path.stat().st_size}-{last_modified}".encode()).hexdigest()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_documents(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Upload multiple documents concurrently.
    """
    return await service.bulk_create_documents(files, current_user.id)


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Get document by ID.
    """
    document = await service.get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Simple access control: owner or public
    if not document.is_public and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this document")

    return document


@router.get("/me", response_model=List[DocumentRead])
async def list_my_documents(
    search: Optional[str] = Query(None),
    folder_id: Optional[UUID] = Query(None),
    status_filter: Optional[DocumentStatus] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Lista documentos do usuário autenticado.
    """
    filters = DocumentSearchFilters(
        search_text=search,
        folder_id=folder_id,
        status=status_filter
    )
    documents, total = await service.list_documents(
        filters, page, size, owner_id=current_user.id
    )
    return documents


@router.get("/", response_model=List[DocumentRead])
async def list_all_documents(
    search: Optional[str] = Query(None),
    folder_id: Optional[UUID] = Query(None),
    status_filter: Optional[DocumentStatus] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Lista todos os documentos (Acesso Admin necessário para ver tudo).
    """
    owner_id = current_user.id if current_user.administrative_level != "CENTRAL" else None
    filters = DocumentSearchFilters(
        search_text=search,
        folder_id=folder_id,
        status=status_filter
    )
    documents, total = await service.list_documents(
        filters, page, size, owner_id=owner_id
    )
    return documents


@router.get("/{document_id}/download")
async def download_document(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Download a document file (latest version).
    """
    document = await service.get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.is_public and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to download this document")

    await log_action(
        db=service.db,
        user_id=current_user.id,
        action="DOCUMENT_DOWNLOAD",
        resource_id=str(document.id),
        details={"filename": document.filename},
        request=Request
    )

    return FileResponse(
        path=document.file_path,
        filename=document.filename,
        media_type=document.mime_type or "application/octet-stream"
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Soft delete a document.
    """
    document = await service.get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")

    await service.delete_document(document_id)


@router.get("/admin/all")
async def admin_list_all_documents(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Lista todos os documentos do sistema (Acesso Admin).
    N+1 evitado com joinedload.
    """
    query = (
        select(Document)
        .options(joinedload(Document.folder))  # Exemplo de joinedload
        .order_by(Document.created_at.desc())
    )

    total = await db.scalar(select(func.count(Document.id)))
    result = await db.execute(query.offset(skip).limit(limit))

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [DocumentRead.model_validate(doc) for doc in result.scalars().all()]
    }


@router.post("/{document_id}/versions", response_model=DocumentVersionRead, status_code=status.HTTP_201_CREATED)
async def create_document_version(
    document_id: UUID,
    file: UploadFile = File(...),
    changelog: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    """
    Create a new version for an existing document.
    """
    return await service.create_new_version(
        document_id=document_id,
        file=file,
        uploaded_by_id=current_user.id,
        changelog=changelog
    )


@router.get("/{document_id}/versions", response_model=List[DocumentVersionRead])
async def list_document_versions(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_active_user),
):
    """
    List all versions of a document.
    """
    return await service.list_versions(document_id)


@router.get("/{document_id}/versions/{version_id}/download")
async def download_document_version(
    document_id: UUID,
    version_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Download a specific version of a document.
    """
    from modules.documents.models.documents import DocumentVersion

    version = await db.get(DocumentVersion, version_id)
    if not version or version.document_id != document_id:
        raise HTTPException(status_code=404, detail="Version not found")

    await log_action(
        db=db,
        user_id=current_user.id,
        action="DOCUMENT_VERSION_DOWNLOAD",
        resource_id=str(document_id),
        details={"version_id": str(version_id)},
        request=Request
    )

    return FileResponse(version.file_path)


@router.get("/{document_id}/thumbnail")
async def get_thumbnail(
    document_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """Serve thumbnail com Cache-Control e ETag."""
    from modules.documents.models.documents import Document
    doc = await db.get(Document, document_id)
    if not doc or (doc.owner_id != current_user.id and current_user.administrative_level != "CENTRAL"):
        raise HTTPException(status_code=403, detail="Acesso negado")

    if doc.status != "completed" or not doc.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail não disponível")

    thumb_path = Path(doc.thumbnail_path)
    if not thumb_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    last_mod = doc.updated_at or doc.created_at
    etag = f'"{_get_etag(thumb_path, last_mod.timestamp())}"'

    # Check ETag
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match == etag:
        return Response(status_code=304)

    headers = {
        "Cache-Control": "public, max-age=31536000, immutable",
        "ETag": etag,
        "Last-Modified": last_mod.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

    return FileResponse(
        path=thumb_path,
        media_type="image/png",
        filename=f"thumb_{doc.id}.png",
        headers=headers,
    )


@router.get("/{document_id}/ocr")
async def get_ocr_text(
    document_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    """Serve texto OCR com Cache-Control e ETag."""
    from modules.documents.models.documents import Document
    doc = await db.get(Document, document_id)
    if not doc or (doc.owner_id != current_user.id and current_user.administrative_level != "CENTRAL"):
        raise HTTPException(status_code=403, detail="Acesso negado")

    if doc.status != "completed" or not doc.ocr_text_path:
        raise HTTPException(status_code=404, detail="Texto OCR não disponível")

    ocr_path = Path(doc.ocr_text_path)
    if not ocr_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    last_mod = doc.updated_at or doc.created_at
    etag = f'"{_get_etag(ocr_path, last_mod.timestamp())}"'

    # Check ETag
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match == etag:
        return Response(status_code=304)

    headers = {
        "Cache-Control": "public, max-age=31536000, immutable",
        "ETag": etag,
        "Last-Modified": last_mod.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

    return FileResponse(
        path=ocr_path,
        media_type="text/plain",
        filename=f"ocr_{doc.id}.txt",
        headers=headers,
    )
