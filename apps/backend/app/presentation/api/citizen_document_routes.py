import os
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.db.session import get_session
from ...infrastructure.models.citizen_document_model import DocumentTypeEnum
from ...infrastructure.repositories.citizen_document_repository import CitizenDocumentRepository
from ..schemas.citizen_document_schema import CitizenDocumentReadSchema

router = APIRouter(prefix="/citizen-documents", tags=["citizen-documents"])
UPLOAD_DIR = "/tmp/citizen_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

session_dep = Depends(get_session)
citizen_id_form = Form(...)
doc_type_form = Form(...)
file_form = File(...)


async def get_repo(session: AsyncSession = session_dep):
    return CitizenDocumentRepository(session)

repo_dep = Depends(get_repo)


@router.post("/upload", response_model=CitizenDocumentReadSchema)
async def upload_document(
    citizen_id: UUID = citizen_id_form,
    doc_type: DocumentTypeEnum = doc_type_form,
    file: UploadFile = file_form,
    repo: CitizenDocumentRepository = repo_dep,
):
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{citizen_id}_{doc_type}{ext}")
    with open(file_path, "wb") as f:
        f.write(await file.read())
    doc = await repo.add(citizen_id, doc_type, file_path)
    return CitizenDocumentReadSchema.from_orm(doc)


@router.get("/latest/{citizen_id}/{doc_type}", response_model=CitizenDocumentReadSchema)
async def get_latest_document(
    citizen_id: UUID,
    doc_type: DocumentTypeEnum,
    repo: CitizenDocumentRepository = repo_dep,
):
    doc = await repo.get_latest(citizen_id, doc_type)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return CitizenDocumentReadSchema.from_orm(doc)


@router.get("/versions/{citizen_id}/{doc_type}", response_model=list[CitizenDocumentReadSchema])
async def list_document_versions(
    citizen_id: UUID,
    doc_type: DocumentTypeEnum,
    repo: CitizenDocumentRepository = repo_dep,
):
    docs = await repo.list_versions(citizen_id, doc_type)
    return [CitizenDocumentReadSchema.from_orm(d) for d in docs]
