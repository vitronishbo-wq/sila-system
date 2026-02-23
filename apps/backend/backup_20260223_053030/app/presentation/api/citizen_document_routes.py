from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from uuid import UUID
from typing import List
from ...infrastructure.db.session import get_session
from ...infrastructure.repositories.citizen_document_repository import CitizenDocumentRepository
from ...infrastructure.models.citizen_document_model import DocumentTypeEnum
from ..schemas.citizen_document_schema import CitizenDocumentReadSchema
from sqlalchemy.ext.asyncio import AsyncSession
import os

router = APIRouter(prefix="/citizen-documents", tags=["citizen-documents"])

UPLOAD_DIR = "/tmp/citizen_documents"  # Ajuste para produção
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_repo(session: AsyncSession = Depends(get_session)):
    return CitizenDocumentRepository(session)

@router.post("/upload", response_model=CitizenDocumentReadSchema)
async def upload_document(
    citizen_id: UUID = Form(...),
    doc_type: DocumentTypeEnum = Form(...),
    file: UploadFile = File(...),
    repo: CitizenDocumentRepository = Depends(get_repo)
):
    # Salvar arquivo
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{citizen_id}_{doc_type}{ext}")
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # Versionamento automático
    doc = await repo.add(citizen_id, doc_type, file_path)
    return CitizenDocumentReadSchema.from_orm(doc)

@router.get("/latest/{citizen_id}/{doc_type}", response_model=CitizenDocumentReadSchema)
async def get_latest_document(
    citizen_id: UUID,
    doc_type: DocumentTypeEnum,
    repo: CitizenDocumentRepository = Depends(get_repo)
):
    doc = await repo.get_latest(citizen_id, doc_type)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return CitizenDocumentReadSchema.from_orm(doc)

@router.get("/versions/{citizen_id}/{doc_type}", response_model=List[CitizenDocumentReadSchema])
async def list_document_versions(
    citizen_id: UUID,
    doc_type: DocumentTypeEnum,
    repo: CitizenDocumentRepository = Depends(get_repo)
):
    docs = await repo.list_versions(citizen_id, doc_type)
    return [CitizenDocumentReadSchema.from_orm(d) for d in docs]
