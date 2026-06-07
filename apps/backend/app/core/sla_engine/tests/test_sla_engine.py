from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from apps.backend.app.core.sla_engine.calculator import SLACalculator
from apps.backend.app.core.sla_engine.governance import SLAGovernance, approve_version
from apps.backend.app.core.sla_engine.models import (
    Base,
    CitizenType,
    Province,
    SLABaseDB,
    SLAContext,
    SLAOverrideDB,
    SLAPolicyDB,
    SLAVersionDB,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def sample_sla_base(db_session: AsyncSession):
    sla = SLABaseDB(
        service_id="test_service",
        service_name="Servico de Teste",
        module="test",
        base_hours=24.0,
        priority="medium",
        tier="silver",
        version="1.0",
    )
    db_session.add(sla)
    await db_session.commit()
    return sla


@pytest.mark.asyncio
async def test_calculate_base_sla(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    calculator = SLACalculator(db_session)
    result = await calculator.calculate("test_service")
    assert result.service_id == "test_service"
    assert result.base_hours == 24.0
    assert result.calculated_hours == 15.36


@pytest.mark.asyncio
async def test_calculate_with_province_factor(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    calculator = SLACalculator(db_session)
    context = SLAContext(province=Province.LUANDA)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 15.36

    context = SLAContext(province=Province.CUBANGO)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 28.8


@pytest.mark.asyncio
async def test_calculate_with_citizen_type(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    calculator = SLACalculator(db_session)
    context = SLAContext(citizen_type=CitizenType.PRIORITARIO)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 7.68

    context = SLAContext(citizen_type=CitizenType.GOVERNO)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 4.61


@pytest.mark.asyncio
async def test_calculate_with_policy(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    policy = SLAPolicyDB(
        scope="global",
        scope_id="global",
        service_id="test_service",
        multiplier=1.5,
        reason="Teste",
        effective_from=datetime.utcnow() - timedelta(days=1),
    )
    db_session.add(policy)
    await db_session.commit()

    calculator = SLACalculator(db_session)
    result = await calculator.calculate("test_service")
    assert round(result.calculated_hours, 2) == 23.04
    assert len(result.applied_policies) == 1


@pytest.mark.asyncio
async def test_calculate_with_override(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    override = SLAOverrideDB(
        name="Test Override",
        description="Override de teste",
        conditions={"province": "luanda", "citizen_type": "prioritario"},
        multiplier=0.3,
        priority=10,
    )
    db_session.add(override)
    await db_session.commit()

    calculator = SLACalculator(db_session)
    context = SLAContext(province=Province.LUANDA, citizen_type=CitizenType.PRIORITARIO)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 2.3

    context = SLAContext(province=Province.HUAMBO)
    result = await calculator.calculate("test_service", context)
    assert round(result.calculated_hours, 2) == 19.2


@pytest.mark.asyncio
async def test_predict_breach(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    calculator = SLACalculator(db_session)
    prediction = await calculator.predict_breach("test_service", 10)
    assert prediction["breach_probability"] < 0.5
    assert prediction["status"] == "active"

    prediction = await calculator.predict_breach("test_service", 23)
    assert prediction["breach_probability"] > 0.8
    assert prediction["estimated_remaining"] == -7.64

    prediction = await calculator.predict_breach("test_service", 25)
    assert prediction["status"] == "breached"


@pytest.mark.asyncio
async def test_create_policy(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    governance = SLAGovernance(db_session)
    from apps.backend.app.core.sla_engine.models import SLAPolicyCreate

    policy_data = SLAPolicyCreate(
        scope="province",
        scope_id="luanda",
        service_id="test_service",
        multiplier=1.2,
        reason="Capacidade reduzida",
        effective_from=datetime.utcnow(),
    )
    policy = await governance.create_policy(policy_data, "test@user.com")
    assert policy.scope == "province"
    assert policy.scope_id == "luanda"
    assert policy.multiplier == 1.2
    assert policy.created_by == "test@user.com"


@pytest.mark.asyncio
async def test_approve_version(db_session: AsyncSession, sample_sla_base: SLABaseDB):
    version = SLAVersionDB(
        version="2.0",
        service_id="test_service",
        base_hours=48.0,
        changes=["Aumento de SLA de 24h para 48h"],
        status="draft",
    )
    db_session.add(version)
    await db_session.commit()

    approved = await approve_version(db_session, version.id, "admin@user.com")
    assert approved.status == "approved"
    assert approved.approved_by == "admin@user.com"

    result = await db_session.get(SLABaseDB, sample_sla_base.id)
    assert result.base_hours == 48.0
    assert result.version == "2.0"
