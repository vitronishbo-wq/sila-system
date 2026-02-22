"""
Modelos SQLAlchemy para o módulo de Documentos.

Define as entidades principais para:
- Gestão completa de documentos digitais
- Controle de acesso e permissões
- Sistema de pastas e organização
- Versionamento e auditoria
- Compartilhamento seguro
- Templates de documentos
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import backref, relationship

from core.db.base_class import Base  # Use centralized Base

from ..schemas.documents import (
    DocumentCategory,
    DocumentStatus,
    DocumentType,
    PermissionLevel,
)

# Remove local Base creation


class Document(Base):
    """
    Modelo principal para documentos digitais.

    Gerencia todos os aspectos de documentos no sistema,
    incluindo metadados, controle de acesso e versionamento.
    """

    __tablename__ = "documents_documents"

    __table_args__ = {"extend_existing": True}

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(Enum(DocumentCategory), nullable=False, index=True)
    document_type = Column(Enum(DocumentType), nullable=False, index=True)
    status = Column(
        Enum(DocumentStatus), default=DocumentStatus.ACTIVE, nullable=False, index=True
    )

    # Informações do arquivo
    file_path = Column(String(1000))  # Caminho no storage
    file_size = Column(Integer)  # Tamanho em bytes
    mime_type = Column(String(100))
    checksum = Column(String(128))  # Hash para verificação de integridade

    # Controle de acesso
    is_public = Column(Boolean, default=False, nullable=False)
    permission_level = Column(
        Enum(PermissionLevel), default=PermissionLevel.RESTRICTED, nullable=False
    )

    # Metadados de uso
    download_count = Column(Integer, default=0, nullable=False)
    version = Column(Integer, default=1, nullable=False)

    # Controle de expiração
    expires_at = Column(DateTime)

    # Organização
    tags = Column(JSON)  # Lista de tags como JSON
    folder_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_document_folders.id")
    )

    # Auditoria
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    folder = relationship(
        "DocumentFolder", foreign_keys=[folder_id], back_populates="documents"
    )
    # creator = relationship(
    #     "Citizen",
    #     foreign_keys=[created_by],
    #     backref=backref("documents", lazy="dynamic"),
    # )  # TODO: Fix relationship - use created_by FK directly for now
    permissions = relationship(
        "DocumentPermission", back_populates="document", cascade="all, delete-orphan"
    )
    versions = relationship(
        "DocumentVersion", back_populates="document", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "DocumentAuditLog", back_populates="document", cascade="all, delete-orphan"
    )
    shares = relationship(
        "DocumentShare", back_populates="document", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Document(id={self.id}, title='{self.title}', category={self.category})>"
        )


class DocumentFolder(Base):
    """
    Modelo para organização hierárquica de documentos.

    Permite criar estrutura de pastas para organizar documentos,
    com suporte a hierarquia e permissões específicas.
    """

    __tablename__ = "documents_document_folders"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    is_public = Column(Boolean, default=False, nullable=False)

    # Hierarquia
    parent_folder_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_document_folders.id")
    )

    # Controle de acesso
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    parent_folder = relationship("DocumentFolder", remote_side=[id])
    subfolders = relationship(
        "DocumentFolder", back_populates="parent_folder", cascade="all, delete-orphan"
    )
    documents = relationship(
        "Document", back_populates="folder", cascade="all, delete-orphan"
    )
    # creator = relationship(
    #     "Citizen", foreign_keys=[created_by], backref=backref("folders", lazy="dynamic")
    # )  # TODO: Fix relationship

    def __repr__(self):
        return f"<DocumentFolder(id={self.id}, name='{self.name}')>"


class DocumentPermission(Base):
    """
    Modelo para controle granular de permissões.

    Define permissões específicas de usuários para documentos,
    incluindo níveis de acesso e operações permitidas.
    """

    __tablename__ = "documents_document_permissions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    document_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_documents.id"), nullable=False
    )
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)
    granted_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)

    # Nível de permissão
    permission_level = Column(Enum(PermissionLevel), nullable=False)

    # Permissões específicas
    can_download = Column(Boolean, default=True, nullable=False)
    can_edit = Column(Boolean, default=False, nullable=False)
    can_delete = Column(Boolean, default=False, nullable=False)
    can_share = Column(Boolean, default=False, nullable=False)

    # Controle de expiração
    expires_at = Column(DateTime)

    # Timestamps
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    document = relationship(
        "Document", foreign_keys=[document_id], back_populates="permissions"
    )
    user = relationship(
        "Citizen",
        foreign_keys=[user_id],
        backref=backref("document_permissions", lazy="dynamic"),
    )
    grantor = relationship(
        "Citizen",
        foreign_keys=[granted_by],
        backref=backref("granted_permissions", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<DocumentPermission(id={self.id}, user_id={self.user_id}, permission_level={self.permission_level})>"


class DocumentVersion(Base):
    """
    Modelo para versionamento de documentos.

    Mantém histórico completo de versões de cada documento,
    permitindo rastrear alterações e reverter quando necessário.
    """

    __tablename__ = "documents_document_versions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    document_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_documents.id"), nullable=False
    )
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)

    # Dados da versão
    version_number = Column(Integer, nullable=False)
    change_description = Column(Text, nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String(128), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    document = relationship(
        "Document", foreign_keys=[document_id], back_populates="versions"
    )
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("document_versions", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<DocumentVersion(id={self.id}, document_id={self.document_id}, version={self.version_number})>"


class DocumentAuditLog(Base):
    """
    Modelo para auditoria completa de operações.

    Registra todas as ações realizadas em documentos para
    conformidade, segurança e rastreabilidade.
    """

    __tablename__ = "documents_document_audit_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    document_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_documents.id"), nullable=False
    )
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)

    # Dados da ação
    action = Column(String(100), nullable=False, index=True)
    details = Column(Text)
    ip_address = Column(String(45))  # Suporte IPv4 e IPv6
    user_agent = Column(Text)

    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relacionamentos
    document = relationship(
        "Document", foreign_keys=[document_id], back_populates="audit_logs"
    )
    user = relationship(
        "Citizen", backref=backref("document_audit_logs", lazy="dynamic")
    )

    def __repr__(self):
        return f"<DocumentAuditLog(id={self.id}, action='{self.action}', timestamp={self.timestamp})>"


class DocumentShare(Base):
    """
    Modelo para compartilhamento seguro de documentos.

    Permite criar links públicos temporários para documentos,
    com controle de acesso e limites de uso.
    """

    __tablename__ = "documents_document_shares"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Relacionamentos
    document_id = Column(
        PGUUID(as_uuid=True), ForeignKey("documents_documents.id"), nullable=False
    )
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)

    # Dados do compartilhamento
    share_token = Column(String(128), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime)
    max_downloads = Column(Integer)
    password_protected = Column(Boolean, default=False, nullable=False)
    allow_download = Column(Boolean, default=True, nullable=False)

    # Controle de uso
    download_count = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_accessed_at = Column(DateTime)

    # Relacionamentos
    document = relationship(
        "Document", foreign_keys=[document_id], back_populates="shares"
    )
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("document_shares", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<DocumentShare(id={self.id}, document_id={self.document_id}, token='{self.share_token[:8]}...')>"


class DocumentTemplate(Base):
    """
    Modelo para templates de documentos.

    Permite criar e gerenciar templates reutilizáveis
    para geração automática de documentos.
    """

    __tablename__ = "documents_document_templates"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Dados básicos
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(DocumentCategory), nullable=False, index=True)

    # Arquivo do template
    file_path = Column(String(1000), nullable=False)
    variables = Column(JSON)  # Campos variáveis do template

    # Controle de uso
    usage_count = Column(Integer, default=0, nullable=False)

    # Controle de acesso
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizenship_citizens.id"), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("document_templates", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<DocumentTemplate(id={self.id}, name='{self.name}', category={self.category})>"


# Índices adicionais para otimização de consultas
from sqlalchemy import Index

# Índices compostos para consultas frequentes
Index("idx_documents_category_status", Document.category, Document.status)
Index("idx_documents_created_by_status", Document.created_by, Document.status)
Index("idx_documents_folder_category", Document.folder_id, Document.category)
Index(
    "idx_documents_tags", Document.id, postgresql_using="gin"
)  # Para busca por tags JSON

Index(
    "idx_folders_parent_public",
    DocumentFolder.parent_folder_id,
    DocumentFolder.is_public,
)
Index("idx_folders_created_by", DocumentFolder.created_by)

Index(
    "idx_permissions_document_user",
    DocumentPermission.document_id,
    DocumentPermission.user_id,
)
Index(
    "idx_permissions_user_active",
    DocumentPermission.user_id,
    DocumentPermission.expires_at,
)

Index(
    "idx_audit_logs_document_timestamp",
    DocumentAuditLog.document_id,
    DocumentAuditLog.timestamp,
)
Index(
    "idx_audit_logs_user_timestamp",
    DocumentAuditLog.user_id,
    DocumentAuditLog.timestamp,
)
Index(
    "idx_audit_logs_action_timestamp",
    DocumentAuditLog.action,
    DocumentAuditLog.timestamp,
)

Index("idx_shares_token_active", DocumentShare.share_token, DocumentShare.is_active)
Index("idx_shares_document_active", DocumentShare.document_id, DocumentShare.is_active)

Index(
    "idx_templates_category_public",
    DocumentTemplate.category,
    DocumentTemplate.is_public,
)
Index("idx_templates_created_by", DocumentTemplate.created_by)
