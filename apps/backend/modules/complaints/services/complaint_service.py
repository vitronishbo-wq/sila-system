"""Complaint service for handling complaint operations."""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core.exceptions import BusinessRuleError, ResourceNotFound
from modules.complaints.models.complaint import (
    Complaint,
    ComplaintStatus,
)
from modules.complaints.schemas.complaint import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)


class ComplaintService:
    """Service for managing complaints."""

    def __init__(self, db: Session):
        self.db = db

    def create_complaint(
        self, complaint_data: ComplaintCreate, citizen_id: int
    ) -> ComplaintResponse:
        """Create a new complaint."""
        try:
            complaint = Complaint(
                title=complaint_data.title,
                description=complaint_data.description,
                category=complaint_data.category,
                priority=complaint_data.priority,
                citizen_id=citizen_id,
                status=ComplaintStatus.OPEN,
            )

            self.db.add(complaint)
            self.db.commit()
            self.db.refresh(complaint)

            return ComplaintResponse.model_validate(complaint)

        except Exception as e:
            self.db.rollback()
            raise BusinessRuleError(f"Failed to create complaint: {str(e)}")

    def get_complaint(self, complaint_id: int) -> ComplaintResponse:
        """Get a complaint by ID."""
        complaint = (
            self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        )
        if not complaint:
            raise ResourceNotFound("Complaint", complaint_id)

        return ComplaintResponse.model_validate(complaint)

    def get_complaints(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ComplaintStatus] = None,
        citizen_id: Optional[int] = None,
    ) -> List[ComplaintResponse]:
        """Get complaints with filters."""
        query = self.db.query(Complaint)

        if status:
            query = query.filter(Complaint.status == status)

        if citizen_id:
            query = query.filter(Complaint.citizen_id == citizen_id)

        complaints = query.offset(skip).limit(limit).all()
        return [ComplaintResponse.model_validate(complaint) for complaint in complaints]

    def update_complaint(
        self, complaint_id: int, complaint_data: ComplaintUpdate
    ) -> ComplaintResponse:
        """Update a complaint."""
        complaint = (
            self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        )
        if not complaint:
            raise ResourceNotFound("Complaint", complaint_id)

        try:
            update_data = complaint_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(complaint, field, value)

            self.db.commit()
            self.db.refresh(complaint)

            return ComplaintResponse.model_validate(complaint)

        except Exception as e:
            self.db.rollback()
            raise BusinessRuleError(f"Failed to update complaint: {str(e)}")

    def delete_complaint(self, complaint_id: int) -> bool:
        """Delete a complaint."""
        complaint = (
            self.db.query(Complaint).filter(Complaint.id == complaint_id).first()
        )
        if not complaint:
            raise ResourceNotFound("Complaint", complaint_id)

        try:
            self.db.delete(complaint)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            raise BusinessRuleError(f"Failed to delete complaint: {str(e)}")

    def get_complaint_stats(self) -> Dict[str, Any]:
        """Get complaint statistics."""
        total = self.db.query(Complaint).count()
        open_count = (
            self.db.query(Complaint)
            .filter(Complaint.status == ComplaintStatus.OPEN)
            .count()
        )
        closed_count = (
            self.db.query(Complaint)
            .filter(Complaint.status == ComplaintStatus.CLOSED)
            .count()
        )

        return {
            "total": total,
            "open": open_count,
            "closed": closed_count,
            "resolution_rate": (closed_count / total * 100) if total > 0 else 0,
        }
