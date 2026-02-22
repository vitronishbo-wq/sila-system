# tests/test_health_crud.py
# tests/test_health_crud.py
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from modules.health.models.health_record import HealthRecord
from modules.health.schemas import HealthCreate, HealthUpdate


@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db():
    """Fixture that provides a database session for testing."""
    async with AsyncSessionLocal() as session:
        # Begin a transaction
        await session.begin()

        try:
            yield session
            # Rollback after test
            await session.rollback()
        finally:
            await session.close()


@pytest.mark.asyncio
async def test_create_health_record(db: AsyncSession):
    """Test creating a health record."""
    health_data = HealthCreate(
        patient_id=1,
        doctor_id=2,
        diagnosis="Test diagnosis",
        notes="Test notes",
    )

    # Create a new health record
    db_health = HealthRecord(**health_data.model_dump())
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)

    assert db_health is not None
    assert db_health.patient_id == 1
    assert db_health.doctor_id == 2
    assert db_health.diagnosis == "Test diagnosis"


@pytest.mark.asyncio
async def test_get_health_record(db: AsyncSession):
    """Test retrieving a health record by ID."""
    # Create a test record
    db_health = HealthRecord(
        patient_id=1,
        doctor_id=2,
        diagnosis="Another test diagnosis",
        notes="More test notes",
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)

    # Retrieve the record
    result = await db.execute(
        select(HealthRecord).where(HealthRecord.id == db_health.id)
    )
    fetched = result.scalar_one_or_none()

    assert fetched is not None
    assert fetched.id == db_health.id
    assert fetched.diagnosis == "Another test diagnosis"


@pytest.mark.asyncio
async def test_update_health_record(db: AsyncSession):
    """Test updating a health record."""
    # Create a test record
    db_health = HealthRecord(
        patient_id=1,
        doctor_id=2,
        diagnosis="Initial diagnosis",
        notes="Initial notes",
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)

    # Update the record
    update_data = HealthUpdate(diagnosis="Updated diagnosis")
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_health, key, value)

    await db.commit()
    await db.refresh(db_health)

    # Verify the update
    result = await db.execute(
        select(HealthRecord).where(HealthRecord.id == db_health.id)
    )
    updated = result.scalar_one_or_none()

    assert updated is not None
    assert updated.id == db_health.id
    assert updated.diagnosis == "Updated diagnosis"


@pytest.mark.asyncio
async def test_get_health_by_patient(db: AsyncSession):
    """Test retrieving health records by patient ID."""
    # Create test records for the same patient
    for diagnosis in ["First condition", "Second condition"]:
        db_health = HealthRecord(
            patient_id=1,
            doctor_id=2,
            diagnosis=diagnosis,
        )
        db.add(db_health)

    await db.commit()

    # Query records by patient ID
    result = await db.execute(select(HealthRecord).where(HealthRecord.patient_id == 1))
    records = result.scalars().all()

    assert len(records) == 2
    assert all(r.patient_id == 1 for r in records)


@pytest.mark.asyncio
async def test_delete_health_record(db: AsyncSession):
    """Test deleting a health record."""
    # Create a test record
    db_health = HealthRecord(
        patient_id=1,
        doctor_id=2,
        diagnosis="To be deleted",
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)

    # Delete the record
    await db.delete(db_health)
    await db.commit()

    # Verify the record is deleted
    result = await db.execute(
        select(HealthRecord).where(HealthRecord.id == db_health.id)
    )
    fetched = result.scalar_one_or_none()

    assert fetched is None
