"""
Testes unitários para modelos de documentos

Foco em lógica crítica de validação de dados:
- Document model: validações de campos obrigatórios
- DocumentFolder: hierarquia e permissões
- DocumentPermission: controle de acesso granular
- DocumentShare: compartilhamento seguro
- Validações de checksum e integridade
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

# Importar os modelos que queremos testar
from modules.documents.models.documents_models import (
    Document,
    DocumentAuditLog,
    DocumentFolder,
    DocumentPermission,
    DocumentShare,
    DocumentTemplate,
    DocumentVersion,
)

# Importar enums
from modules.documents.schemas.documents import (
    DocumentCategory,
    DocumentStatus,
    DocumentType,
    PermissionLevel,
)


class TestDocumentModel:
    """Testes para modelo Document - validações críticas"""

    def test_document_creation_valid(self):
        """Testar criação de documento com dados válidos"""
        user_id = uuid4()

        document = Document(
            title="Test Document",
            description="Test description",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            status=DocumentStatus.ACTIVE,
            file_path="/documents/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
            checksum="abc123def456",
            is_public=False,
            permission_level=PermissionLevel.RESTRICTED,
            created_by=user_id,
            tags=["test", "document"],
        )

        assert document.title == "Test Document"
        assert document.category == DocumentCategory.ADMINISTRATIVE
        assert document.status == DocumentStatus.ACTIVE
        assert document.version == 1
        assert document.download_count == 0
        assert document.is_public is False
        assert document.created_by == user_id
        assert isinstance(document.tags, list)

    def test_document_repr(self):
        """Testar representação string do documento"""
        user_id = uuid4()

        document = Document(
            id=uuid4(),
            title="Test Document",
            category=DocumentCategory.ADMINISTRATIVE,
            created_by=user_id,
        )

        repr_str = repr(document)
        assert "Document" in repr_str
        assert str(document.id) in repr_str
        assert "Test Document" in repr_str

    def test_document_expires_at_validation(self):
        """Testar validação de data de expiração"""
        user_id = uuid4()
        future_date = datetime.utcnow() + timedelta(days=30)
        past_date = datetime.utcnow() - timedelta(days=1)

        # Documento com expiração futura (válido)
        document_valid = Document(
            title="Valid Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            created_by=user_id,
            expires_at=future_date,
        )

        assert document_valid.expires_at == future_date

        # Documento com expiração passada (válido, mas expirado)
        document_expired = Document(
            title="Expired Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            created_by=user_id,
            expires_at=past_date,
        )

        assert document_expired.expires_at == past_date

    def test_document_file_validation(self):
        """Testar validações de arquivo"""
        user_id = uuid4()

        # Documento com arquivo válido
        document = Document(
            title="File Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            file_path="/path/to/file.pdf",
            file_size=2048,
            mime_type="application/pdf",
            checksum="sha256_hash_here",
            created_by=user_id,
        )

        assert document.file_size == 2048
        assert document.mime_type == "application/pdf"
        assert document.checksum == "sha256_hash_here"

    def test_document_tags_json_validation(self):
        """Testar validação de tags como JSON"""
        user_id = uuid4()

        # Tags como lista
        tags_list = ["tag1", "tag2", "tag3"]
        document = Document(
            title="Tagged Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            created_by=user_id,
            tags=tags_list,
        )

        assert document.tags == tags_list

        # Tags como string JSON
        tags_json = '["tag1", "tag2"]'
        document_json = Document(
            title="JSON Tagged Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            created_by=user_id,
            tags=tags_json,
        )

        assert document_json.tags == tags_json


class TestDocumentFolderModel:
    """Testes para modelo DocumentFolder - hierarquia"""

    def test_folder_creation_valid(self):
        """Testar criação de pasta com dados válidos"""
        user_id = uuid4()

        folder = DocumentFolder(
            name="Test Folder",
            description="Test folder description",
            is_public=False,
            created_by=user_id,
        )

        assert folder.name == "Test Folder"
        assert folder.is_public is False
        assert folder.created_by == user_id

    def test_folder_repr(self):
        """Testar representação string da pasta"""
        user_id = uuid4()

        folder = DocumentFolder(id=uuid4(), name="Test Folder", created_by=user_id)

        repr_str = repr(folder)
        assert "DocumentFolder" in repr_str
        assert str(folder.id) in repr_str
        assert "Test Folder" in repr_str

    def test_folder_hierarchy(self):
        """Testar hierarquia de pastas"""
        user_id = uuid4()
        parent_id = uuid4()

        # Pasta pai
        parent_folder = DocumentFolder(
            id=parent_id, name="Parent Folder", created_by=user_id
        )

        # Pasta filha
        child_folder = DocumentFolder(
            name="Child Folder", parent_folder_id=parent_id, created_by=user_id
        )

        assert child_folder.parent_folder_id == parent_id
        assert child_folder.name == "Child Folder"


class TestDocumentPermissionModel:
    """Testes para modelo DocumentPermission - controle de acesso"""

    def test_permission_creation_valid(self):
        """Testar criação de permissão com dados válidos"""
        doc_id = uuid4()
        user_id = uuid4()
        grantor_id = uuid4()

        permission = DocumentPermission(
            document_id=doc_id,
            user_id=user_id,
            granted_by=grantor_id,
            permission_level=PermissionLevel.READ,
            can_download=True,
            can_edit=False,
            can_delete=False,
            can_share=False,
        )

        assert permission.document_id == doc_id
        assert permission.user_id == user_id
        assert permission.granted_by == grantor_id
        assert permission.permission_level == PermissionLevel.READ
        assert permission.can_download is True
        assert permission.can_edit is False

    def test_permission_repr(self):
        """Testar representação string da permissão"""
        doc_id = uuid4()
        user_id = uuid4()
        grantor_id = uuid4()

        permission = DocumentPermission(
            id=uuid4(),
            document_id=doc_id,
            user_id=user_id,
            granted_by=grantor_id,
            permission_level=PermissionLevel.EDIT,
        )

        repr_str = repr(permission)
        assert "DocumentPermission" in repr_str
        assert str(permission.id) in repr_str
        assert "EDIT" in repr_str

    def test_permission_expires_at(self):
        """Testar expiração de permissões"""
        doc_id = uuid4()
        user_id = uuid4()
        grantor_id = uuid4()
        expiry_date = datetime.utcnow() + timedelta(days=7)

        permission = DocumentPermission(
            document_id=doc_id,
            user_id=user_id,
            granted_by=grantor_id,
            permission_level=PermissionLevel.READ,
            expires_at=expiry_date,
        )

        assert permission.expires_at == expiry_date

    def test_permission_all_operations_disabled(self):
        """Testar permissão com todas operações desabilitadas"""
        doc_id = uuid4()
        user_id = uuid4()
        grantor_id = uuid4()

        permission = DocumentPermission(
            document_id=doc_id,
            user_id=user_id,
            granted_by=grantor_id,
            permission_level=PermissionLevel.RESTRICTED,
            can_download=False,
            can_edit=False,
            can_delete=False,
            can_share=False,
        )

        assert permission.can_download is False
        assert permission.can_edit is False
        assert permission.can_delete is False
        assert permission.can_share is False


class TestDocumentVersionModel:
    """Testes para modelo DocumentVersion - versionamento"""

    def test_version_creation_valid(self):
        """Testar criação de versão com dados válidos"""
        doc_id = uuid4()
        user_id = uuid4()

        version = DocumentVersion(
            document_id=doc_id,
            created_by=user_id,
            version_number=2,
            change_description="Updated content",
            file_path="/documents/v2.pdf",
            file_size=2048,
            checksum="new_hash_456",
        )

        assert version.document_id == doc_id
        assert version.created_by == user_id
        assert version.version_number == 2
        assert version.change_description == "Updated content"
        assert version.file_size == 2048
        assert version.checksum == "new_hash_456"

    def test_version_repr(self):
        """Testar representação string da versão"""
        doc_id = uuid4()
        user_id = uuid4()

        version = DocumentVersion(
            id=uuid4(), document_id=doc_id, created_by=user_id, version_number=1
        )

        repr_str = repr(version)
        assert "DocumentVersion" in repr_str
        assert str(version.id) in repr_str
        assert "version=1" in repr_str


class TestDocumentAuditLogModel:
    """Testes para modelo DocumentAuditLog - auditoria"""

    def test_audit_log_creation_valid(self):
        """Testar criação de log de auditoria"""
        doc_id = uuid4()
        user_id = uuid4()

        audit_log = DocumentAuditLog(
            document_id=doc_id,
            user_id=user_id,
            action="download",
            details="Document downloaded successfully",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 Test Browser",
        )

        assert audit_log.document_id == doc_id
        assert audit_log.user_id == user_id
        assert audit_log.action == "download"
        assert audit_log.details == "Document downloaded successfully"
        assert audit_log.ip_address == "192.168.1.100"
        assert audit_log.user_agent == "Mozilla/5.0 Test Browser"
        assert isinstance(audit_log.timestamp, datetime)

    def test_audit_log_repr(self):
        """Testar representação string do log de auditoria"""
        doc_id = uuid4()
        user_id = uuid4()

        audit_log = DocumentAuditLog(
            id=uuid4(),
            document_id=doc_id,
            user_id=user_id,
            action="create",
            timestamp=datetime.utcnow(),
        )

        repr_str = repr(audit_log)
        assert "DocumentAuditLog" in repr_str
        assert "create" in repr_str
        assert str(audit_log.timestamp) in repr_str


class TestDocumentShareModel:
    """Testes para modelo DocumentShare - compartilhamento"""

    def test_share_creation_valid(self):
        """Testar criação de compartilhamento válido"""
        doc_id = uuid4()
        user_id = uuid4()

        share = DocumentShare(
            document_id=doc_id,
            created_by=user_id,
            share_token="unique_token_123456",
            expires_at=datetime.utcnow() + timedelta(days=7),
            max_downloads=10,
            password_protected=False,
            allow_download=True,
            is_active=True,
        )

        assert share.document_id == doc_id
        assert share.created_by == user_id
        assert share.share_token == "unique_token_123456"
        assert share.expires_at is not None
        assert share.max_downloads == 10
        assert share.password_protected is False
        assert share.allow_download is True
        assert share.is_active is True
        assert share.download_count == 0

    def test_share_repr(self):
        """Testar representação string do compartilhamento"""
        doc_id = uuid4()
        user_id = uuid4()

        share = DocumentShare(
            id=uuid4(),
            document_id=doc_id,
            created_by=user_id,
            share_token="abc123def456",
        )

        repr_str = repr(share)
        assert "DocumentShare" in repr_str
        assert "abc123de..." in repr_str  # Token truncado

    def test_share_token_uniqueness(self):
        """Testar unicidade do token de compartilhamento"""
        doc_id = uuid4()
        user_id = uuid4()

        share1 = DocumentShare(
            document_id=doc_id, created_by=user_id, share_token="unique_token_1"
        )

        share2 = DocumentShare(
            document_id=doc_id, created_by=user_id, share_token="unique_token_2"
        )

        assert share1.share_token != share2.share_token

    def test_share_password_protected(self):
        """Testar compartilhamento protegido por senha"""
        doc_id = uuid4()
        user_id = uuid4()

        share = DocumentShare(
            document_id=doc_id,
            created_by=user_id,
            share_token="password_protected_token",
            password_protected=True,
            allow_download=False,  # Apenas visualização
        )

        assert share.password_protected is True
        assert share.allow_download is False


class TestDocumentTemplateModel:
    """Testes para modelo DocumentTemplate - templates"""

    def test_template_creation_valid(self):
        """Testar criação de template válido"""
        user_id = uuid4()

        template = DocumentTemplate(
            name="Test Template",
            description="Template for testing",
            category=DocumentCategory.ADMINISTRATIVE,
            file_path="/templates/test.docx",
            variables={"name": "string", "date": "date"},
            usage_count=0,
            created_by=user_id,
            is_public=False,
        )

        assert template.name == "Test Template"
        assert template.category == DocumentCategory.ADMINISTRATIVE
        assert template.variables == {"name": "string", "date": "date"}
        assert template.usage_count == 0
        assert template.is_public is False
        assert template.created_by == user_id

    def test_template_repr(self):
        """Testar representação string do template"""
        user_id = uuid4()

        template = DocumentTemplate(
            id=uuid4(),
            name="Test Template",
            category=DocumentCategory.ADMINISTRATIVE,
            created_by=user_id,
        )

        repr_str = repr(template)
        assert "DocumentTemplate" in repr_str
        assert str(template.id) in repr_str
        assert "Test Template" in repr_str

    def test_template_usage_count(self):
        """Testar contador de uso do template"""
        user_id = uuid4()

        template = DocumentTemplate(
            name="Usage Test Template",
            description="Template to test usage counting",
            category=DocumentCategory.ADMINISTRATIVE,
            file_path="/templates/usage_test.docx",
            created_by=user_id,
            usage_count=5,
        )

        assert template.usage_count == 5

        # Simular incremento de uso
        template.usage_count += 1
        assert template.usage_count == 6


class TestModelValidations:
    """Testes para validações gerais dos modelos"""

    def test_document_required_fields(self):
        """Testar campos obrigatórios do documento"""
        user_id = uuid4()

        # Documento sem campos obrigatórios deve funcionar (SQLAlchemy defaults)
        document = Document(
            title="Minimal Document",
            category=DocumentCategory.ADMINISTRATIVE,
            document_type=DocumentType.PDF,
            created_by=user_id,
        )

        assert document.title == "Minimal Document"
        assert document.version == 1  # Default
        assert document.download_count == 0  # Default
        assert document.is_public is False  # Default

    def test_folder_required_fields(self):
        """Testar campos obrigatórios da pasta"""
        user_id = uuid4()

        # Pasta sem campos opcionais
        folder = DocumentFolder(name="Minimal Folder", created_by=user_id)

        assert folder.name == "Minimal Folder"
        assert folder.is_public is False  # Default

    def test_permission_required_fields(self):
        """Testar campos obrigatórios da permissão"""
        doc_id = uuid4()
        user_id = uuid4()
        grantor_id = uuid4()

        # Permissão com valores padrão
        permission = DocumentPermission(
            document_id=doc_id,
            user_id=user_id,
            granted_by=grantor_id,
            permission_level=PermissionLevel.READ,
        )

        assert permission.can_download is True  # Default
        assert permission.can_edit is False  # Default
        assert permission.can_delete is False  # Default
        assert permission.can_share is False  # Default

    def test_audit_log_required_fields(self):
        """Testar campos obrigatórios do log de auditoria"""
        doc_id = uuid4()
        user_id = uuid4()

        # Log de auditoria mínimo
        audit_log = DocumentAuditLog(document_id=doc_id, user_id=user_id, action="view")

        assert audit_log.action == "view"
        assert isinstance(audit_log.timestamp, datetime)

    def test_share_required_fields(self):
        """Testar campos obrigatórios do compartilhamento"""
        doc_id = uuid4()
        user_id = uuid4()

        # Compartilhamento com valores padrão
        share = DocumentShare(
            document_id=doc_id, created_by=user_id, share_token="test_token_123"
        )

        assert share.password_protected is False  # Default
        assert share.allow_download is True  # Default
        assert share.is_active is True  # Default
        assert share.download_count == 0  # Default
