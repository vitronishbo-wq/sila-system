"""Legal document service for the justice module."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session

from core.logging.metrics import log_activity
from modules.justice.models import (
    Case,
    DocumentCategory,
    DocumentStatus,
    DocumentType,
    LegalDocument,
)
from modules.justice.schemas import LegalDocumentCreate, LegalDocumentUpdate


class LegalDocumentService:
    """Service for managing legal documents."""

    @staticmethod
    def generate_document_number(db: Session, document_type: DocumentType) -> str:
        """Generate unique document number."""
        year = datetime.now().year
        type_prefix = document_type.value[:3].upper()

        # Count existing documents this year
        count = (
            db.query(LegalDocument)
            .filter(
                func.extract("year", LegalDocument.created_at) == year,
                LegalDocument.document_type == document_type,
            )
            .count()
        )

        sequence = str(count + 1).zfill(4)
        return f"{type_prefix}-{year}-{sequence}"

    @staticmethod
    def create_document(
        db: Session, document_data: LegalDocumentCreate, current_user_id: int
    ) -> LegalDocument:
        """Create a new legal document."""
        try:
            # Verify case exists if provided
            if document_data.case_id:
                case = db.query(Case).filter(Case.id == document_data.case_id).first()
                if not case:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Processo não encontrado",
                    )

                # Check access permissions for confidential cases
                if case.is_confidential and case.created_by != current_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Sem permissão para adicionar documentos a processo confidencial",
                    )

            # Generate document number
            document_number = LegalDocumentService.generate_document_number(
                db, document_data.document_type
            )

            # Calculate expiry date if validity period is provided
            expiry_date = None
            if document_data.validity_period_days:
                issue_date = datetime.utcnow()
                expiry_date = issue_date + timedelta(
                    days=document_data.validity_period_days
                )

            # Create document
            db_document = LegalDocument(
                case_id=document_data.case_id,
                document_number=document_number,
                title=document_data.title,
                description=document_data.description,
                document_type=document_data.document_type,
                category=document_data.category,
                content=document_data.content,
                file_name=document_data.file_name,
                issuing_authority=document_data.issuing_authority,
                recipient=document_data.recipient,
                legal_basis=document_data.legal_basis,
                validity_period_days=document_data.validity_period_days,
                effective_date=document_data.effective_date,
                expiry_date=expiry_date,
                service_date=document_data.service_date,
                is_confidential=document_data.is_confidential,
                is_public=document_data.is_public,
                requires_signature=document_data.requires_signature,
                created_by=current_user_id,
            )

            db.add(db_document)
            db.commit()
            db.refresh(db_document)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="CREATE_LEGAL_DOCUMENT",
                resource_type="LegalDocument",
                resource_id=db_document.id,
                details=f"Documento criado: {document_number}",
            )

            return db_document

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar documento: {str(e)}",
            )

    @staticmethod
    def get_document(
        db: Session, document_id: int, current_user_id: int
    ) -> Optional[LegalDocument]:
        """Get a document by ID with access control."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )

        if not document:
            return None

        # Check access permissions
        if document.is_confidential and document.created_by != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado a documento confidencial",
            )

        # Check case access if document is linked to a case
        if document.case_id:
            case = db.query(Case).filter(Case.id == document.case_id).first()
            if case and case.is_confidential and case.created_by != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso negado a documento de processo confidencial",
                )

        return document

    @staticmethod
    def get_document_by_number(
        db: Session, document_number: str, current_user_id: int
    ) -> Optional[LegalDocument]:
        """Get a document by document number."""
        document = (
            db.query(LegalDocument)
            .filter(LegalDocument.document_number == document_number)
            .first()
        )

        if not document:
            return None

        # Check access permissions
        if document.is_confidential and document.created_by != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado a documento confidencial",
            )

        return document

    @staticmethod
    def get_case_documents(
        db: Session,
        case_id: int,
        current_user_id: int,
        skip: int = 0,
        limit: int = 100,
        document_type: Optional[DocumentType] = None,
        category: Optional[DocumentCategory] = None,
        status: Optional[DocumentStatus] = None,
    ) -> List[LegalDocument]:
        """Get documents for a specific case."""
        # Check case access
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Processo não encontrado"
            )

        if case.is_confidential and case.created_by != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado a processo confidencial",
            )

        query = db.query(LegalDocument).filter(LegalDocument.case_id == case_id)

        # Apply filters
        if document_type:
            query = query.filter(LegalDocument.document_type == document_type)

        if category:
            query = query.filter(LegalDocument.category == category)

        if status:
            query = query.filter(LegalDocument.status == status)

        return (
            query.order_by(desc(LegalDocument.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_documents(
        db: Session,
        current_user_id: int,
        skip: int = 0,
        limit: int = 100,
        document_type: Optional[DocumentType] = None,
        category: Optional[DocumentCategory] = None,
        status: Optional[DocumentStatus] = None,
        search: Optional[str] = None,
        case_id: Optional[int] = None,
    ) -> List[LegalDocument]:
        """Get documents with filtering options."""
        query = db.query(LegalDocument)

        # Filter out confidential documents unless user has access
        query = query.filter(
            or_(
                LegalDocument.is_confidential == False,
                LegalDocument.created_by == current_user_id,
            )
        )

        # Apply filters
        if document_type:
            query = query.filter(LegalDocument.document_type == document_type)

        if category:
            query = query.filter(LegalDocument.category == category)

        if status:
            query = query.filter(LegalDocument.status == status)

        if case_id:
            query = query.filter(LegalDocument.case_id == case_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    LegalDocument.title.ilike(search_term),
                    LegalDocument.description.ilike(search_term),
                    LegalDocument.document_number.ilike(search_term),
                    LegalDocument.content.ilike(search_term),
                )
            )

        return (
            query.order_by(desc(LegalDocument.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_document(
        db: Session,
        document_id: int,
        document_update: LegalDocumentUpdate,
        current_user_id: int,
    ) -> Optional[LegalDocument]:
        """Update a legal document."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )

        if not document:
            return None

        # Check permissions
        if document.is_confidential and document.created_by != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para editar documento confidencial",
            )

        try:
            # Update fields
            update_data = document_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(document, field, value)

            document.updated_by = current_user_id

            db.commit()
            db.refresh(document)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="UPDATE_LEGAL_DOCUMENT",
                resource_type="LegalDocument",
                resource_id=document.id,
                details=f"Documento atualizado: {document.document_number}",
            )

            return document

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar documento: {str(e)}",
            )

    @staticmethod
    def approve_document(
        db: Session,
        document_id: int,
        current_user_id: int,
        approval_notes: Optional[str] = None,
    ) -> Optional[LegalDocument]:
        """Approve a document."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )

        if not document:
            return None

        if document.status != DocumentStatus.PENDING_REVIEW:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas documentos pendentes podem ser aprovados",
            )

        try:
            document.status = DocumentStatus.APPROVED
            document.approved_by = current_user_id
            document.updated_by = current_user_id

            if approval_notes:
                document.description = (
                    f"{document.description}\n\nAprovação: {approval_notes}"
                )

            db.commit()
            db.refresh(document)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="APPROVE_LEGAL_DOCUMENT",
                resource_type="LegalDocument",
                resource_id=document.id,
                details=f"Documento aprovado: {document.document_number}",
            )

            return document

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao aprovar documento: {str(e)}",
            )

    @staticmethod
    def issue_document(
        db: Session, document_id: int, current_user_id: int
    ) -> Optional[LegalDocument]:
        """Issue an approved document."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )

        if not document:
            return None

        if document.status != DocumentStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas documentos aprovados podem ser emitidos",
            )

        try:
            document.status = DocumentStatus.ISSUED
            document.issue_date = datetime.utcnow()
            document.updated_by = current_user_id

            # Set effective date if not already set
            if not document.effective_date:
                document.effective_date = datetime.utcnow()

            db.commit()
            db.refresh(document)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="ISSUE_LEGAL_DOCUMENT",
                resource_type="LegalDocument",
                resource_id=document.id,
                details=f"Documento emitido: {document.document_number}",
            )

            return document

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao emitir documento: {str(e)}",
            )

    @staticmethod
    def sign_document(
        db: Session, document_id: int, current_user_id: int, digital_signature: str
    ) -> Optional[LegalDocument]:
        """Sign a document digitally."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )

        if not document:
            return None

        if not document.requires_signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Documento não requer assinatura",
            )

        if document.is_signed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Documento já está assinado",
            )

        try:
            document.is_signed = True
            document.digital_signature = digital_signature
            document.updated_by = current_user_id

            db.commit()
            db.refresh(document)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="SIGN_LEGAL_DOCUMENT",
                resource_type="LegalDocument",
                resource_id=document.id,
                details=f"Documento assinado: {document.document_number}",
            )

            return document

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao assinar documento: {str(e)}",
            )

    @staticmethod
    def get_expiring_documents(
        db: Session, days_threshold: int = 30
    ) -> List[LegalDocument]:
        """Get documents expiring within threshold days."""
        threshold_date = datetime.utcnow() + timedelta(days=days_threshold)

        return (
            db.query(LegalDocument)
            .filter(
                LegalDocument.status == DocumentStatus.ISSUED,
                LegalDocument.expiry_date.isnot(None),
                LegalDocument.expiry_date <= threshold_date,
                LegalDocument.expiry_date > datetime.utcnow(),
            )
            .order_by(LegalDocument.expiry_date)
            .all()
        )

    @staticmethod
    def get_expired_documents(db: Session) -> List[LegalDocument]:
        """Get expired documents."""
        return (
            db.query(LegalDocument)
            .filter(
                LegalDocument.expiry_date.isnot(None),
                LegalDocument.expiry_date < datetime.utcnow(),
                LegalDocument.status != DocumentStatus.EXPIRED,
            )
            .order_by(LegalDocument.expiry_date)
            .all()
        )

    @staticmethod
    def get_document_statistics(
        db: Session, case_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get document statistics."""
        query = db.query(LegalDocument)

        if case_id:
            query = query.filter(LegalDocument.case_id == case_id)

        total_documents = query.count()
        issued_documents = query.filter(
            LegalDocument.status == DocumentStatus.ISSUED
        ).count()
        pending_documents = query.filter(
            LegalDocument.status == DocumentStatus.PENDING_REVIEW
        ).count()

        # Documents by type
        documents_by_type = {}
        for doc_type in DocumentType:
            count = query.filter(LegalDocument.document_type == doc_type).count()
            documents_by_type[doc_type.value] = count

        # Documents by category
        documents_by_category = {}
        for category in DocumentCategory:
            count = query.filter(LegalDocument.category == category).count()
            documents_by_category[category.value] = count

        # Expiring documents (next 30 days)
        expiring_count = query.filter(
            LegalDocument.status == DocumentStatus.ISSUED,
            LegalDocument.expiry_date.isnot(None),
            LegalDocument.expiry_date.between(
                datetime.utcnow(), datetime.utcnow() + timedelta(days=30)
            ),
        ).count()

        # Expired documents
        expired_count = query.filter(
            LegalDocument.expiry_date.isnot(None),
            LegalDocument.expiry_date < datetime.utcnow(),
        ).count()

        return {
            "total_documents": total_documents,
            "issued_documents": issued_documents,
            "pending_documents": pending_documents,
            "documents_by_type": documents_by_type,
            "documents_by_category": documents_by_category,
            "expiring_documents": expiring_count,
            "expired_documents": expired_count,
            "issuance_rate": (
                (issued_documents / total_documents * 100) if total_documents > 0 else 0
            ),
        }
