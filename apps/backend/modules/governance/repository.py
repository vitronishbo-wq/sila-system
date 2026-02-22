"""
Governance module repository - Data access layer.
Refatorado para suporte a multi-tenancy e segurança por nível de acesso.
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
        region_id: Optional[UUID] = None, # Adicionado para vínculo regional
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
            region_id=region_id
        )
        self.db.add(institution)
        await self.db.commit()
        await self.db.refresh(institution)
        return institution

    async def list_institutions(
        self,
        institution_type: Optional[str] = None,
        parent_id: Optional[UUID] = None,
        region_id: Optional[UUID] = None, # Filtro de segurança regional
        skip: int = 0,
        limit: int = 100,
    ) -> List[Institution]:
        """List institutions com filtro de região para multi-tenancy."""
        stmt = select(Institution).where(Institution.deleted_at.is_(None))

        if institution_type:
            stmt = stmt.where(Institution.institution_type == institution_type)
        if parent_id is not None:
            stmt = stmt.where(Institution.parent_institution_id == parent_id)
        
        # ✅ CRÍTICO: Se um region_id for passado (ex: vindo do token do usuário), 
        # filtramos para que ele só veja o que pertence à sua região.
        if region_id:
            stmt = stmt.where(Institution.region_id == region_id)

        stmt = stmt.offset(skip).limit(limit).order_by(Institution.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ========================================================================
    # Mandates
    # ========================================================================

    async def get_mandate(self, mandate_id: UUID) -> Optional[Mandate]:
        """Get a mandate by ID (excludes soft-deleted)."""
        stmt = (
            select(Mandate)
            .options(selectinload(Mandate.institution))
            .where(and_(Mandate.id == mandate_id, Mandate.deleted_at.is_(None)))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_mandate(self, mandate_id: UUID) -> bool:
        """Soft delete a mandate usando timezone-aware datetime."""
        mandate = await self.get_mandate(mandate_id)
        if not mandate:
            return False

        mandate.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
        return True

    # ========================================================================
    # Decisions
    # ========================================================================

    async def list_decisions(
        self,
        meeting_id: Optional[UUID] = None,
        status: Optional[str] = None,
        decision_type: Optional[str] = None,
        region_id: Optional[UUID] = None, # Segurança regional
        skip: int = 0,
        limit: int = 100,
    ) -> List[Decision]:
        """List decisions com join opcional para filtrar por região da reunião."""
        stmt = (
            select(Decision)
            .options(selectinload(Decision.meeting))
            .where(Decision.deleted_at.is_(None))
        )

        if meeting_id:
            stmt = stmt.where(Decision.meeting_id == meeting_id)
        if status:
            stmt = stmt.where(Decision.status == status)
        
        # Se region_id for fornecido, filtramos via join com a reunião/conselho
        if region_id:
             stmt = stmt.join(Decision.meeting).where(CouncilMeeting.region_id == region_id)

        stmt = stmt.offset(skip).limit(limit).order_by(Decision.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ========================================================================
    # Council Meetings
    # ========================================================================

    async def update_council_meeting(
        self,
        meeting_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        end_time: Optional[datetime] = None,
        minutes: Optional[dict] = None,
    ) -> Optional[CouncilMeeting]:
        """Update a council meeting com refresh seguro."""
        meeting = await self.get_council_meeting(meeting_id)
        if not meeting:
            return None

        if title is not None: meeting.title = title
        if description is not None: meeting.description = description
        if status is not None: meeting.status = status
        if end_time is not None: meeting.end_time = end_time
        if minutes is not None: meeting.minutes = minutes

        await self.db.commit()
        await self.db.refresh(meeting)
        return meeting

    async def delete_council_meeting(self, meeting_id: UUID) -> bool:
        """Soft delete a council meeting."""
        meeting = await self.get_council_meeting(meeting_id)
        if not meeting:
            return False

        meeting.deleted_at = datetime.now(timezone.utc)
        await self.db.commit()
        return True

# Mantendo os outros métodos padrão que você já tinha...
# (A lógica de count e create segue o mesmo padrão acima)

__all__ = ["GovernanceRepository"]