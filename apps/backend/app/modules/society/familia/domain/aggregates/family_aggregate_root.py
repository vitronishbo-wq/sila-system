from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
from apps.backend.app.modules.society.familia.domain.entities import FamilyMember
from apps.backend.app.modules.society.familia.domain.enums import FamilyStatus, MemberRole
from apps.backend.app.modules.society.familia.domain.events import FamilyCreatedEvent, FamilyDissolvedEvent, FamilyHeadTransferredEvent, FamilyMemberAddedEvent, FamilyMemberRemovedEvent
from apps.backend.app.modules.society.familia.domain.rules.head_must_be_adult_rule import HeadMustBeAdultRule

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class FamilyAggregate:

    def __init__(self, *, family_id: UUID | None=None, code: str | None=None, head_citizen_id: UUID | None=None, head_age: int=18, status: FamilyStatus=FamilyStatus.ACTIVE, created_at: datetime | None=None, metadata: dict | None=None, emit_events: bool=True) -> None:
        self.id = family_id or uuid4()
        self._code = code
        self._head_citizen_id = head_citizen_id
        self._status = status
        self._created_at = created_at or _utcnow()
        self._updated_at = self._created_at
        self._metadata = metadata or {}
        self._members: list[FamilyMember] = []
        self._pending_events: list[object] = []
        if head_citizen_id:
            HeadMustBeAdultRule().validate(citizen_id=head_citizen_id, age=head_age)
            self._members.append(FamilyMember(family_id=self.id, citizen_id=head_citizen_id, role=MemberRole.HEAD, joined_at=self._created_at))
            if emit_events:
                self._pending_events.append(FamilyCreatedEvent(aggregate_id=self.id, head_citizen_id=head_citizen_id, code=code or '', occurred_at=self._created_at))

    @property
    def code(self) -> str:
        return self._code or ''

    @property
    def head_citizen_id(self) -> UUID:
        if self._head_citizen_id is None:
            raise ValueError('Aggregate sem chefe definido')
        return self._head_citizen_id

    @property
    def status(self) -> FamilyStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def metadata(self) -> dict:
        return self._metadata

    @property
    def members(self) -> list[FamilyMember]:
        return [m for m in self._members if m.left_at is None]

    @property
    def all_members(self) -> list[FamilyMember]:
        return list(self._members)

    def add_member(self, *, citizen_id: UUID, role: MemberRole, joined_at: datetime | None=None) -> None:
        if self._status != FamilyStatus.ACTIVE:
            raise ValueError('Nao e possivel adicionar membros em agregado inativo')
        if any((m.citizen_id == citizen_id and m.left_at is None for m in self._members)):
            raise ValueError(f'Cidadao {citizen_id} ja e membro deste agregado')
        self._members.append(FamilyMember(family_id=self.id, citizen_id=citizen_id, role=role, joined_at=joined_at or _utcnow()))
        self._updated_at = _utcnow()
        self._pending_events.append(FamilyMemberAddedEvent(aggregate_id=self.id, citizen_id=citizen_id, role=role, occurred_at=self._updated_at))

    def remove_member(self, *, citizen_id: UUID, reason: str | None=None) -> None:
        if self._status != FamilyStatus.ACTIVE:
            raise ValueError('Nao e possivel remover membros em agregado inativo')
        if self._head_citizen_id is None:
            raise ValueError('Aggregate sem chefe definido')
        if citizen_id == self._head_citizen_id:
            raise ValueError('Nao e possivel remover o chefe do agregado; use dissolve() ou transfer_head()')
        member = next((m for m in self._members if m.citizen_id == citizen_id and m.left_at is None), None)
        if member is None:
            raise ValueError('Membro nao encontrado ou ja inativo')
        member.left_at = _utcnow()
        self._updated_at = member.left_at
        self._pending_events.append(FamilyMemberRemovedEvent(aggregate_id=self.id, citizen_id=citizen_id, reason=reason, occurred_at=self._updated_at))

    def transfer_head(self, *, new_head_citizen_id: UUID) -> None:
        if self._status != FamilyStatus.ACTIVE:
            raise ValueError('Nao e possivel transferir chefia em agregado inativo')
        if self._head_citizen_id is None:
            raise ValueError('Aggregate sem chefe definido')
        target = next((m for m in self._members if m.citizen_id == new_head_citizen_id and m.left_at is None), None)
        if target is None:
            raise ValueError('Novo chefe deve ser membro ativo do agregado')
        if new_head_citizen_id == self._head_citizen_id:
            return
        old_head = self._head_citizen_id
        for m in self._members:
            if m.left_at is not None:
                continue
            if m.citizen_id == old_head:
                m.role = MemberRole.MEMBER
            if m.citizen_id == new_head_citizen_id:
                m.role = MemberRole.HEAD
        self._head_citizen_id = new_head_citizen_id
        self._updated_at = _utcnow()
        self._pending_events.append(FamilyHeadTransferredEvent(aggregate_id=self.id, old_head_citizen_id=old_head, new_head_citizen_id=new_head_citizen_id, occurred_at=self._updated_at))

    def dissolve(self, *, reason: str, dissolved_at: datetime | None=None) -> None:
        if self._status != FamilyStatus.ACTIVE:
            raise ValueError('Agregado nao esta ativo')
        self._status = FamilyStatus.DISSOLVED
        self._updated_at = dissolved_at or _utcnow()
        self._metadata['dissolution_reason'] = reason
        for m in self._members:
            if m.left_at is None:
                m.left_at = self._updated_at
        self._pending_events.append(FamilyDissolvedEvent(payload={'aggregate_id': str(self.id), 'head_citizen_id': str(self.head_citizen_id), 'reason': reason, 'occurred_at': self._updated_at.isoformat()}))

    def get_pending_events(self) -> list[object]:
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    @classmethod
    def reconstitute(cls, *, state: dict, members: list[FamilyMember]) -> 'FamilyAggregate':
        aggregate = cls(family_id=state['id'], code=state['code'], head_citizen_id=state['head_citizen_id'], status=state['status'], created_at=state['created_at'], metadata=state.get('metadata') or {}, emit_events=False)
        aggregate._members = list(members)
        aggregate._updated_at = state['updated_at']
        return aggregate