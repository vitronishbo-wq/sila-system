from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379")

from uuid import uuid4

from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
    InstitutionCapacityModel,
)
from foundation.persistence.educacao_repository import EducacaoRepository


class FakeModel:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid4()))
        self.__dict__.update(kwargs)


async def test_execute_transfer_commits_all_steps_in_transaction() -> None:
    repository = EducacaoRepository()

    identity = SimpleNamespace(
        id="identity-1",
        current_institution_id="school-origin",
        current_grade="5A",
    )
    active_enrollment = SimpleNamespace(
        id="enroll-1",
        institution_id="school-origin",
        status="ACTIVE",
        academic_year="2026",
        student_id="identity-1",
        transfer_destination_id=None,
        ended_at=None,
    )

    session = SimpleNamespace()
    session.add = Mock()
    session.flush = AsyncMock()
    session.execute = AsyncMock()

    @asynccontextmanager
    async def fake_transaction():
        yield session

    repository._get_identity_by_student_id = AsyncMock(return_value=identity)
    repository._get_active_enrollment = AsyncMock(return_value=active_enrollment)
    repository.reserve_capacity = AsyncMock(return_value=None)
    repository.update_academic_record_for_transfer = AsyncMock(return_value=None)
    repository._publish_outbox_event = AsyncMock(return_value=None)

    with patch(
        "foundation.persistence.educacao_repository._load_db_transaction",
        return_value=fake_transaction,
    ), patch(
        "foundation.persistence.educacao_repository._load_models",
        return_value=(None, None, FakeModel, None, FakeModel),
    ):
        transfer = await repository.execute_transfer(
            type("TR", (), {
                "student_id": "student-1",
                "target_school_id": "school-dest",
                "target_class": "7B",
                "academic_year": "2026",
                "metadata": {"reason": "Mudanca"},
            })(),
            force=True,
        )

    assert active_enrollment.status == "TRANSFERRED"
    assert active_enrollment.ended_at is not None
    assert session.add.call_count == 2

    created_enrollment = session.add.call_args_list[0][0][0]
    created_transfer = session.add.call_args_list[1][0][0]

    assert isinstance(created_enrollment, FakeModel)
    assert created_enrollment.status == "ACTIVE"
    assert created_enrollment.student_id == identity.id
    assert created_enrollment.institution_id == "school-dest"
    assert created_enrollment.transfer_origin_id == active_enrollment.id

    assert isinstance(created_transfer, FakeModel)
    assert created_transfer.to_institution_id == "school-dest"
    assert created_transfer.from_enrollment_id == active_enrollment.id
    assert created_transfer.to_enrollment_id == created_enrollment.id
    assert created_transfer.status == "executed"

    repository.reserve_capacity.assert_awaited_once_with(
        "school-dest",
        "7B",
        "2026",
        quantity=1,
        session=session,
    )

    assert repository._publish_outbox_event.await_count == 4
    event_calls = [call.args[0] for call in repository._publish_outbox_event.await_args_list]
    assert event_calls == [
        "capacity_reserved",
        "enrollment_closed",
        "enrollment_created",
        "student_transferred",
    ]


async def test_execute_transfer_generates_audit_event_inside_transaction() -> None:
    repository = EducacaoRepository()

    identity = SimpleNamespace(
        id="identity-1",
        current_institution_id="school-origin",
        current_grade="5A",
    )
    active_enrollment = SimpleNamespace(
        id="enroll-1",
        institution_id="school-origin",
        status="ACTIVE",
        academic_year="2026",
        student_id="identity-1",
        transfer_destination_id=None,
        ended_at=None,
    )

    session = SimpleNamespace()
    session.add = Mock()
    session.flush = AsyncMock()
    session.execute = AsyncMock()

    @asynccontextmanager
    async def fake_transaction():
        yield session

    audit_called = False

    async def fake_audit_event_async(*args, **kwargs):
        nonlocal audit_called
        audit_called = True
        assert kwargs.get("session") is session

    repository._get_identity_by_student_id = AsyncMock(return_value=identity)
    repository._get_active_enrollment = AsyncMock(return_value=active_enrollment)
    repository.reserve_capacity = AsyncMock(return_value=None)
    repository.update_academic_record_for_transfer = AsyncMock(return_value=None)
    repository._publish_outbox_event = AsyncMock(return_value=None)

    with patch(
        "foundation.persistence.educacao_repository._load_db_transaction",
        return_value=fake_transaction,
    ), patch(
        "foundation.persistence.educacao_repository._load_models",
        return_value=(None, None, FakeModel, None, FakeModel),
    ), patch(
        "foundation.eligibility.audit.audit_event_async",
        side_effect=fake_audit_event_async,
    ):
        await repository.execute_transfer(
            type("TR", (), {
                "student_id": "student-1",
                "target_school_id": "school-dest",
                "target_class": "7B",
                "academic_year": "2026",
                "metadata": {"reason": "Mudanca"},
            })(),
            force=True,
        )

    assert audit_called is True


async def test_reserve_capacity_updates_reserved_quantity() -> None:
    repository = EducacaoRepository()

    capacity_row = SimpleNamespace(
        capacity_total=10,
        capacity_used=5,
        capacity_reserved=2,
    )
    repository._get_capacity_row = AsyncMock(return_value=capacity_row)

    session = SimpleNamespace()
    session.add = Mock()
    session.flush = AsyncMock()

    await repository.reserve_capacity(
        "school-dest",
        "7B",
        "2026",
        quantity=1,
        session=session,
    )

    assert capacity_row.capacity_reserved == 3


async def test_get_capacity_row_prefers_all_shift() -> None:
    repository = EducacaoRepository()

    all_shift_row = SimpleNamespace(
        shift="ALL",
        capacity_total=20,
        capacity_used=5,
        capacity_reserved=2,
    )
    other_shift_row = SimpleNamespace(
        shift="MORNING",
        capacity_total=20,
        capacity_used=5,
        capacity_reserved=2,
    )

    async def fake_execute(stmt):
        class Scalars:
            def all(self):
                return [all_shift_row, other_shift_row]

            def first(self):
                return all_shift_row

        class Result:
            def scalars(self_non):
                return Scalars()

        return Result()

    session = SimpleNamespace()
    session.execute = AsyncMock(side_effect=fake_execute)

    with patch(
        "foundation.persistence.educacao_repository._load_models",
        return_value=(None, None, None, InstitutionCapacityModel, None),
    ):
        chosen = await repository._get_capacity_row(
            "school-dest",
            "7B",
            "2026",
            session=session,
        )

    assert chosen is all_shift_row


class FakeAcademicRecordModel:
    def __init__(self, academic_identity_id=None, current_class=None, history_json=None):
        self.academic_identity_id = academic_identity_id
        self.current_class = current_class
        self.history_json = history_json


async def test_update_academic_record_for_transfer_creates_record_if_missing() -> None:
    repository = EducacaoRepository()

    repository._get_academic_record = AsyncMock(return_value=None)
    session = SimpleNamespace()
    session.add = Mock()
    session.flush = AsyncMock()

    with patch(
        "foundation.persistence.educacao_repository._load_models",
        return_value=(None, FakeAcademicRecordModel, None, None, None),
    ):
        await repository.update_academic_record_for_transfer(
            uuid4(),
            target_class="7B",
            academic_year="2026",
            session=session,
        )

    assert session.add.call_count == 1
    created_record = session.add.call_args[0][0]
    assert isinstance(created_record, FakeAcademicRecordModel)
    assert created_record.current_class == "7B"
    assert created_record.history_json["transfers"][0]["academic_year"] == "2026"
