"""Integration with citizenship module for justice operations."""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class CitizenshipIntegration:
    """Integration service for citizenship module."""

    @staticmethod
    def get_citizen_info(db: Session, citizen_id: int) -> Optional[Dict[str, Any]]:
        """Get citizen information for justice processes."""
        try:
            # TODO: Replace with actual citizenship module import when available
            # from modules.citizenship.services import CitizenService
            # citizen = CitizenService.get_citizen(db, citizen_id)

            # Mock implementation for now
            return {
                "id": citizen_id,
                "full_name": f"Cidadão {citizen_id}",
                "bi_number": f"00{citizen_id}LA2024",
                "nif": f"500{citizen_id}000",
                "birth_date": "1990-01-01",
                "address": "Luanda, Angola",
                "phone": "+244 900 000 000",
                "email": f"citizen{citizen_id}@example.com",
            }
        except Exception:
            return None

    @staticmethod
    def validate_citizen_exists(db: Session, citizen_id: int) -> bool:
        """Validate if citizen exists in the system."""
        citizen = CitizenshipIntegration.get_citizen_info(db, citizen_id)
        return citizen is not None

    @staticmethod
    def get_citizen_legal_history(db: Session, citizen_id: int) -> Dict[str, Any]:
        """Get citizen's legal history from justice system."""
        from modules.justice.models import Case

        # Get cases where citizen is involved
        plaintiff_cases = (
            db.query(Case).filter(Case.plaintiff_citizen_id == citizen_id).all()
        )
        defendant_cases = (
            db.query(Case).filter(Case.defendant_citizen_id == citizen_id).all()
        )

        return {
            "citizen_id": citizen_id,
            "total_cases": len(plaintiff_cases) + len(defendant_cases),
            "as_plaintiff": len(plaintiff_cases),
            "as_defendant": len(defendant_cases),
            "active_cases": len(
                [c for c in plaintiff_cases + defendant_cases if c.is_active]
            ),
            "recent_cases": [
                {
                    "case_number": case.case_number,
                    "title": case.title,
                    "type": case.case_type.value,
                    "status": case.status.value,
                    "role": "plaintiff" if case in plaintiff_cases else "defendant",
                    "filing_date": case.filing_date.isoformat(),
                }
                for case in sorted(
                    plaintiff_cases + defendant_cases,
                    key=lambda x: x.filing_date,
                    reverse=True,
                )[:5]
            ],
        }

    @staticmethod
    def create_citizen_certificate_request(
        db: Session, citizen_id: int, certificate_type: str, current_user_id: int
    ) -> Dict[str, Any]:
        """Create a certificate request for a citizen."""
        from modules.justice.models import (
            DocumentCategory,
            DocumentType,
        )
        from modules.justice.schemas import LegalDocumentCreate
        from modules.justice.services import LegalDocumentService

        # Validate citizen exists
        if not CitizenshipIntegration.validate_citizen_exists(db, citizen_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cidadão não encontrado"
            )

        # Map certificate types
        cert_type_mapping = {
            "antecedentes": DocumentType.CERTIFICATE,
            "criminal": DocumentType.CERTIFICATE,
            "protestos": DocumentType.CERTIFICATE,
        }

        doc_type = cert_type_mapping.get(
            certificate_type.lower(), DocumentType.CERTIFICATE
        )

        # Create certificate document
        cert_data = LegalDocumentCreate(
            title=f"Certidão de {certificate_type.title()}",
            description=f"Certidão de {certificate_type} solicitada para cidadão ID {citizen_id}",
            document_type=doc_type,
            category=DocumentCategory.CERTIFICATE,
            issuing_authority="Sistema de Justiça SILA",
            recipient=f"Cidadão ID {citizen_id}",
            validity_period_days=90,
            is_public=False,
            requires_signature=True,
        )

        certificate = LegalDocumentService.create_document(
            db, cert_data, current_user_id
        )

        return {
            "certificate_id": certificate.id,
            "document_number": certificate.document_number,
            "type": certificate_type,
            "citizen_id": citizen_id,
            "status": certificate.status.value,
            "created_at": certificate.created_at.isoformat(),
        }
