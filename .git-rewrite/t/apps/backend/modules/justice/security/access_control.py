"""Access control for justice module operations."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modules.justice.models import Case, LegalDocument
from modules.justice.security.audit_logger import (
    JusticeAuditAction,
    JusticeAuditLogger,
)


class JusticeAccessControl:
    """Access control service for justice operations."""

    # Role-based permissions
    ROLE_PERMISSIONS = {
        "admin": ["*"],  # Full access
        "judge": [
            "case:read",
            "case:update",
            "case:close",
            "event:read",
            "event:create",
            "event:update",
            "event:complete",
            "document:read",
            "document:create",
            "document:approve",
            "document:sign",
            "court:read",
        ],
        "prosecutor": [
            "case:read",
            "case:create",
            "case:update",
            "event:read",
            "event:create",
            "event:update",
            "document:read",
            "document:create",
            "court:read",
        ],
        "lawyer": [
            "case:read",
            "case:create",
            "event:read",
            "event:create",
            "document:read",
            "document:create",
            "court:read",
        ],
        "clerk": [
            "case:read",
            "case:create",
            "case:update",
            "event:read",
            "event:create",
            "event:update",
            "document:read",
            "document:create",
            "document:update",
            "court:read",
        ],
        "citizen": ["case:read_own", "document:read_own", "court:read"],
    }

    @staticmethod
    def check_permission(user_role: str, permission: str) -> bool:
        """Check if user role has specific permission."""
        if user_role not in JusticeAccessControl.ROLE_PERMISSIONS:
            return False

        permissions = JusticeAccessControl.ROLE_PERMISSIONS[user_role]
        return "*" in permissions or permission in permissions

    @staticmethod
    def require_permission(user_role: str, permission: str):
        """Require specific permission or raise HTTPException."""
        if not JusticeAccessControl.check_permission(user_role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão insuficiente. Requerida: {permission}",
            )

    @staticmethod
    def can_access_case(
        db: Session, case_id: int, user_id: int, user_role: str, action: str = "read"
    ) -> bool:
        """Check if user can access a specific case."""
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return False

        # Admin has full access
        if user_role == "admin":
            return True

        # Check role-based permissions
        permission = f"case:{action}"
        if not JusticeAccessControl.check_permission(user_role, permission):
            # Check if user has "own" permission and owns the case
            own_permission = f"case:{action}_own"
            if JusticeAccessControl.check_permission(user_role, own_permission):
                return (
                    case.created_by == user_id or case.plaintiff_citizen_id == user_id
                )
            return False

        # Confidential cases require special handling
        if case.is_confidential:
            if user_role not in ["admin", "judge"]:
                # Only creator or involved parties can access confidential cases
                return (
                    case.created_by == user_id
                    or case.plaintiff_citizen_id == user_id
                    or case.defendant_citizen_id == user_id
                )

        return True

    @staticmethod
    def can_access_document(
        db: Session,
        document_id: int,
        user_id: int,
        user_role: str,
        action: str = "read",
    ) -> bool:
        """Check if user can access a specific document."""
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )
        if not document:
            return False

        # Admin has full access
        if user_role == "admin":
            return True

        # Check role-based permissions
        permission = f"document:{action}"
        if not JusticeAccessControl.check_permission(user_role, permission):
            # Check if user has "own" permission and owns the document
            own_permission = f"document:{action}_own"
            if JusticeAccessControl.check_permission(user_role, own_permission):
                return document.created_by == user_id
            return False

        # Confidential documents require special handling
        if document.is_confidential:
            if user_role not in ["admin", "judge"]:
                return document.created_by == user_id

        # If document is linked to a case, check case access
        if document.case_id:
            return JusticeAccessControl.can_access_case(
                db, document.case_id, user_id, user_role, "read"
            )

        return True

    @staticmethod
    def enforce_case_access(
        db: Session,
        case_id: int,
        user_id: int,
        user_role: str,
        action: str = "read",
        ip_address: Optional[str] = None,
    ):
        """Enforce case access control with audit logging."""
        if not JusticeAccessControl.can_access_case(
            db, case_id, user_id, user_role, action
        ):
            # Log unauthorized access attempt
            JusticeAuditLogger.log_security_event(
                user_id=user_id,
                action=JusticeAuditAction.UNAUTHORIZED_ACCESS_ATTEMPT,
                resource_type="Case",
                resource_id=case_id,
                details=f"Tentativa de acesso não autorizado ao processo ID {case_id} com ação '{action}'",
                ip_address=ip_address,
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado ao processo",
            )

        # Log access for confidential cases
        case = db.query(Case).filter(Case.id == case_id).first()
        if case and case.is_confidential:
            JusticeAuditLogger.log_data_access(
                user_id=user_id,
                resource_type="Case",
                resource_id=case_id,
                access_type=action,
                is_confidential=True,
                details=f"Acesso a processo confidencial {case.case_number}",
            )

    @staticmethod
    def enforce_document_access(
        db: Session,
        document_id: int,
        user_id: int,
        user_role: str,
        action: str = "read",
        ip_address: Optional[str] = None,
    ):
        """Enforce document access control with audit logging."""
        if not JusticeAccessControl.can_access_document(
            db, document_id, user_id, user_role, action
        ):
            # Log unauthorized access attempt
            JusticeAuditLogger.log_security_event(
                user_id=user_id,
                action=JusticeAuditAction.UNAUTHORIZED_ACCESS_ATTEMPT,
                resource_type="LegalDocument",
                resource_id=document_id,
                details=f"Tentativa de acesso não autorizado ao documento ID {document_id} com ação '{action}'",
                ip_address=ip_address,
            )

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado ao documento",
            )

        # Log access for confidential documents
        document = (
            db.query(LegalDocument).filter(LegalDocument.id == document_id).first()
        )
        if document and document.is_confidential:
            JusticeAuditLogger.log_data_access(
                user_id=user_id,
                resource_type="LegalDocument",
                resource_id=document_id,
                access_type=action,
                is_confidential=True,
                details=f"Acesso a documento confidencial {document.document_number}",
            )

    @staticmethod
    def get_user_accessible_cases(
        db: Session, user_id: int, user_role: str, base_query
    ):
        """Filter cases query to only include accessible cases for user."""
        if user_role == "admin":
            return base_query

        if user_role == "citizen":
            # Citizens can only see cases they're involved in
            return base_query.filter(
                (Case.plaintiff_citizen_id == user_id)
                | (Case.defendant_citizen_id == user_id)
                | (Case.is_public == True)
            )

        if user_role in ["judge", "prosecutor", "lawyer", "clerk"]:
            # Legal professionals can see non-confidential cases or cases they created
            return base_query.filter(
                (Case.is_confidential == False) | (Case.created_by == user_id)
            )

        # Default: no access
        return base_query.filter(False)

    @staticmethod
    def get_user_accessible_documents(
        db: Session, user_id: int, user_role: str, base_query
    ):
        """Filter documents query to only include accessible documents for user."""
        if user_role == "admin":
            return base_query

        if user_role == "citizen":
            # Citizens can only see public documents or documents they requested
            return base_query.filter(
                (LegalDocument.is_public == True)
                | (LegalDocument.created_by == user_id)
            )

        if user_role in ["judge", "prosecutor", "lawyer", "clerk"]:
            # Legal professionals can see non-confidential documents or documents they created
            return base_query.filter(
                (LegalDocument.is_confidential == False)
                | (LegalDocument.created_by == user_id)
            )

        # Default: no access
        return base_query.filter(False)

    @staticmethod
    def mask_sensitive_data(data: dict, user_role: str) -> dict:
        """Mask sensitive data based on user role."""
        if user_role == "admin":
            return data  # Admin sees everything

        masked_data = data.copy()

        # Mask personal information for non-authorized users
        if user_role not in ["judge", "prosecutor"]:
            if "plaintiff_name" in masked_data and masked_data["plaintiff_name"]:
                masked_data["plaintiff_name"] = JusticeAccessControl._mask_name(
                    masked_data["plaintiff_name"]
                )
            if "defendant_name" in masked_data and masked_data["defendant_name"]:
                masked_data["defendant_name"] = JusticeAccessControl._mask_name(
                    masked_data["defendant_name"]
                )

        return masked_data

    @staticmethod
    def _mask_name(name: str) -> str:
        """Mask a person's name showing only initials."""
        if not name:
            return name

        parts = name.split()
        if len(parts) <= 1:
            return f"{name[0]}***"

        return f"{parts[0][0]}. {parts[-1][0]}***"
