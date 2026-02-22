"""
Schemas Pydantic para o módulo de Documentos.

Define estruturas de dados para gestão documental, incluindo:
- Upload e armazenamento de documentos
- Categorização e metadados
- Controle de acesso e permissões
- Busca avançada e filtros
- Auditoria e versionamento
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Enums para categorização e controle
class DocumentCategory(str, Enum):
    """Categorias de documentos."""

    CONTRATO = "contrato"
    CERTIDAO = "certidao"
    ATO_ADMINISTRATIVO = "ato_administrativo"
    PROCESSO = "processo"
    RELATORIO = "relatorio"
    COMPROVANTE = "comprovante"
    OUTROS = "outros"


class DocumentStatus(str, Enum):
    """Status possíveis para documentos."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    PENDING_REVIEW = "pending_review"
    EXPIRED = "expired"


class DocumentType(str, Enum):
    """Tipos de arquivo suportados."""

    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
    TXT = "txt"
    RTF = "rtf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    TIFF = "tiff"
    ZIP = "zip"
    RAR = "rar"
    OUTROS = "outros"


class PermissionLevel(str, Enum):
    """Níveis de permissão para documentos."""

    PUBLIC = "public"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"


class DocumentBase(BaseModel):
    """Schema base para documentos."""

    title: str = Field(
        ..., min_length=1, max_length=255, description="Título do documento"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Descrição detalhada"
    )
    category: DocumentCategory = Field(..., description="Categoria do documento")
    document_type: DocumentType = Field(..., description="Tipo de arquivo")
    tags: List[str] = Field(default_factory=list, description="Tags para organização")
    is_public: bool = Field(False, description="Se o documento é público")
    permission_level: PermissionLevel = Field(
        PermissionLevel.RESTRICTED, description="Nível de permissão"
    )


class DocumentCreate(DocumentBase):
    """Schema para criação de documentos."""

    file_path: Optional[str] = Field(None, description="Caminho do arquivo no storage")
    file_size: Optional[int] = Field(
        None, ge=0, description="Tamanho do arquivo em bytes"
    )
    mime_type: Optional[str] = Field(None, description="MIME type do arquivo")
    checksum: Optional[str] = Field(
        None, description="Hash MD5/SHA256 para verificação"
    )


class DocumentUpload(BaseModel):
    """Schema específico para upload de documentos."""

    file: Any = Field(..., description="Arquivo a ser enviado")
    title: str = Field(
        ..., min_length=1, max_length=255, description="Título do documento"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Descrição detalhada"
    )
    category: DocumentCategory = Field(..., description="Categoria do documento")
    tags: List[str] = Field(default_factory=list, description="Tags para organização")
    is_public: bool = Field(False, description="Se o documento é público")
    permission_level: PermissionLevel = Field(
        PermissionLevel.RESTRICTED, description="Nível de permissão"
    )
    parent_folder_id: Optional[UUID] = Field(
        None, description="ID da pasta pai (se aplicável)"
    )


class DocumentUpdate(BaseModel):
    """Schema para atualização de documentos."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Novo título"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Nova descrição"
    )
    category: Optional[DocumentCategory] = Field(None, description="Nova categoria")
    tags: Optional[List[str]] = Field(None, description="Novas tags")
    is_public: Optional[bool] = Field(None, description="Alterar visibilidade pública")
    permission_level: Optional[PermissionLevel] = Field(
        None, description="Novo nível de permissão"
    )


class DocumentRead(DocumentBase):
    """Schema para leitura de documentos."""

    id: UUID
    file_path: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    checksum: Optional[str]
    status: DocumentStatus
    download_count: int = Field(0, description="Número de downloads")
    version: int = Field(1, description="Versão atual do documento")

    # Metadados do sistema
    created_by: UUID
    created_by_name: str
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    # Relacionamentos
    folder_id: Optional[UUID] = None
    folder_name: Optional[str] = None

    # URLs de acesso
    download_url: Optional[str] = None
    preview_url: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Schema para lista de documentos."""

    documents: List[DocumentRead]
    total: int
    page: int
    size: int
    total_pages: int


class DocumentSearchFilters(BaseModel):
    """Schema para filtros de busca de documentos."""

    category: Optional[DocumentCategory] = None
    document_type: Optional[DocumentType] = None
    status: Optional[DocumentStatus] = None
    permission_level: Optional[PermissionLevel] = None
    tags: Optional[List[str]] = None
    created_by: Optional[UUID] = None
    folder_id: Optional[UUID] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search_text: Optional[str] = None
    is_public: Optional[bool] = None


