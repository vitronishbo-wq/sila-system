"""
Governance module repository - Data access layer.

This repository handles all database operations for the Governance module
using SQLAlchemy 2.x async patterns, following the Health module pattern.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.governance.models import (
    CouncilMeeting,
    Decision,
    Institution,
    Mandate,
)


class GovernanceRepository:
    """Repository for Governance module database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # Institutions
    # ========================================================================

    async def create_institution(
        self,
        name: str,
        acronym: Optional[str] = None,
        institution_type: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        description: Optional[str] = None,
        founding_date: Optional[datetime] = None,
        website: Optional[str] = None,
        contact_info: Optional[dict] = None,
        leadership: Optional[dict] = None,
        parent_institution_id: Optional[UUID] = None,
    ) -> Institution:
        """Create a new institution."""
        institution = Institution(
            name=name,
            acronym=acronym,
            institution_type=institution_type,
            jurisdiction=jurisdiction,
            description=description,
            founding_date=founding_date,
            website=website,
            contact_info=contact_info,
            leadership=leadership,
            parent_institution_id=parent_institution_id,
        )
        self.db.add(institution)
        await self.db.commit()
        await self.db.refresh(institution)
        return institution

    async def get_institution(self, institution_id: UUID) -> Optional[Institution]:
        """Get an institution by ID (excludes soft-deleted)."""
        stmt = select(Institution).where(
            and_(Institution.id == institution_id, Institution.deleted_at.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_institutions(
        self,
        institution_type: Optional[str] = None,
        parent_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Institution]:
        """List institutions with optional filters (excludes soft-deleted)."""
        stmt = select(Institution).where(Institution.deleted_at.is_(None))

        if institution_type:
            stmt = stmt.where(Institution.institution_type == institution_type)
        if parent_id is not None:
            stmt = stmt.where(Institution.parent_institution_id == parent_id)

        stmt = stmt.offset(skip).limit(limit).order_by(Institution.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_institutions(
        self,
        institution_type: Optional[str] = None,
        parent_id: Optional[UUID] = None,
    ) -> int:
        """Count institutions with optional filters (excludes soft-deleted)."""
        stmt = select(func.count(Institution.id)).where(
            Institution.deleted_at.is_(None)
        )

        if institution_type:
            stmt = stmt.where(Institution.institution_type == institution_type)
        if parent_id is not None:
            stmt = stmt.where(Institution.parent_institution_id == parent_id)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def update_institution(
        self,
        institution_id: UUID,
        name: Optional[str] = None,
        acronym: Optional[str] = None,
        institution_type: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        description: Optional[str] = None,
        website: Optional[str] = None,
        contact_info: Optional[dict] = None,
        leadership: Optional[dict] = None,
    ) -> Optional[Institution]:
        """Update an institution."""
        institution = await self.get_institution(institution_id)
        if not institution:
            return None

        if name is not None:
            institution.name = name
        if acronym is not None:
            institution.acronym = acronym
        if institution_type is not None:
            institution.institution_type = institution_type
        if jurisdiction is not None:
            institution.jurisdiction = jurisdiction
        if description is not None:
            institution.description = description
        if website is not None:
            institution.website = website
        if contact_info is not None:
            institution.contact_info = contact_info
        if leadership is not None:
            institution.leadership = leadership

        await self.db.commit()
        await self.db.refresh(institution)
        return institution

    async def delete_institution(self, institution_id: UUID) -> bool:
        """Soft delete an institution."""
        institution = await self.get_institution(institution_id)
        if not institution:
            return False

        institution.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
        return True

    # ========================================================================
    # Mandates
    # ========================================================================

    async def create_mandate(
        self,
        title: str,
        description: Optional[str] = None,
        mandate_type: Optional[str] = None,
        issuing_authority: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: str = "active",
        scope: Optional[dict] = None,
        related_documents: Optional[dict] = None,
        institution_id: Optional[UUID] = None,
    ) -> Mandate:
        """Create a new mandate."""
        mandate = Mandate(
            title=title,
            description=description,
            mandate_type=mandate_type,
            issuing_authority=issuing_authority,
            start_date=start_date,
            end_date=end_date,
            status=status,
            scope=scope,
            related_documents=related_documents,
            institution_id=institution_id,
        )
        self.db.add(mandate)
        await self.db.commit()
        await self.db.refresh(mandate)
        return mandate

    async def get_mandate(self, mandate_id: UUID) -> Optional[Mandate]:
        """Get a mandate by ID (excludes soft-deleted)."""
        stmt = (
            select(Mandate)
            .options(
                selectinload(Mandate.institution),
            )
            .where(and_(Mandate.id == mandate_id, Mandate.deleted_at.is_(None)))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_mandates(
        self,
        institution_id: Optional[UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Mandate]:
        """List mandates with optional filters (excludes soft-deleted)."""
        stmt = (
            select(Mandate)
            .options(
                selectinload(Mandate.institution),
            )
            .where(Mandate.deleted_at.is_(None))
        )

        if institution_id:
            stmt = stmt.where(Mandate.institution_id == institution_id)
        if status:
            stmt = stmt.where(Mandate.status == status)

        stmt = stmt.offset(skip).limit(limit).order_by(Mandate.start_date.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_mandates(
        self,
        institution_id: Optional[UUID] = None,
        status: Optional[str] = None,
    ) -> int:
        """Count mandates with optional filters (excludes soft-deleted)."""
        stmt = select(func.count(Mandate.id)).where(Mandate.deleted_at.is_(None))

        if institution_id:
            stmt = stmt.where(Mandate.institution_id == institution_id)
        if status:
            stmt = stmt.where(Mandate.status == status)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def update_mandate(
        self,
        mandate_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[Mandate]:
        """Update a mandate."""
        mandate = await self.get_mandate(mandate_id)
        if not mandate:
            return None

        if title is not None:
            mandate.title = title
        if description is not None:
            mandate.description = description
        if status is not None:
            mandate.status = status
        if end_date is not None:
            mandate.end_date = end_date

        await self.db.commit()
        await self.db.refresh(mandate)
        return mandate

    async def delete_mandate(self, mandate_id: UUID) -> bool:
        """Soft delete a mandate."""
        mandate = await self.get_mandate(mandate_id)
        if not mandate:
            return False

        mandate.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True

    # ========================================================================
    # Decisions
    # ========================================================================

    async def create_decision(
        self,
        title: str,
        description: Optional[str] = None,
        decision_type: Optional[str] = None,
        status: str = "proposed",
        voting_record: Optional[dict] = None,
        meeting_id: Optional[UUID] = None,
        effective_date: Optional[datetime] = None,
        expiration_date: Optional[datetime] = None,
        related_documents: Optional[dict] = None,
    ) -> Decision:
        """Create a new decision."""
        decision = Decision(
            title=title,
            description=description,
            decision_type=decision_type,
            status=status,
            voting_record=voting_record,
            meeting_id=meeting_id,
            effective_date=effective_date,
            expiration_date=expiration_date,
            related_documents=related_documents,
        )
        self.db.add(decision)
        await self.db.commit()
        await self.db.refresh(decision)
        return decision

    async def get_decision(self, decision_id: UUID) -> Optional[Decision]:
        """Get a decision by ID (excludes soft-deleted)."""
        stmt = (
            select(Decision)
            .options(
                selectinload(Decision.meeting),
            )
            .where(and_(Decision.id == decision_id, Decision.deleted_at.is_(None)))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_decisions(
        self,
        meeting_id: Optional[UUID] = None,
        status: Optional[str] = None,
        decision_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Decision]:
        """List decisions with optional filters (excludes soft-deleted)."""
        stmt = (
            select(Decision)
            .options(
                selectinload(Decision.meeting),
            )
            .where(Decision.deleted_at.is_(None))
        )

        if meeting_id:
            stmt = stmt.where(Decision.meeting_id == meeting_id)
        if status:
            stmt = stmt.where(Decision.status == status)
        if decision_type:
            stmt = stmt.where(Decision.decision_type == decision_type)

        stmt = stmt.offset(skip).limit(limit).order_by(Decision.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_decisions(
        self,
        meeting_id: Optional[UUID] = None,
        status: Optional[str] = None,
        decision_type: Optional[str] = None,
    ) -> int:
        """Count decisions with optional filters (excludes soft-deleted)."""
        stmt = select(func.count(Decision.id)).where(Decision.deleted_at.is_(None))

        if meeting_id:
            stmt = stmt.where(Decision.meeting_id == meeting_id)
        if status:
            stmt = stmt.where(Decision.status == status)
        if decision_type:
            stmt = stmt.where(Decision.decision_type == decision_type)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def update_decision(
        self,
        decision_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        voting_record: Optional[dict] = None,
    ) -> Optional[Decision]:
        """Update a decision."""
        decision = await self.get_decision(decision_id)
        if not decision:
            return None

        if title is not None:
            decision.title = title
        if description is not None:
            decision.description = description
        if status is not None:
            decision.status = status
        if voting_record is not None:
            decision.voting_record = voting_record

        await self.db.commit()
        await self.db.refresh(decision)
        return decision

    async def delete_decision(self, decision_id: UUID) -> bool:
        """Soft delete a decision."""
        decision = await self.get_decision(decision_id)
        if not decision:
            return False

        decision.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True

    # ========================================================================
    # Council Meetings
    # ========================================================================

    async def create_council_meeting(
        self,
        title: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: str = "scheduled",
        agenda: Optional[dict] = None,
        minutes: Optional[dict] = None,
        decisions: Optional[dict] = None,
        participants: Optional[dict] = None,
        council_id: Optional[UUID] = None,
    ) -> CouncilMeeting:
        """Create a new council meeting."""
        meeting = CouncilMeeting(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            status=status,
            agenda=agenda,
            minutes=minutes,
            decisions=decisions,
            participants=participants,
            council_id=council_id,
        )
        self.db.add(meeting)
        await self.db.commit()
        await self.db.refresh(meeting)
        return meeting

    async def get_council_meeting(self, meeting_id: UUID) -> Optional[CouncilMeeting]:
        """Get a council meeting by ID (excludes soft-deleted)."""
        stmt = select(CouncilMeeting).where(
            and_(CouncilMeeting.id == meeting_id, CouncilMeeting.deleted_at.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_council_meetings(
        self,
        council_id: Optional[UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[CouncilMeeting]:
        """List council meetings with optional filters (excludes soft-deleted)."""
        stmt = select(CouncilMeeting).where(CouncilMeeting.deleted_at.is_(None))

        if council_id:
            stmt = stmt.where(CouncilMeeting.council_id == council_id)
        if status:
            stmt = stmt.where(CouncilMeeting.status == status)

        stmt = stmt.offset(skip).limit(limit).order_by(CouncilMeeting.start_time.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_council_meetings(
        self,
        council_id: Optional[UUID] = None,
        status: Optional[str] = None,
    ) -> int:
        """Count council meetings with optional filters (excludes soft-deleted)."""
        stmt = select(func.count(CouncilMeeting.id)).where(
            CouncilMeeting.deleted_at.is_(None)
        )

        if council_id:
            stmt = stmt.where(CouncilMeeting.council_id == council_id)
        if status:
            stmt = stmt.where(CouncilMeeting.status == status)

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    async def update_council_meeting(
        self,
        meeting_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        end_time: Optional[datetime] = None,
        minutes: Optional[dict] = None,
    ) -> Optional[CouncilMeeting]:
        """Update a council meeting."""
        meeting = await self.get_council_meeting(meeting_id)
        if not meeting:
            return None

        if title is not None:
            meeting.title = title
        if description is not None:
            meeting.description = description
        if status is not None:
            meeting.status = status
        if end_time is not None:
            meeting.end_time = end_time
        if minutes is not None:
            meeting.minutes = minutes

        await self.db.commit()
        await self.db.refresh(meeting)
        return meeting

    async def delete_council_meeting(self, meeting_id: UUID) -> bool:
        """Soft delete a council meeting."""
        meeting = await self.get_council_meeting(meeting_id)
        if not meeting:
            return False

        meeting.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True


__all__ = ["GovernanceRepository"]
