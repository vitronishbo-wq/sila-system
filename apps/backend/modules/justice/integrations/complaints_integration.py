"""Integration with complaints module for justice operations."""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class ComplaintsIntegration:
    """Integration service for complaints module."""

    @staticmethod
    def get_complaint_info(db: Session, complaint_id: int) -> Optional[Dict[str, Any]]:
        """Get complaint information for case creation."""
        try:
            # TODO: Replace with actual complaints module import when available
            # from modules.complaints.services import ComplaintService
            # complaint = ComplaintService.get_complaint(db, complaint_id)

            # Mock implementation for now
            return {
                "id": complaint_id,
                "title": f"Denúncia #{complaint_id}",
                "description": f"Descrição da denúncia {complaint_id}",
                "complainant_id": 1001,
                "defendant_name": "João Silva",
                "category": "civil",
                "status": "under_investigation",
                "created_at": "2024-01-01T10:00:00",
                "location": "Luanda",
                "evidence_files": [],
            }
        except Exception:
            return None

    @staticmethod
    def convert_complaint_to_case(
        db: Session, complaint_id: int, court_id: int, current_user_id: int
    ) -> Dict[str, Any]:
        """Convert a complaint into a legal case."""
        from modules.justice.models import CaseType
        from modules.justice.schemas import CaseCreate
        from modules.justice.services import CaseService

        # Get complaint information
        complaint = ComplaintsIntegration.get_complaint_info(db, complaint_id)
        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Denúncia não encontrada"
            )

        # Map complaint category to case type
        case_type_mapping = {
            "civil": CaseType.CIVIL,
            "criminal": CaseType.CRIMINAL,
            "administrative": CaseType.ADMINISTRATIVE,
            "family": CaseType.FAMILY,
            "labor": CaseType.LABOR,
            "commercial": CaseType.COMMERCIAL,
        }

        case_type = case_type_mapping.get(complaint["category"], CaseType.CIVIL)

        # Create case from complaint
        case_data = CaseCreate(
            title=f"Processo originado da {complaint['title']}",
            description=f"Processo judicial iniciado com base na denúncia #{complaint_id}.\n\n"
            f"Descrição original: {complaint['description']}",
            case_type=case_type,
            plaintiff_citizen_id=complaint["complainant_id"],
            defendant_name=complaint["defendant_name"],
            court_id=court_id,
            is_public=False,
            is_confidential=False,
        )

        case = CaseService.create_case(db, case_data, current_user_id)

        # Update complaint status to indicate it became a case
        # TODO: Implement actual complaint status update
        # ComplaintService.update_status(db, complaint_id, "converted_to_case")

        return {
            "case_id": case.id,
            "case_number": case.case_number,
            "complaint_id": complaint_id,
            "conversion_date": case.created_at.isoformat(),
            "message": f"Denúncia #{complaint_id} convertida em processo {case.case_number}",
        }

    @staticmethod
    def get_complaints_ready_for_conversion(db: Session) -> List[Dict[str, Any]]:
        """Get complaints that are ready to be converted to cases."""
        # TODO: Implement actual query to complaints module
        # This would typically filter complaints with status "investigation_complete"
        # or "requires_legal_action"

        # Mock implementation
        return [
            {
                "id": 1001,
                "title": "Denúncia de Fraude Comercial",
                "category": "commercial",
                "status": "investigation_complete",
                "complainant_id": 2001,
                "created_at": "2024-01-15T09:00:00",
                "priority": "high",
            },
            {
                "id": 1002,
                "title": "Conflito de Propriedade",
                "category": "civil",
                "status": "requires_legal_action",
                "complainant_id": 2002,
                "created_at": "2024-01-20T14:30:00",
                "priority": "medium",
            },
        ]

    @staticmethod
    def link_case_to_complaint(
        db: Session, case_id: int, complaint_id: int, current_user_id: int
    ) -> Dict[str, Any]:
        """Link an existing case to a complaint."""

        # Verify case exists
        case = CaseService.get_case(db, case_id, current_user_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Processo não encontrado"
            )

        # Verify complaint exists
        complaint = ComplaintsIntegration.get_complaint_info(db, complaint_id)
        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Denúncia não encontrada"
            )

        # Update case description to include complaint reference
        case.description = f"{case.description}\n\nRelacionado à denúncia #{complaint_id}: {complaint['title']}"
        db.commit()

        return {
            "case_id": case_id,
            "case_number": case.case_number,
            "complaint_id": complaint_id,
            "linked_at": case.updated_at.isoformat(),
            "message": f"Processo {case.case_number} vinculado à denúncia #{complaint_id}",
        }

    @staticmethod
    def get_case_complaints_history(db: Session, case_id: int) -> List[Dict[str, Any]]:
        """Get complaints history related to a case."""
        # TODO: Implement actual query to find complaints linked to case
        # This would search for complaints mentioned in case description or
        # stored in a separate linking table

        # Mock implementation
        return [
            {
                "complaint_id": 1001,
                "title": "Denúncia Original",
                "status": "converted_to_case",
                "created_at": "2024-01-15T09:00:00",
                "relationship": "originated_from",
            }
        ]
