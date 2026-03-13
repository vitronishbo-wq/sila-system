from uuid import uuid4
import pytest
from apps.backend.app.modules.society.familia.domain.aggregates.family_aggregate_root import FamilyAggregate
from apps.backend.app.modules.society.familia.domain.enums import FamilyStatus, MemberRole
from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import HeadMustBeAdultError

def test_create_aggregate_with_valid_head() -> None:
    head_id = uuid4()
    aggregate = FamilyAggregate(family_id=uuid4(), head_citizen_id=head_id, code='FAM-2026-000001', head_age=30)
    assert aggregate.head_citizen_id == head_id
    assert aggregate.status == FamilyStatus.ACTIVE

def test_create_aggregate_with_minor_head_raises_error() -> None:
    with pytest.raises(HeadMustBeAdultError):
        FamilyAggregate(family_id=uuid4(), head_citizen_id=uuid4(), code='FAM-2026-000001', head_age=16)

def test_add_member_to_active_aggregate() -> None:
    aggregate = FamilyAggregate(family_id=uuid4(), head_citizen_id=uuid4(), code='FAM-2026-000001', head_age=40)
    member_id = uuid4()
    aggregate.add_member(citizen_id=member_id, role=MemberRole.MEMBER)
    assert any((member.citizen_id == member_id for member in aggregate.members))

def test_pending_events_are_cleared_after_retrieval() -> None:
    aggregate = FamilyAggregate(family_id=uuid4(), head_citizen_id=uuid4(), code='FAM-2026-000001', head_age=40)
    first = aggregate.get_pending_events()
    second = aggregate.get_pending_events()
    assert len(first) == 1
    assert second == []