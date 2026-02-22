from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.governance.repository import GovernanceRepository
from modules.governance.schemas.api_schemas import (
    CouncilMeetingCreate,
    CouncilMeetingResponse,
    CouncilMeetingsListResponse,
    CouncilMeetingUpdate,
    DecisionCreate,
    DecisionResponse,
    DecisionsListResponse,
    DecisionUpdate,
    InstitutionCreate,
    InstitutionResponse,
    InstitutionsListResponse,
    InstitutionUpdate,
    MandateCreate,
    MandateResponse,
    MandatesListResponse,
    MandateUpdate,
)


class GovernanceService:
    def __init__(self, db: AsyncSession):
        self.repository = GovernanceRepository(db)
        self.db = db

    async def create_institution(
        self, payload: InstitutionCreate
    ) -> InstitutionResponse:
        inst = await self.repository.create_institution(
            name=payload.name,
            acronym=payload.acronym,
            institution_type=payload.institution_type,
            jurisdiction=payload.jurisdiction,
            description=payload.description,
            founding_date=payload.founding_date,
            website=payload.website,
            contact_info=payload.contact_info,
            leadership=payload.leadership,
            parent_institution_id=payload.parent_institution_id,
        )
        return InstitutionResponse(
            id=inst.id,
            name=inst.name,
            acronym=inst.acronym,
            institution_type=inst.institution_type,
            jurisdiction=inst.jurisdiction,
            description=inst.description,
            founding_date=inst.founding_date,
            website=inst.website,
            contact_info=inst.contact_info,
            leadership=inst.leadership,
            parent_institution_id=inst.parent_institution_id,
            created_at=inst.created_at,
            updated_at=inst.updated_at,
        )

    async def get_institution(
        self, institution_id: UUID
    ) -> Optional[InstitutionResponse]:
        inst = await self.repository.get_institution(institution_id)
        if not inst:
            return None
        return InstitutionResponse(
            id=inst.id,
            name=inst.name,
            acronym=inst.acronym,
            institution_type=inst.institution_type,
            jurisdiction=inst.jurisdiction,
            description=inst.description,
            founding_date=inst.founding_date,
            website=inst.website,
            contact_info=inst.contact_info,
            leadership=inst.leadership,
            parent_institution_id=inst.parent_institution_id,
            created_at=inst.created_at,
            updated_at=inst.updated_at,
        )

    async def list_institutions(
        self,
        institution_type: Optional[str] = None,
        parent_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> InstitutionsListResponse:
        insts = await self.repository.list_institutions(
            institution_type=institution_type,
            parent_id=parent_id,
            skip=skip,
            limit=limit,
        )
        total = await self.repository.count_institutions(
            institution_type=institution_type, parent_id=parent_id
        )
        items = [
            InstitutionResponse(
                id=i.id,
                name=i.name,
                acronym=i.acronym,
                institution_type=i.institution_type,
                jurisdiction=i.jurisdiction,
                description=i.description,
                founding_date=i.founding_date,
                website=i.website,
                contact_info=i.contact_info,
                leadership=i.leadership,
                parent_institution_id=i.parent_institution_id,
                created_at=i.created_at,
                updated_at=i.updated_at,
            )
            for i in insts
        ]
        return InstitutionsListResponse(items=items, total=total)

    async def update_institution(
        self, institution_id: UUID, payload: InstitutionUpdate
    ) -> Optional[InstitutionResponse]:
        inst = await self.repository.update_institution(
            institution_id=institution_id,
            name=payload.name,
            acronym=payload.acronym,
            institution_type=payload.institution_type,
            jurisdiction=payload.jurisdiction,
            description=payload.description,
            website=payload.website,
            contact_info=payload.contact_info,
            leadership=payload.leadership,
        )
        if not inst:
            return None
        return InstitutionResponse(
            id=inst.id,
            name=inst.name,
            acronym=inst.acronym,
            institution_type=inst.institution_type,
            jurisdiction=inst.jurisdiction,
            description=inst.description,
            founding_date=inst.founding_date,
            website=inst.website,
            contact_info=inst.contact_info,
            leadership=inst.leadership,
            parent_institution_id=inst.parent_institution_id,
            created_at=inst.created_at,
            updated_at=inst.updated_at,
        )

    async def delete_institution(self, institution_id: UUID) -> bool:
        return await self.repository.delete_institution(institution_id)

    async def create_mandate(self, payload: MandateCreate) -> MandateResponse:
        m = await self.repository.create_mandate(
            title=payload.title,
            description=payload.description,
            mandate_type=payload.mandate_type,
            issuing_authority=payload.issuing_authority,
            start_date=payload.start_date,
            end_date=payload.end_date,
            status=payload.status,
            scope=payload.scope,
            related_documents=payload.related_documents,
            institution_id=payload.institution_id,
        )
        return MandateResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            mandate_type=m.mandate_type,
            issuing_authority=m.issuing_authority,
            start_date=m.start_date,
            end_date=m.end_date,
            status=m.status,
            scope=m.scope,
            related_documents=m.related_documents,
            institution_id=m.institution_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get_mandate(self, mandate_id: UUID) -> Optional[MandateResponse]:
        m = await self.repository.get_mandate(mandate_id)
        if not m:
            return None
        return MandateResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            mandate_type=m.mandate_type,
            issuing_authority=m.issuing_authority,
            start_date=m.start_date,
            end_date=m.end_date,
            status=m.status,
            scope=m.scope,
            related_documents=m.related_documents,
            institution_id=m.institution_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def list_mandates(
        self,
        institution_id: Optional[UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> MandatesListResponse:
        mandates = await self.repository.list_mandates(
            institution_id=institution_id, status=status, skip=skip, limit=limit
        )
        total = await self.repository.count_mandates(
            institution_id=institution_id, status=status
        )
        items = [
            MandateResponse(
                id=m.id,
                title=m.title,
                description=m.description,
                mandate_type=m.mandate_type,
                issuing_authority=m.issuing_authority,
                start_date=m.start_date,
                end_date=m.end_date,
                status=m.status,
                scope=m.scope,
                related_documents=m.related_documents,
                institution_id=m.institution_id,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in mandates
        ]
        return MandatesListResponse(items=items, total=total)

    async def update_mandate(
        self, mandate_id: UUID, payload: MandateUpdate
    ) -> Optional[MandateResponse]:
        m = await self.repository.update_mandate(
            mandate_id=mandate_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            end_date=payload.end_date,
        )
        if not m:
            return None
        return MandateResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            mandate_type=m.mandate_type,
            issuing_authority=m.issuing_authority,
            start_date=m.start_date,
            end_date=m.end_date,
            status=m.status,
            scope=m.scope,
            related_documents=m.related_documents,
            institution_id=m.institution_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def delete_mandate(self, mandate_id: UUID) -> bool:
        return await self.repository.delete_mandate(mandate_id)

    async def create_decision(self, payload: DecisionCreate) -> DecisionResponse:
        d = await self.repository.create_decision(
            title=payload.title,
            description=payload.description,
            decision_type=payload.decision_type,
            status=payload.status,
            voting_record=payload.voting_record,
            meeting_id=payload.meeting_id,
            effective_date=payload.effective_date,
            expiration_date=payload.expiration_date,
            related_documents=payload.related_documents,
        )
        return DecisionResponse(
            id=d.id,
            title=d.title,
            description=d.description,
            decision_type=d.decision_type,
            status=d.status,
            voting_record=d.voting_record,
            meeting_id=d.meeting_id,
            effective_date=d.effective_date,
            expiration_date=d.expiration_date,
            related_documents=d.related_documents,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )

    async def get_decision(self, decision_id: UUID) -> Optional[DecisionResponse]:
        d = await self.repository.get_decision(decision_id)
        if not d:
            return None
        return DecisionResponse(
            id=d.id,
            title=d.title,
            description=d.description,
            decision_type=d.decision_type,
            status=d.status,
            voting_record=d.voting_record,
            meeting_id=d.meeting_id,
            effective_date=d.effective_date,
            expiration_date=d.expiration_date,
            related_documents=d.related_documents,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )

    async def list_decisions(
        self,
        meeting_id: Optional[UUID] = None,
        status: Optional[str] = None,
        decision_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> DecisionsListResponse:
        decisions = await self.repository.list_decisions(
            meeting_id=meeting_id,
            status=status,
            decision_type=decision_type,
            skip=skip,
            limit=limit,
        )
        total = await self.repository.count_decisions(
            meeting_id=meeting_id, status=status, decision_type=decision_type
        )
        items = [
            DecisionResponse(
                id=d.id,
                title=d.title,
                description=d.description,
                decision_type=d.decision_type,
                status=d.status,
                voting_record=d.voting_record,
                meeting_id=d.meeting_id,
                effective_date=d.effective_date,
                expiration_date=d.expiration_date,
                related_documents=d.related_documents,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in decisions
        ]
        return DecisionsListResponse(items=items, total=total)

    async def update_decision(
        self, decision_id: UUID, payload: DecisionUpdate
    ) -> Optional[DecisionResponse]:
        d = await self.repository.update_decision(
            decision_id=decision_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            voting_record=payload.voting_record,
        )
        if not d:
            return None
        return DecisionResponse(
            id=d.id,
            title=d.title,
            description=d.description,
            decision_type=d.decision_type,
            status=d.status,
            voting_record=d.voting_record,
            meeting_id=d.meeting_id,
            effective_date=d.effective_date,
            expiration_date=d.expiration_date,
            related_documents=d.related_documents,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )

    async def delete_decision(self, decision_id: UUID) -> bool:
        return await self.repository.delete_decision(decision_id)

    async def create_council_meeting(
        self, payload: CouncilMeetingCreate
    ) -> CouncilMeetingResponse:
        m = await self.repository.create_council_meeting(
            title=payload.title,
            description=payload.description,
            location=payload.location,
            start_time=payload.start_time,
            end_time=payload.end_time,
            status=payload.status,
            agenda=payload.agenda,
            minutes=payload.minutes,
            decisions=payload.decisions,
            participants=payload.participants,
            council_id=payload.council_id,
        )
        return CouncilMeetingResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            location=m.location,
            start_time=m.start_time,
            end_time=m.end_time,
            status=m.status,
            agenda=m.agenda,
            minutes=m.minutes,
            decisions=m.decisions,
            participants=m.participants,
            council_id=m.council_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get_council_meeting(
        self, meeting_id: UUID
    ) -> Optional[CouncilMeetingResponse]:
        m = await self.repository.get_council_meeting(meeting_id)
        if not m:
            return None
        return CouncilMeetingResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            location=m.location,
            start_time=m.start_time,
            end_time=m.end_time,
            status=m.status,
            agenda=m.agenda,
            minutes=m.minutes,
            decisions=m.decisions,
            participants=m.participants,
            council_id=m.council_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def list_council_meetings(
        self,
        council_id: Optional[UUID] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> CouncilMeetingsListResponse:
        meetings = await self.repository.list_council_meetings(
            council_id=council_id, status=status, skip=skip, limit=limit
        )
        total = await self.repository.count_council_meetings(
            council_id=council_id, status=status
        )
        items = [
            CouncilMeetingResponse(
                id=m.id,
                title=m.title,
                description=m.description,
                location=m.location,
                start_time=m.start_time,
                end_time=m.end_time,
                status=m.status,
                agenda=m.agenda,
                minutes=m.minutes,
                decisions=m.decisions,
                participants=m.participants,
                council_id=m.council_id,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in meetings
        ]
        return CouncilMeetingsListResponse(items=items, total=total)

    async def update_council_meeting(
        self, meeting_id: UUID, payload: CouncilMeetingUpdate
    ) -> Optional[CouncilMeetingResponse]:
        m = await self.repository.update_council_meeting(
            meeting_id=meeting_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            end_time=payload.end_time,
            minutes=payload.minutes,
        )
        if not m:
            return None
        return CouncilMeetingResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            location=m.location,
            start_time=m.start_time,
            end_time=m.end_time,
            status=m.status,
            agenda=m.agenda,
            minutes=m.minutes,
            decisions=m.decisions,
            participants=m.participants,
            council_id=m.council_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def delete_council_meeting(self, meeting_id: UUID) -> bool:
        return await self.repository.delete_council_meeting(meeting_id)


__all__ = ["GovernanceService"]
