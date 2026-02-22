"""
Pydantic schemas for Documents module with UUID support.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, model_validator


# Enums
class DocumentCategory(str, Enum):
    CONTRATO = "contrato"
    CERTIDAO = "certidao"
    ATO_ADMINISTRATIVO = "ato_administrativo"
    PROCESSO = "processo"
    RELATORIO = "relatorio"
    COMPROVANTE = "comprovante"
    OUTROS = "outros"


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"
    DELETED = "deleted"


class DocumentType(str, Enum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
    TXT = "txt"
    JPG = "jpg"
    PNG = "png"
    ZIP = "zip"
    OUTROS = "outros"


# --- SHARED BASES ---

class DocumentBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: DocumentStatus = DocumentStatus.PENDING
    is_public: bool = False
    metadata_info: Optional[Dict[str, Any]] = None


class DocumentFolderBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    parent_id: Optional[UUID] = None


# --- FOLDER SCHEMAS ---

class DocumentFolderCreate(DocumentFolderBase):
    pass


class DocumentFolderRead(DocumentFolderBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --- DOCUMENT SCHEMAS ---

class DocumentCreate(DocumentBase):
    folder_id: Optional[UUID] = None
    # File is uploaded separately, this schema handles metadata creation


class DocumentRead(DocumentBase):
    id: UUID
    original_filename: Optional[str] = None
    file_type: str
    file_size: int
    mime_type: Optional[str] = None  # content_type
    status: DocumentStatus
    owner_id: UUID
    folder_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    # URLs prontas para o frontend — zero exposição de path interno
    thumbnail_url: Optional[str] = None
    ocr_url: Optional[str] = None
    download_url: Optional[str] = None
    highlight_snippet: Optional[str] = None

    @model_validator(mode="after")
    def build_urls(self) -> "DocumentRead":
        base = f"/api/v1/documents/{self.id}"
        self.download_url = f"{base}/download"
        if self.status == DocumentStatus.COMPLETED:
            self.thumbnail_url = f"{base}/thumbnail"
            self.ocr_url = f"{base}/ocr"
        return self

    folder: Optional[DocumentFolderRead] = None

    model_config = ConfigDict(from_attributes=True)


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DocumentStatus] = None
    folder_id: Optional[UUID] = None
    is_public: Optional[bool] = None
    metadata_info: Optional[Dict[str, Any]] = None


# --- VERSION SCHEMAS ---

class DocumentVersionRead(BaseModel):
    id: UUID
    document_id: UUID
    version_number: int
    changelog: Optional[str] = None
    uploaded_at: datetime
    uploaded_by_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DocumentSearchFilters(BaseModel):
    search_text: Optional[str] = None
    folder_id: Optional[UUID] = None
    status: Optional[DocumentStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
