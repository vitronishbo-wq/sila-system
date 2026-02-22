"""
Serviço principal para gestão de documentos.

Este módulo implementa a lógica de negócio completa para:
- Upload e armazenamento seguro de documentos
- Controle de acesso e permissões granulares
- Organização hierárquica em pastas
- Versionamento e auditoria completa
- Busca avançada com filtros
- Compartilhamento seguro
- Templates de documentos
"""

import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.citizenship.models.citizen import Citizen
from modules.documents.models.documents_models import (
    Document,
    DocumentAuditLog,
    DocumentFolder,
    DocumentPermission,
    DocumentShare,
)

from ..schemas.documents import (
    DocumentCreate,
    DocumentFolderCreate,
    DocumentFolderRead,
    DocumentRead,
    DocumentSearchFilters,
    DocumentShareCreate,
    DocumentShareRead,
    DocumentStatus,
    DocumentType,
    DocumentUpdate,
    DocumentUpload,
)

logger = logging.getLogger(__name__)

# Configurações de upload
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "txt",
    "rtf",
    "jpg",
    "jpeg",
    "png",
    "gif",
    "tiff",
    "zip",
    "rar",
}
UPLOAD_DIR = "/opt/sila-system/uploads/documents"


class DocumentService:
    """Classe principal para operações documentais."""

    @staticmethod
    async def get_user_documents(
        db: AsyncSession,
        citizen_id: UUID,
        filters: Optional[DocumentSearchFilters] = None,
        page: int = 1,
        size: int = 20,
    ) -> Tuple[List[DocumentRead], int]:
        """
        Busca documentos do usuário com filtros aplicados.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão
            filters: Filtros de busca opcionais
            page: Página para paginação
            size: Tamanho da página

        Returns:
            Tupla com lista de documentos e total de registros
        """
        try:
            # Query base com relacionamentos
            query = (
                db.query(Document)
                .options(selectinload(Document.folder), selectinload(Document.creator))
                .filter(
                    or_(
                        Document.created_by == citizen_id,
                        Document.is_public == True,
                        # Documentos compartilhados com o usuário
                        Document.id.in_(
                            db.query(DocumentPermission.document_id).filter(
                                DocumentPermission.user_id == citizen_id,
                                or_(
                                    DocumentPermission.expires_at.is_(None),
                                    DocumentPermission.expires_at > datetime.utcnow(),
                                ),
                            )
                        ),
                    )
                )
            )

            # Aplicar filtros
            if filters:
                if filters.category:
                    query = query.filter(Document.category == filters.category)
                if filters.document_type:
                    query = query.filter(
                        Document.document_type == filters.document_type
                    )
                if filters.status:
                    query = query.filter(Document.status == filters.status)
                if filters.is_public is not None:
                    query = query.filter(Document.is_public == filters.is_public)
                if filters.folder_id:
                    query = query.filter(Document.folder_id == filters.folder_id)
                if filters.date_from:
                    query = query.filter(Document.created_at >= filters.date_from)
                if filters.date_to:
                    query = query.filter(Document.created_at <= filters.date_to)
                if filters.search_text:
                    search_filter = f"%{filters.search_text}%"
                    query = query.filter(
                        or_(
                            Document.title.ilike(search_filter),
                            Document.description.ilike(search_filter),
                        )
                    )

            # Ordenação e paginação
            total = query.count()
            documents = (
                query.order_by(desc(Document.created_at))
                .offset((page - 1) * size)
                .limit(size)
                .all()
            )

            # Converter para schema de leitura
            result = []
            for doc in documents:
                doc_dict = await DocumentService._document_to_dict(db, doc, citizen_id)
                result.append(DocumentRead(**doc_dict))

            return result, total

        except Exception as e:
            logger.error(f"Erro ao buscar documentos do usuário: {e}")
            raise

    @staticmethod
    async def upload_document(
        db: AsyncSession,
        file: UploadFile,
        upload_data: DocumentUpload,
        citizen_id: UUID,
    ) -> DocumentRead:
        """
        Realiza upload e armazenamento de documento.

        Args:
            db: Sessão do banco de dados
            file: Arquivo enviado
            upload_data: Dados do upload
            citizen_id: ID do cidadão

        Returns:
            Documento criado
        """
        try:
            # Validar arquivo
            (
                file_path,
                file_size,
                mime_type,
                checksum,
            ) = await DocumentService._validate_and_store_file(file)

            # Criar documento no banco
            document_data = DocumentCreate(
                title=upload_data.title,
                description=upload_data.description,
                category=upload_data.category,
                document_type=DocumentService._get_document_type_from_mime(mime_type),
                tags=upload_data.tags,
                is_public=upload_data.is_public,
                permission_level=upload_data.permission_level,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type,
                checksum=checksum,
                created_by=citizen_id,
            )

            # Se especificada pasta pai, verificar se existe e se usuário tem acesso
            if upload_data.parent_folder_id:
                folder = (
                    db.query(DocumentFolder)
                    .filter(DocumentFolder.id == upload_data.parent_folder_id)
                    .first()
                )

                if not folder:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Pasta não encontrada",
                    )

                if not folder.is_public and folder.created_by != citizen_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para usar esta pasta",
                    )

                document_data.folder_id = upload_data.parent_folder_id

            # Criar documento
            new_document = Document(**document_data.dict())
            db.add(new_document)
            db.commit()
            db.refresh(new_document)

            # Registrar ação na auditoria
            await DocumentService._log_audit_action(
                db,
                new_document.id,
                citizen_id,
                "UPLOAD",
                f"Documento '{upload_data.title}' enviado",
            )

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(
                db, new_document, citizen_id
            )

            logger.info(f"Documento enviado com sucesso: {new_document.id}")
            return DocumentRead(**doc_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro no upload de documento: {e}")
            raise

    @staticmethod
    async def get_document_by_id(
        db: AsyncSession, document_id: UUID, citizen_id: UUID
    ) -> Optional[DocumentRead]:
        """
        Busca documento específico por ID.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            citizen_id: ID do cidadão solicitante

        Returns:
            Dados do documento ou None se não encontrado/não autorizado
        """
        try:
            document = (
                db.query(Document)
                .options(
                    selectinload(Document.folder),
                    selectinload(Document.creator),
                    selectinload(Document.permissions),
                )
                .filter(Document.id == document_id)
                .first()
            )

            if not document:
                return None

            # Verificar permissões
            if not await DocumentService._check_document_access(
                db, document, citizen_id
            ):
                return None

            # Registrar acesso na auditoria
            await DocumentService._log_audit_action(
                db, document_id, citizen_id, "ACCESS", "Documento acessado"
            )

            # Incrementar contador de downloads se for acesso para download
            document.download_count += 1
            db.commit()

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(db, document, citizen_id)
            return DocumentRead(**doc_dict)

        except Exception as e:
            logger.error(f"Erro ao buscar documento por ID: {e}")
            raise

    @staticmethod
    async def update_document(
        db: AsyncSession,
        document_id: UUID,
        update_data: DocumentUpdate,
        citizen_id: UUID,
    ) -> Optional[DocumentRead]:
        """
        Atualiza metadados de documento.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            update_data: Dados para atualização
            citizen_id: ID do cidadão

        Returns:
            Documento atualizado ou None se não autorizado
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                return None

            # Verificar se usuário pode editar
            if document.created_by != citizen_id:
                # Verificar se tem permissão específica de edição
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_edit == True,
                        or_(
                            DocumentPermission.expires_at.is_(None),
                            DocumentPermission.expires_at > datetime.utcnow(),
                        ),
                    )
                    .first()
                )

                if not permission:
                    return None

            # Atualizar campos permitidos
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                if hasattr(document, field):
                    setattr(document, field, value)

            document.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(document)

            # Registrar alteração na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "UPDATE",
                f"Documento atualizado: {list(update_dict.keys())}",
            )

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(db, document, citizen_id)
            return DocumentRead(**doc_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar documento: {e}")
            raise

    @staticmethod
    async def delete_document(
        db: AsyncSession, document_id: UUID, citizen_id: UUID
    ) -> bool:
        """
        Remove documento (soft delete).

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            citizen_id: ID do cidadão

        Returns:
            True se removido com sucesso
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                return False

            # Verificar se usuário pode deletar
            if document.created_by != citizen_id:
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_delete == True,
                    )
                    .first()
                )

                if not permission:
                    return False

            # Soft delete - alterar status
            document.status = DocumentStatus.DELETED
            document.updated_at = datetime.utcnow()
            db.commit()

            # Registrar exclusão na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "DELETE",
                "Documento removido (soft delete)",
            )

            logger.info(f"Documento removido: {document_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao remover documento: {e}")
            raise

    @staticmethod
    async def create_folder(
        db: AsyncSession, folder_data: DocumentFolderCreate, citizen_id: UUID
    ) -> DocumentFolderRead:
        """
        Cria nova pasta para organização de documentos.

        Args:
            db: Sessão do banco de dados
            folder_data: Dados da pasta
            citizen_id: ID do cidadão

        Returns:
            Pasta criada
        """
        try:
            # Se especificada pasta pai, verificar se existe e se usuário tem acesso
            if folder_data.parent_folder_id:
                parent_folder = (
                    db.query(DocumentFolder)
                    .filter(DocumentFolder.id == folder_data.parent_folder_id)
                    .first()
                )

                if not parent_folder:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Pasta pai não encontrada",
                    )

                if (
                    not parent_folder.is_public
                    and parent_folder.created_by != citizen_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para criar pasta nesta localização",
                    )

            # Criar pasta
            new_folder = DocumentFolder(
                name=folder_data.name,
                description=folder_data.description,
                parent_folder_id=folder_data.parent_folder_id,
                is_public=folder_data.is_public,
                created_by=citizen_id,
            )

            db.add(new_folder)
            db.commit()
            db.refresh(new_folder)

            # Converter para schema de leitura
            folder_dict = {
                "id": new_folder.id,
                "name": new_folder.name,
                "description": new_folder.description,
                "parent_folder_id": new_folder.parent_folder_id,
                "is_public": new_folder.is_public,
                "created_by": new_folder.created_by,
                "created_at": new_folder.created_at,
                "updated_at": new_folder.updated_at,
                "document_count": 0,
            }

            logger.info(f"Pasta criada: {new_folder.id}")
            return DocumentFolderRead(**folder_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar pasta: {e}")
            raise

    @staticmethod
    async def share_document(
        db: AsyncSession,
        document_id: UUID,
        share_data: DocumentShareCreate,
        citizen_id: UUID,
    ) -> DocumentShareRead:
        """
        Cria link de compartilhamento para documento.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            share_data: Dados do compartilhamento
            citizen_id: ID do cidadão

        Returns:
            Link de compartilhamento criado
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Documento não encontrado",
                )

            # Verificar se usuário pode compartilhar
            if document.created_by != citizen_id:
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_share == True,
                    )
                    .first()
                )

                if not permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para compartilhar este documento",
                    )

            # Gerar token único
            share_token = secrets.token_urlsafe(32)

            # Criar compartilhamento
            new_share = DocumentShare(
                document_id=document_id,
                created_by=citizen_id,
                share_token=share_token,
                expires_at=share_data.expires_at,
                max_downloads=share_data.max_downloads,
                password_protected=share_data.password_protected,
                allow_download=share_data.allow_download,
            )

            db.add(new_share)
            db.commit()
            db.refresh(new_share)

            # Converter para schema de leitura
            share_dict = {
                "id": new_share.id,
                "document_id": new_share.document_id,
                "share_token": new_share.share_token,
                "created_by": new_share.created_by,
                "created_at": new_share.created_at,
                "download_count": new_share.download_count,
                "is_active": new_share.is_active,
                "expires_at": share_data.expires_at,
                "max_downloads": share_data.max_downloads,
                "password_protected": share_data.password_protected,
                "allow_download": share_data.allow_download,
            }

            # Registrar compartilhamento na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "SHARE",
                f"Documento compartilhado com token: {share_token[:8]}...",
            )

            logger.info(f"Documento compartilhado: {document_id}")
            return DocumentShareRead(**share_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao compartilhar documento: {e}")
            raise

    @staticmethod
    async def get_document_statistics(
        db: AsyncSession, citizen_id: UUID
    ) -> Dict[str, Any]:
        """
        Obtém estatísticas de documentos do usuário.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão

        Returns:
            Estatísticas documentais
        """
        try:
            # Query para estatísticas gerais
            total_docs = (
                db.query(func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
            )

            docs_by_category = dict(
                db.query(Document.category, func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .group_by(Document.category)
                .all()
            )

            docs_by_status = dict(
                db.query(Document.status, func.count(Document.id))
                .filter(Document.created_by == citizen_id)
                .group_by(Document.status)
                .all()
            )

            total_size = (
                db.query(func.sum(Document.file_size))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
                or 0
            )

            # Documentos recentes (últimos 30 dias)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_uploads = (
                db.query(func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.created_at >= thirty_days_ago,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
            )

            # Top uploaders (outros usuários que compartilharam com ele)
            top_sharers = (
                db.query(
                    Citizen.full_name,
                    func.count(DocumentPermission.id).label("shared_count"),
                )
                .join(DocumentPermission, Citizen.id == DocumentPermission.granted_by)
                .filter(DocumentPermission.user_id == citizen_id)
                .group_by(Citizen.id, Citizen.full_name)
                .order_by(desc("shared_count"))
                .limit(5)
                .all()
            )

            return {
                "total_documents": total_docs,
                "documents_by_category": docs_by_category,
                "documents_by_status": docs_by_status,
                "total_size_bytes": total_size,
                "avg_file_size_bytes": total_size / max(total_docs, 1),
                "documents_by_type": {},  # Pode ser expandido
                "recent_uploads": recent_uploads,
                "top_uploaders": [
                    {"name": sharer.full_name, "shared_count": sharer.shared_count}
                    for sharer in top_sharers
                ],
            }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise

    # Métodos auxiliares privados

    @staticmethod
    async def _validate_and_store_file(file: UploadFile) -> Tuple[str, int, str, str]:
        """Valida e armazena arquivo enviado."""
        # Validar tamanho
        file_size = 0
        content = b""

        while chunk := await file.read(8192):
            file_size += len(chunk)
            content += chunk

            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Arquivo muito grande. Máximo: {MAX_FILE_SIZE} bytes",
                )

        # Validar extensão
        filename = file.filename or "unnamed_file"
        file_ext = filename.split(".")[-1].lower() if "." in filename else ""

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido: {file_ext}",
            )

        # Detectar MIME type
        import magic

        mime_type = magic.from_buffer(content, mime=True)

        # Calcular checksum
        checksum = hashlib.sha256(content).hexdigest()

        # Criar diretório se não existir
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Gerar nome único para arquivo
        file_id = str(uuid4())
        safe_filename = f"{file_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Salvar arquivo
        with open(file_path, "wb") as f:
            f.write(content)

        return file_path, file_size, mime_type, checksum

    @staticmethod
    def _get_document_type_from_mime(mime_type: str) -> DocumentType:
        """Converte MIME type para enum DocumentType."""
        mime_to_type = {
            "application/pdf": DocumentType.PDF,
            "application/msword": DocumentType.DOC,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocumentType.DOCX,
            "application/vnd.ms-excel": DocumentType.XLS,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": DocumentType.XLSX,
            "text/plain": DocumentType.TXT,
            "application/rtf": DocumentType.RTF,
            "image/jpeg": DocumentType.JPEG,
            "image/png": DocumentType.PNG,
            "image/gif": DocumentType.GIF,
            "image/tiff": DocumentType.TIFF,
            "application/zip": DocumentType.ZIP,
            "application/x-rar-compressed": DocumentType.RAR,
        }

        return mime_to_type.get(mime_type, DocumentType.OUTROS)

    @staticmethod
    async def _check_document_access(
        db: AsyncSession, document: Document, citizen_id: UUID
    ) -> bool:
        """Verifica se usuário tem acesso ao documento."""
        # Criador sempre tem acesso
        if document.created_by == citizen_id:
            return True

        # Documentos públicos
        if document.is_public:
            return True

        # Verificar permissões específicas
        permission = (
            db.query(DocumentPermission)
            .filter(
                DocumentPermission.document_id == document.id,
                DocumentPermission.user_id == citizen_id,
                or_(
                    DocumentPermission.expires_at.is_(None),
                    DocumentPermission.expires_at > datetime.utcnow(),
                ),
            )
            .first()
        )

        return permission is not None

    @staticmethod
    async def _document_to_dict(
        db: AsyncSession, document: Document, citizen_id: UUID
    ) -> Dict[str, Any]:
        """Converte modelo Document para dicionário com dados adicionais."""
        # Buscar criador
        creator = db.query(Citizen).filter(Citizen.id == document.created_by).first()

        return {
            "id": document.id,
            "title": document.title,
            "description": document.description,
            "category": document.category,
            "document_type": document.document_type,
            "status": document.status,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "checksum": document.checksum,
            "tags": document.tags or [],
            "is_public": document.is_public,
            "permission_level": document.permission_level,
            "download_count": document.download_count,
            "version": document.version,
            "created_by": document.created_by,
            "created_by_name": creator.full_name if creator else "Usuário desconhecido",
            "created_at": document.created_at,
            "updated_at": document.updated_at,
            "expires_at": document.expires_at,
            "folder_id": document.folder_id,
            "folder_name": document.folder.name if document.folder else None,
            "download_url": (
                f"/api/v1/documents/{document.id}/download"
                if document.file_path
                else None
            ),
            "preview_url": (
                f"/api/v1/documents/{document.id}/preview"
                if document.file_path
                else None
            ),
        }


"""
Serviço principal para gestão de documentos.

Este módulo implementa a lógica de negócio completa para:
- Upload e armazenamento seguro de documentos
- Controle de acesso e permissões granulares
- Organização hierárquica em pastas
- Versionamento e auditoria completa
- Busca avançada com filtros
- Compartilhamento seguro
- Templates de documentos
"""

import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.citizenship.models.citizen import Citizen

from ..models.documents_models import (
    Document,
    DocumentAuditLog,
    DocumentFolder,
    DocumentPermission,
    DocumentShare,
)
from ..schemas.documents import (
    DocumentCreate,
    DocumentFolderCreate,
    DocumentFolderRead,
    DocumentRead,
    DocumentSearchFilters,
    DocumentShareCreate,
    DocumentShareRead,
    DocumentStatus,
    DocumentType,
    DocumentUpdate,
    DocumentUpload,
)

logger = logging.getLogger(__name__)

# Configurações de upload
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "txt",
    "rtf",
    "jpg",
    "jpeg",
    "png",
    "gif",
    "tiff",
    "zip",
    "rar",
}
UPLOAD_DIR = "/opt/sila-system/uploads/documents"


class DocumentService:
    """Classe principal para operações documentais."""

    @staticmethod
    async def get_user_documents(
        db: AsyncSession,
        citizen_id: UUID,
        filters: Optional[DocumentSearchFilters] = None,
        page: int = 1,
        size: int = 20,
    ) -> Tuple[List[DocumentRead], int]:
        """
        Busca documentos do usuário com filtros aplicados.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão
            filters: Filtros de busca opcionais
            page: Página para paginação
            size: Tamanho da página

        Returns:
            Tupla com lista de documentos e total de registros
        """
        try:
            # Query base com relacionamentos
            query = (
                db.query(Document)
                .options(selectinload(Document.folder), selectinload(Document.creator))
                .filter(
                    or_(
                        Document.created_by == citizen_id,
                        Document.is_public == True,
                        # Documentos compartilhados com o usuário
                        Document.id.in_(
                            db.query(DocumentPermission.document_id).filter(
                                DocumentPermission.user_id == citizen_id,
                                or_(
                                    DocumentPermission.expires_at.is_(None),
                                    DocumentPermission.expires_at > datetime.utcnow(),
                                ),
                            )
                        ),
                    )
                )
            )

            # Aplicar filtros
            if filters:
                if filters.category:
                    query = query.filter(Document.category == filters.category)
                if filters.document_type:
                    query = query.filter(
                        Document.document_type == filters.document_type
                    )
                if filters.status:
                    query = query.filter(Document.status == filters.status)
                if filters.is_public is not None:
                    query = query.filter(Document.is_public == filters.is_public)
                if filters.folder_id:
                    query = query.filter(Document.folder_id == filters.folder_id)
                if filters.date_from:
                    query = query.filter(Document.created_at >= filters.date_from)
                if filters.date_to:
                    query = query.filter(Document.created_at <= filters.date_to)
                if filters.search_text:
                    search_filter = f"%{filters.search_text}%"
                    query = query.filter(
                        or_(
                            Document.title.ilike(search_filter),
                            Document.description.ilike(search_filter),
                        )
                    )

            # Ordenação e paginação
            total = query.count()
            documents = (
                query.order_by(desc(Document.created_at))
                .offset((page - 1) * size)
                .limit(size)
                .all()
            )

            # Converter para schema de leitura
            result = []
            for doc in documents:
                doc_dict = await DocumentService._document_to_dict(db, doc, citizen_id)
                result.append(DocumentRead(**doc_dict))

            return result, total

        except Exception as e:
            logger.error(f"Erro ao buscar documentos do usuário: {e}")
            raise

    @staticmethod
    async def upload_document(
        db: AsyncSession,
        file: UploadFile,
        upload_data: DocumentUpload,
        citizen_id: UUID,
    ) -> DocumentRead:
        """
        Realiza upload e armazenamento de documento.

        Args:
            db: Sessão do banco de dados
            file: Arquivo enviado
            upload_data: Dados do upload
            citizen_id: ID do cidadão

        Returns:
            Documento criado
        """
        try:
            # Validar arquivo
            (
                file_path,
                file_size,
                mime_type,
                checksum,
            ) = await DocumentService._validate_and_store_file(file)

            # Criar documento no banco
            document_data = DocumentCreate(
                title=upload_data.title,
                description=upload_data.description,
                category=upload_data.category,
                document_type=DocumentService._get_document_type_from_mime(mime_type),
                tags=upload_data.tags,
                is_public=upload_data.is_public,
                permission_level=upload_data.permission_level,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type,
                checksum=checksum,
                created_by=citizen_id,
            )

            # Se especificada pasta pai, verificar se existe e se usuário tem acesso
            if upload_data.parent_folder_id:
                folder = (
                    db.query(DocumentFolder)
                    .filter(DocumentFolder.id == upload_data.parent_folder_id)
                    .first()
                )

                if not folder:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Pasta não encontrada",
                    )

                if not folder.is_public and folder.created_by != citizen_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para usar esta pasta",
                    )

                document_data.folder_id = upload_data.parent_folder_id

            # Criar documento
            new_document = Document(**document_data.dict())
            db.add(new_document)
            db.commit()
            db.refresh(new_document)

            # Registrar ação na auditoria
            await DocumentService._log_audit_action(
                db,
                new_document.id,
                citizen_id,
                "UPLOAD",
                f"Documento '{upload_data.title}' enviado",
            )

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(
                db, new_document, citizen_id
            )

            logger.info(f"Documento enviado com sucesso: {new_document.id}")
            return DocumentRead(**doc_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro no upload de documento: {e}")
            raise

    @staticmethod
    async def get_document_by_id(
        db: AsyncSession, document_id: UUID, citizen_id: UUID
    ) -> Optional[DocumentRead]:
        """
        Busca documento específico por ID.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            citizen_id: ID do cidadão solicitante

        Returns:
            Dados do documento ou None se não encontrado/não autorizado
        """
        try:
            document = (
                db.query(Document)
                .options(
                    selectinload(Document.folder),
                    selectinload(Document.creator),
                    selectinload(Document.permissions),
                )
                .filter(Document.id == document_id)
                .first()
            )

            if not document:
                return None

            # Verificar permissões
            if not await DocumentService._check_document_access(
                db, document, citizen_id
            ):
                return None

            # Registrar acesso na auditoria
            await DocumentService._log_audit_action(
                db, document_id, citizen_id, "ACCESS", "Documento acessado"
            )

            # Incrementar contador de downloads se for acesso para download
            document.download_count += 1
            db.commit()

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(db, document, citizen_id)
            return DocumentRead(**doc_dict)

        except Exception as e:
            logger.error(f"Erro ao buscar documento por ID: {e}")
            raise

    @staticmethod
    async def update_document(
        db: AsyncSession,
        document_id: UUID,
        update_data: DocumentUpdate,
        citizen_id: UUID,
    ) -> Optional[DocumentRead]:
        """
        Atualiza metadados de documento.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            update_data: Dados para atualização
            citizen_id: ID do cidadão

        Returns:
            Documento atualizado ou None se não autorizado
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                return None

            # Verificar se usuário pode editar
            if document.created_by != citizen_id:
                # Verificar se tem permissão específica de edição
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_edit == True,
                        or_(
                            DocumentPermission.expires_at.is_(None),
                            DocumentPermission.expires_at > datetime.utcnow(),
                        ),
                    )
                    .first()
                )

                if not permission:
                    return None

            # Atualizar campos permitidos
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                if hasattr(document, field):
                    setattr(document, field, value)

            document.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(document)

            # Registrar alteração na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "UPDATE",
                f"Documento atualizado: {list(update_dict.keys())}",
            )

            # Converter para schema de leitura
            doc_dict = await DocumentService._document_to_dict(db, document, citizen_id)
            return DocumentRead(**doc_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar documento: {e}")
            raise

    @staticmethod
    async def delete_document(
        db: AsyncSession, document_id: UUID, citizen_id: UUID
    ) -> bool:
        """
        Remove documento (soft delete).

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            citizen_id: ID do cidadão

        Returns:
            True se removido com sucesso
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                return False

            # Verificar se usuário pode deletar
            if document.created_by != citizen_id:
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_delete == True,
                    )
                    .first()
                )

                if not permission:
                    return False

            # Soft delete - alterar status
            document.status = DocumentStatus.DELETED
            document.updated_at = datetime.utcnow()
            db.commit()

            # Registrar exclusão na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "DELETE",
                "Documento removido (soft delete)",
            )

            logger.info(f"Documento removido: {document_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao remover documento: {e}")
            raise

    @staticmethod
    async def create_folder(
        db: AsyncSession, folder_data: DocumentFolderCreate, citizen_id: UUID
    ) -> DocumentFolderRead:
        """
        Cria nova pasta para organização de documentos.

        Args:
            db: Sessão do banco de dados
            folder_data: Dados da pasta
            citizen_id: ID do cidadão

        Returns:
            Pasta criada
        """
        try:
            # Se especificada pasta pai, verificar se existe e se usuário tem acesso
            if folder_data.parent_folder_id:
                parent_folder = (
                    db.query(DocumentFolder)
                    .filter(DocumentFolder.id == folder_data.parent_folder_id)
                    .first()
                )

                if not parent_folder:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Pasta pai não encontrada",
                    )

                if (
                    not parent_folder.is_public
                    and parent_folder.created_by != citizen_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para criar pasta nesta localização",
                    )

            # Criar pasta
            new_folder = DocumentFolder(
                name=folder_data.name,
                description=folder_data.description,
                parent_folder_id=folder_data.parent_folder_id,
                is_public=folder_data.is_public,
                created_by=citizen_id,
            )

            db.add(new_folder)
            db.commit()
            db.refresh(new_folder)

            # Converter para schema de leitura
            folder_dict = {
                "id": new_folder.id,
                "name": new_folder.name,
                "description": new_folder.description,
                "parent_folder_id": new_folder.parent_folder_id,
                "is_public": new_folder.is_public,
                "created_by": new_folder.created_by,
                "created_at": new_folder.created_at,
                "updated_at": new_folder.updated_at,
                "document_count": 0,
            }

            logger.info(f"Pasta criada: {new_folder.id}")
            return DocumentFolderRead(**folder_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar pasta: {e}")
            raise

    @staticmethod
    async def share_document(
        db: AsyncSession,
        document_id: UUID,
        share_data: DocumentShareCreate,
        citizen_id: UUID,
    ) -> DocumentShareRead:
        """
        Cria link de compartilhamento para documento.

        Args:
            db: Sessão do banco de dados
            document_id: ID do documento
            share_data: Dados do compartilhamento
            citizen_id: ID do cidadão

        Returns:
            Link de compartilhamento criado
        """
        try:
            document = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Documento não encontrado",
                )

            # Verificar se usuário pode compartilhar
            if document.created_by != citizen_id:
                permission = (
                    db.query(DocumentPermission)
                    .filter(
                        DocumentPermission.document_id == document_id,
                        DocumentPermission.user_id == citizen_id,
                        DocumentPermission.can_share == True,
                    )
                    .first()
                )

                if not permission:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para compartilhar este documento",
                    )

            # Gerar token único
            share_token = secrets.token_urlsafe(32)

            # Criar compartilhamento
            new_share = DocumentShare(
                document_id=document_id,
                created_by=citizen_id,
                share_token=share_token,
                expires_at=share_data.expires_at,
                max_downloads=share_data.max_downloads,
                password_protected=share_data.password_protected,
                allow_download=share_data.allow_download,
            )

            db.add(new_share)
            db.commit()
            db.refresh(new_share)

            # Converter para schema de leitura
            share_dict = {
                "id": new_share.id,
                "document_id": new_share.document_id,
                "share_token": new_share.share_token,
                "created_by": new_share.created_by,
                "created_at": new_share.created_at,
                "download_count": new_share.download_count,
                "is_active": new_share.is_active,
                "expires_at": share_data.expires_at,
                "max_downloads": share_data.max_downloads,
                "password_protected": share_data.password_protected,
                "allow_download": share_data.allow_download,
            }

            # Registrar compartilhamento na auditoria
            await DocumentService._log_audit_action(
                db,
                document_id,
                citizen_id,
                "SHARE",
                f"Documento compartilhado com token: {share_token[:8]}...",
            )

            logger.info(f"Documento compartilhado: {document_id}")
            return DocumentShareRead(**share_dict)

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao compartilhar documento: {e}")
            raise

    @staticmethod
    async def get_document_statistics(
        db: AsyncSession, citizen_id: UUID
    ) -> Dict[str, Any]:
        """
        Obtém estatísticas de documentos do usuário.

        Args:
            db: Sessão do banco de dados
            citizen_id: ID do cidadão

        Returns:
            Estatísticas documentais
        """
        try:
            # Query para estatísticas gerais
            total_docs = (
                db.query(func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
            )

            docs_by_category = dict(
                db.query(Document.category, func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .group_by(Document.category)
                .all()
            )

            docs_by_status = dict(
                db.query(Document.status, func.count(Document.id))
                .filter(Document.created_by == citizen_id)
                .group_by(Document.status)
                .all()
            )

            total_size = (
                db.query(func.sum(Document.file_size))
                .filter(
                    Document.created_by == citizen_id,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
                or 0
            )

            # Documentos recentes (últimos 30 dias)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_uploads = (
                db.query(func.count(Document.id))
                .filter(
                    Document.created_by == citizen_id,
                    Document.created_at >= thirty_days_ago,
                    Document.status == DocumentStatus.ACTIVE,
                )
                .scalar()
            )

            # Top uploaders (outros usuários que compartilharam com ele)
            top_sharers = (
                db.query(
                    Citizen.full_name,
                    func.count(DocumentPermission.id).label("shared_count"),
                )
                .join(DocumentPermission, Citizen.id == DocumentPermission.granted_by)
                .filter(DocumentPermission.user_id == citizen_id)
                .group_by(Citizen.id, Citizen.full_name)
                .order_by(desc("shared_count"))
                .limit(5)
                .all()
            )

            return {
                "total_documents": total_docs,
                "documents_by_category": docs_by_category,
                "documents_by_status": docs_by_status,
                "total_size_bytes": total_size,
                "avg_file_size_bytes": total_size / max(total_docs, 1),
                "documents_by_type": {},  # Pode ser expandido
                "recent_uploads": recent_uploads,
                "top_uploaders": [
                    {"name": sharer.full_name, "shared_count": sharer.shared_count}
                    for sharer in top_sharers
                ],
            }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise

    # Métodos auxiliares privados

    @staticmethod
    async def _validate_and_store_file(file: UploadFile) -> Tuple[str, int, str, str]:
        """Valida e armazena arquivo enviado."""
        # Validar tamanho
        file_size = 0
        content = b""

        while chunk := await file.read(8192):
            file_size += len(chunk)
            content += chunk

            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Arquivo muito grande. Máximo: {MAX_FILE_SIZE} bytes",
                )

        # Validar extensão
        filename = file.filename or "unnamed_file"
        file_ext = filename.split(".")[-1].lower() if "." in filename else ""

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido: {file_ext}",
            )

        # Detectar MIME type
        import magic

        mime_type = magic.from_buffer(content, mime=True)

        # Calcular checksum
        checksum = hashlib.sha256(content).hexdigest()

        # Criar diretório se não existir
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Gerar nome único para arquivo
        file_id = str(uuid4())
        safe_filename = f"{file_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Salvar arquivo
        with open(file_path, "wb") as f:
            f.write(content)

        return file_path, file_size, mime_type, checksum

    @staticmethod
    def _get_document_type_from_mime(mime_type: str) -> DocumentType:
        """Converte MIME type para enum DocumentType."""
        mime_to_type = {
            "application/pdf": DocumentType.PDF,
            "application/msword": DocumentType.DOC,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocumentType.DOCX,
            "application/vnd.ms-excel": DocumentType.XLS,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": DocumentType.XLSX,
            "text/plain": DocumentType.TXT,
            "application/rtf": DocumentType.RTF,
            "image/jpeg": DocumentType.JPEG,
            "image/png": DocumentType.PNG,
            "image/gif": DocumentType.GIF,
            "image/tiff": DocumentType.TIFF,
            "application/zip": DocumentType.ZIP,
            "application/x-rar-compressed": DocumentType.RAR,
        }

        return mime_to_type.get(mime_type, DocumentType.OUTROS)

    @staticmethod
    async def _check_document_access(
        db: AsyncSession, document: Document, citizen_id: UUID
    ) -> bool:
        """Verifica se usuário tem acesso ao documento."""
        # Criador sempre tem acesso
        if document.created_by == citizen_id:
            return True

        # Documentos públicos
        if document.is_public:
            return True

        # Verificar permissões específicas
        permission = (
            db.query(DocumentPermission)
            .filter(
                DocumentPermission.document_id == document.id,
                DocumentPermission.user_id == citizen_id,
                or_(
                    DocumentPermission.expires_at.is_(None),
                    DocumentPermission.expires_at > datetime.utcnow(),
                ),
            )
            .first()
        )

        return permission is not None

    @staticmethod
    async def _document_to_dict(
        db: AsyncSession, document: Document, citizen_id: UUID
    ) -> Dict[str, Any]:
        """Converte modelo Document para dicionário com dados adicionais."""
        # Buscar criador
        creator = db.query(Citizen).filter(Citizen.id == document.created_by).first()

        return {
            "id": document.id,
            "title": document.title,
            "description": document.description,
            "category": document.category,
            "document_type": document.document_type,
            "status": document.status,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "checksum": document.checksum,
            "tags": document.tags or [],
            "is_public": document.is_public,
            "permission_level": document.permission_level,
            "download_count": document.download_count,
            "version": document.version,
            "created_by": document.created_by,
            "created_by_name": creator.full_name if creator else "Usuário desconhecido",
            "created_at": document.created_at,
            "updated_at": document.updated_at,
            "expires_at": document.expires_at,
            "folder_id": document.folder_id,
            "folder_name": document.folder.name if document.folder else None,
            "download_url": (
                f"/api/v1/documents/{document.id}/download"
                if document.file_path
                else None
            ),
            "preview_url": (
                f"/api/v1/documents/{document.id}/preview"
                if document.file_path
                else None
            ),
        }

    @staticmethod
    async def _log_audit_action(
        db: AsyncSession,
        document_id: UUID,
        user_id: UUID,
        action: str,
        details: str,
        ip_address: str = None,
        user_agent: str = None,
    ):
        """Registra ação na auditoria."""
        audit_log = DocumentAuditLog(
            document_id=document_id,
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.add(audit_log)
        db.commit()
