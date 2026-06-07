from __future__ import annotations

import uuid

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

# Import adapters/engine lazily inside tests to avoid import-time circularities
# model imports are deferred into tests to avoid import-time mapper configuration


@pytest.mark.asyncio
async def test_execute_transfer_integration(db_session: AsyncSession):
    """Integration test: successful transfer using real SQLAlchemy adapters."""
    institution_id = uuid.uuid4()
    enrollment_id = uuid.uuid4()
    student_id = uuid.uuid4()

    # import models lazily
    from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
        InstitutionCapacityModel,
    )
    from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel

    # seed capacity with one available slot
    cap = InstitutionCapacityModel(
        id=uuid.uuid4(),
        institution_id=institution_id,
        grade="1",
        shift="M",
        capacity_total=1,
        capacity_used=0,
        capacity_reserved=0,
    )
    db_session.add(cap)

    # seed an active enrollment
    enr = EnrollmentModel(
        id=enrollment_id,
        student_id=student_id,
        institution_id=uuid.uuid4(),
        academic_year="2026",
        grade="1",
        status="ACTIVE",
    )
    db_session.add(enr)

    await db_session.flush()

    # ensure dependent models are imported to avoid mapper resolution errors
    import apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model

    # lazy imports to avoid circular import during test collection
    from apps.backend.app.foundation.transactional.core import TransferTransactionalEngine
    from apps.backend.app.foundation.transactional.adapters.sqlalchemy_capacity_adapter import (
        SQLAlchemyCapacityReservationAdapter,
    )
    from apps.backend.app.foundation.transactional.adapters.sqlalchemy_enrollment_adapter import (
        SQLAlchemyEnrollmentStateMachineAdapter,
    )
    # ensure mappers are configured after model imports so string relationships resolve
    from sqlalchemy.orm import configure_mappers
    configure_mappers()

    capacity_adapter = SQLAlchemyCapacityReservationAdapter(session=db_session)
    enrollment_adapter = SQLAlchemyEnrollmentStateMachineAdapter(session=db_session)

    engine = TransferTransactionalEngine(capacity=capacity_adapter, enrollment_sm=enrollment_adapter)

    payload = {
        "institution_id": institution_id,
        "grade": "1",
        "shift": "M",
        "current_enrollment_id": enrollment_id,
        "actor_id": student_id,
    }

    receipt = await engine.execute_transfer(db_session, payload, idempotency_key="test-1")

    assert receipt["status"] == "success"

    await db_session.refresh(cap)
    await db_session.refresh(enr)

    assert cap.capacity_reserved == 1
    assert enr.status == "TRANSFERRED"


@pytest.mark.asyncio
async def test_execute_transfer_no_capacity(db_session: AsyncSession):
    """Integration test: transfer fails when no capacity is available."""
    institution_id = uuid.uuid4()
    enrollment_id = uuid.uuid4()
    student_id = uuid.uuid4()

    # import models lazily
    from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
        InstitutionCapacityModel,
    )
    from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel

    # seed capacity fully used
    cap = InstitutionCapacityModel(
        id=uuid.uuid4(),
        institution_id=institution_id,
        grade="1",
        shift="M",
        capacity_total=1,
        capacity_used=1,
        capacity_reserved=0,
    )
    db_session.add(cap)

    enr = EnrollmentModel(
        id=enrollment_id,
        student_id=student_id,
        institution_id=uuid.uuid4(),
        academic_year="2026",
        grade="1",
        status="ACTIVE",
    )
    db_session.add(enr)

    await db_session.flush()

    # ensure dependent models are imported to avoid mapper resolution errors
    import apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model

    # lazy imports to avoid circular import during test collection
    from apps.backend.app.foundation.transactional.core import TransferTransactionalEngine
    from apps.backend.app.foundation.transactional.adapters.sqlalchemy_capacity_adapter import (
        SQLAlchemyCapacityReservationAdapter,
    )
    from apps.backend.app.foundation.transactional.adapters.sqlalchemy_enrollment_adapter import (
        SQLAlchemyEnrollmentStateMachineAdapter,
    )
    # ensure mappers are configured after model imports so string relationships resolve
    from sqlalchemy.orm import configure_mappers
    configure_mappers()

    capacity_adapter = SQLAlchemyCapacityReservationAdapter(session=db_session)
    enrollment_adapter = SQLAlchemyEnrollmentStateMachineAdapter(session=db_session)

    engine = TransferTransactionalEngine(capacity=capacity_adapter, enrollment_sm=enrollment_adapter)

    payload = {
        "institution_id": institution_id,
        "grade": "1",
        "shift": "M",
        "current_enrollment_id": enrollment_id,
        "actor_id": student_id,
    }

    with pytest.raises(ValueError) as exc:
        await engine.execute_transfer(db_session, payload, idempotency_key="test-2")

    assert "No capacity available" in str(exc.value)
