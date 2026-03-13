from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.familia.application.ports.family_aggregate_repository_port import FamilyAggregateRepositoryPort
from app.modules.society.familia.domain.aggregates.family_aggregate_root import FamilyAggregate
from app.modules.society.familia.domain.entities import FamilyMember
from app.modules.society.familia.domain.enums import FamilyStatus, MemberRole
from app.modules.society.familia.infrastructure.models.family_aggregate_model import FamilyAggregateModel
from app.modules.society.familia.infrastructure.models.family_member_model import FamilyMemberModel

class SQLAlchemyFamilyAggregateRepository(FamilyAggregateRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, aggregate: FamilyAggregate) -> None:
        model = await self._session.get(FamilyAggregateModel, aggregate.id)
        if model is None:
            model = FamilyAggregateModel(id=aggregate.id, code=aggregate.code, head_citizen_id=aggregate.head_citizen_id, status=aggregate.status.value, metadata_json=aggregate.metadata, created_at=aggregate.created_at, updated_at=aggregate.updated_at)
            self._session.add(model)
        else:
            model.code = aggregate.code
            model.head_citizen_id = aggregate.head_citizen_id
            model.status = aggregate.status.value
            model.metadata_json = aggregate.metadata
            model.updated_at = aggregate.updated_at
        existing_rows = await self._session.execute(select(FamilyMemberModel).where(FamilyMemberModel.family_id == aggregate.id))
        by_citizen_id: dict[UUID, FamilyMemberModel] = {row.citizen_id: row for row in existing_rows.scalars().all()}
        for member in aggregate.all_members:
            row = by_citizen_id.get(member.citizen_id)
            if row is None:
                self._session.add(FamilyMemberModel(id=member.id, family_id=aggregate.id, citizen_id=member.citizen_id, role=member.role.value, joined_at=member.joined_at, left_at=member.left_at, metadata_json={}))
                continue
            row.role = member.role.value
            row.joined_at = member.joined_at
            row.left_at = member.left_at
        await self._session.flush()

    async def get_by_id(self, family_id: UUID) -> FamilyAggregate | None:
        model = await self._session.get(FamilyAggregateModel, family_id)
        if model is None:
            return None
        rows = await self._session.execute(select(FamilyMemberModel).where(FamilyMemberModel.family_id == family_id))
        members = [FamilyMember(id=row.id, family_id=row.family_id, citizen_id=row.citizen_id, role=MemberRole(row.role), joined_at=row.joined_at, left_at=row.left_at) for row in rows.scalars().all()]
        return FamilyAggregate.reconstitute(state={'id': model.id, 'code': model.code, 'head_citizen_id': model.head_citizen_id, 'status': FamilyStatus(model.status), 'created_at': model.created_at, 'updated_at': model.updated_at, 'metadata': model.metadata_json}, members=members)

    async def find_active_family_for_citizen(self, citizen_id: UUID, exclude_family_id: UUID | None=None) -> UUID | None:
        stmt = select(FamilyAggregateModel.id).join(FamilyMemberModel, FamilyMemberModel.family_id == FamilyAggregateModel.id).where(FamilyMemberModel.citizen_id == citizen_id, FamilyMemberModel.left_at.is_(None), FamilyAggregateModel.status == FamilyStatus.ACTIVE.value)
        if exclude_family_id is not None:
            stmt = stmt.where(FamilyAggregateModel.id != exclude_family_id)
        result = await self._session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def find_active_family_by_head(self, head_citizen_id: UUID) -> UUID | None:
        stmt = select(FamilyAggregateModel.id).where(FamilyAggregateModel.head_citizen_id == head_citizen_id, FamilyAggregateModel.status == FamilyStatus.ACTIVE.value)
        result = await self._session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def list_family_ids_for_citizen(self, citizen_id: UUID, *, limit: int=100, offset: int=0) -> list[UUID]:
        stmt = select(FamilyAggregateModel.id).join(FamilyMemberModel, FamilyMemberModel.family_id == FamilyAggregateModel.id).where(FamilyMemberModel.citizen_id == citizen_id).order_by(FamilyAggregateModel.created_at.desc()).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_next_sequence(self, year: int) -> int:
        result = await self._session.execute(select(func.count(FamilyAggregateModel.id)).where(FamilyAggregateModel.code.like(f'FAM-{year}-%')))
        return int(result.scalar_one() or 0) + 1

    async def commit(self) -> None:
        await self._session.commit()