class DocumentFolderBase(BaseModel):
    """Schema base para pastas de documentos."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome da pasta")
    description: Optional[str] = Field(
        None, max_length=500, description="Descrição da pasta"
    )
    parent_folder_id: Optional[UUID] = Field(None, description="ID da pasta pai")
    is_public: bool = Field(False, description="Se a pasta é pública")


class DocumentFolderCreate(DocumentFolderBase):
    """Schema para criação de pastas."""


class DocumentFolderRead(DocumentFolderBase):
    """Schema para leitura de pastas."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    document_count: int = Field(0, description="Número de documentos na pasta")

    class Config:
        from_attributes = True


class DocumentPermissionBase(BaseModel):
    """Schema base para permissões de documentos."""

    user_id: UUID = Field(..., description="ID do usuário")
    permission_level: PermissionLevel = Field(..., description="Nível de permissão")
    can_download: bool = Field(True, description="Permissão de download")
    can_edit: bool = Field(False, description="Permissão de edição")
    can_delete: bool = Field(False, description="Permissão de exclusão")
    can_share: bool = Field(False, description="Permissão de compartilhamento")


class DocumentPermissionCreate(DocumentPermissionBase):
    """Schema para criação de permissões."""

    document_id: UUID = Field(..., description="ID do documento")


class DocumentPermissionRead(DocumentPermissionBase):
    """Schema para leitura de permissões."""

    id: UUID
    document_id: UUID
    granted_by: UUID
    granted_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentVersionBase(BaseModel):
    """Schema base para versões de documentos."""

    version_number: int = Field(..., ge=1, description="Número da versão")
    change_description: str = Field(
        ..., max_length=500, description="Descrição das alterações"
    )
    file_path: str = Field(..., description="Caminho do arquivo da versão")
    file_size: int = Field(..., ge=0, description="Tamanho do arquivo")


class DocumentVersionRead(DocumentVersionBase):
    """Schema para leitura de versões."""

    id: UUID
    document_id: UUID
    created_by: UUID
    created_at: datetime
    checksum: str

    class Config:
        from_attributes = True


class DocumentAuditLogBase(BaseModel):
    """Schema base para logs de auditoria."""

    action: str = Field(..., description="Ação realizada")
    details: Optional[str] = Field(
        None, max_length=1000, description="Detalhes da ação"
    )
    ip_address: Optional[str] = Field(None, description="IP de origem")
    user_agent: Optional[str] = Field(None, description="User agent")


class DocumentAuditLogRead(DocumentAuditLogBase):
    """Schema para leitura de logs de auditoria."""

    id: UUID
    document_id: UUID
    user_id: UUID
    user_name: str
    timestamp: datetime

    class Config:
        from_attributes = True


class DocumentStatistics(BaseModel):
    """Schema para estatísticas de documentos."""

    total_documents: int
    documents_by_category: Dict[str, int]
    documents_by_status: Dict[str, int]
    total_size_bytes: int
    avg_file_size_bytes: float
    documents_by_type: Dict[str, int]
    recent_uploads: int  # Últimos 30 dias
    top_uploaders: List[Dict[str, Any]]


class DocumentShareBase(BaseModel):
    """Schema base para compartilhamento de documentos."""

    expires_at: Optional[datetime] = Field(
        None, description="Data de expiração do link"
    )
    max_downloads: Optional[int] = Field(
        None, ge=1, description="Número máximo de downloads"
    )
    password_protected: bool = Field(False, description="Se requer senha")
    allow_download: bool = Field(True, description="Permite download")


class DocumentShareCreate(DocumentShareBase):
    """Schema para criação de links de compartilhamento."""

    document_id: UUID = Field(..., description="ID do documento")


class DocumentShareRead(DocumentShareBase):
    """Schema para leitura de links de compartilhamento."""

    id: UUID
    document_id: UUID
    share_token: str
    created_by: UUID
    created_at: datetime
    download_count: int = Field(0, description="Número de downloads")
    is_active: bool = Field(True, description="Se o link está ativo")

    class Config:
        from_attributes = True


class DocumentTemplateBase(BaseModel):
    """Schema base para templates de documentos."""

    name: str = Field(..., min_length=1, max_length=255, description="Nome do template")
    description: str = Field(..., max_length=1000, description="Descrição do template")
    category: DocumentCategory = Field(..., description="Categoria do template")
    file_path: str = Field(..., description="Caminho do arquivo template")
    variables: Dict[str, Any] = Field(
        default_factory=dict, description="Variáveis do template"
    )


class DocumentTemplateRead(DocumentTemplateBase):
    """Schema para leitura de templates."""

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    usage_count: int = Field(0, description="Número de usos")

    class Config:
        from_attributes = True
