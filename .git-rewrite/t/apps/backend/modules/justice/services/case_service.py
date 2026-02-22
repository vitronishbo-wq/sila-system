"""Service layer for case management with business logic."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud_new import get_case_crud
from ..models.case import CasePriority, CaseStatus
from ..schemas.justice_crud import (
    CaseCreate,
    CaseFilter,
    CaseInDB,
    CaseUpdate,
)


class CaseService:
    """Service class for case business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_case_crud(db)

    async def create_case(self, case_data: CaseCreate, user_id: int) -> CaseInDB:
        """Create a new case with business validation."""
        # Business logic: Validate case data
        if case_data.hearing_date and case_data.hearing_date <= datetime.now():
            raise ValueError("Hearing date must be in the future")

        # Business logic: Set priority based on case type if not specified
        if not case_data.priority or case_data.priority == CasePriority.MEDIUM:
            case_data.priority = self._determine_default_priority(case_data.case_type)

        return await self.crud.create(case_data, created_by=user_id)

    async def get_case(self, case_id: int, user_id: int) -> Optional[CaseInDB]:
        """Get a case with access control."""
        case = await self.crud.get(case_id)
        if case:
            # Business logic: Check access permissions
            if not self._can_access_case(case, user_id):
                return None
        return case

    async def get_cases(
        self, skip: int = 0, limit: int = 100, user_id: int = None
    ) -> List[CaseInDB]:
        """Get cases with optional user filtering."""
        cases = await self.crud.get_multi(skip=skip, limit=limit)

        # Business logic: Filter cases based on user access
        if user_id:
            cases = [case for case in cases if self._can_access_case(case, user_id)]

        return cases

    async def update_case(
        self, case_id: int, case_data: CaseUpdate, user_id: int
    ) -> Optional[CaseInDB]:
        """Update a case with business validation."""
        case = await self.crud.get(case_id)
        if not case:
            return None

        # Business logic: Check update permissions
        if not self._can_update_case(case, user_id):
            raise PermissionError("User cannot update this case")

        # Business logic: Validate status transitions
        if case_data.status and not self._is_valid_status_transition(
            case.status, case_data.status
        ):
            raise ValueError(
                f"Invalid status transition from {case.status} to {case_data.status}"
            )

        return await self.crud.update(case, case_data)

    async def delete_case(self, case_id: int, user_id: int) -> bool:
        """Delete a case with business validation."""
        case = await self.crud.get(case_id)
        if not case:
            return False

        # Business logic: Only allow deletion of registered cases
        if case.status != CaseStatus.REGISTERED:
            raise ValueError("Only registered cases can be deleted")

        # Business logic: Check delete permissions
        if not self._can_delete_case(case, user_id):
            raise PermissionError("User cannot delete this case")

        return await self.crud.delete(case_id)

    async def search_cases(
        self, filters: CaseFilter, skip: int = 0, limit: int = 100, user_id: int = None
    ) -> List[CaseInDB]:
        """Search cases with filters."""
        cases = await self.crud.get_filtered(filters, skip, limit)

        # Business logic: Filter cases based on user access
        if user_id:
            cases = [case for case in cases if self._can_access_case(case, user_id)]

        return cases

    async def get_case_statistics(
        self, court_id: Optional[int] = None, user_id: int = None
    ) -> Dict[str, Any]:
        """Get case statistics with access control."""
        stats = await self.crud.get_statistics(court_id)

        # Business logic: Apply user-specific filtering if needed
        if user_id:
            # This would need to be implemented based on user permissions
            pass

        return stats

    # Business logic methods
    def _determine_default_priority(self, case_type: str) -> CasePriority:
        """Determine default priority based on case type."""
        high_priority_types = ["criminal", "family"]
        if case_type in high_priority_types:
            return CasePriority.HIGH
        return CasePriority.MEDIUM

    def _can_access_case(self, case: CaseInDB, user_id: int) -> bool:
        """Check if user can access the case."""
        # Business logic: Case creator can always access
        if case.created_by == user_id:
            return True

        # Business logic: Public cases can be accessed by anyone
        if case.is_public and not case.is_confidential:
            return True

        # Business logic: Additional access rules would go here
        # (e.g., role-based access, court assignment, etc.)
        return False

    def _can_update_case(self, case: CaseInDB, user_id: int) -> bool:
        """Check if user can update the case."""
        # Business logic: Case creator can update
        if case.created_by == user_id:
            return True

        # Business logic: Additional update rules would go here
        return False

    def _can_delete_case(self, case: CaseInDB, user_id: int) -> bool:
        """Check if user can delete the case."""
        # Business logic: Only case creator can delete
        if case.created_by == user_id:
            return True

        return False

    def _is_valid_status_transition(
        self, current_status: CaseStatus, new_status: CaseStatus
    ) -> bool:
        """Validate case status transitions."""
        valid_transitions = {
            CaseStatus.REGISTERED: [CaseStatus.IN_PROGRESS, CaseStatus.ARCHIVED],
            CaseStatus.IN_PROGRESS: [
                CaseStatus.SUSPENDED,
                CaseStatus.CONCLUDED,
                CaseStatus.ARCHIVED,
            ],
            CaseStatus.SUSPENDED: [
                CaseStatus.IN_PROGRESS,
                CaseStatus.CONCLUDED,
                CaseStatus.ARCHIVED,
            ],
            CaseStatus.CONCLUDED: [CaseStatus.APPEALED, CaseStatus.ARCHIVED],
            CaseStatus.APPEALED: [
                CaseStatus.IN_PROGRESS,
                CaseStatus.CONCLUDED,
                CaseStatus.ARCHIVED,
            ],
            CaseStatus.ARCHIVED: [],  # Archived cases cannot change status
        }

        return new_status in valid_transitions.get(current_status, [])

    @staticmethod
    async def get_case_statistics(
        db: AsyncSession, court_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Static method for backward compatibility."""
        service = CaseService(db)
        return await service.get_case_statistics(court_id)
