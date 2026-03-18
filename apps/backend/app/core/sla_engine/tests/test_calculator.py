from app.core.sla_engine.calculator import apply_context_factors
from app.core.sla_engine.models import SLAContext, Province, CitizenType, ChannelType, LoadLevel


def test_apply_context_factors_basic():
    context = SLAContext(
        province=Province.LUANDA,
        citizen_type=CitizenType.NORMAL,
        channel=ChannelType.ONLINE,
        load_level=LoadLevel.MEDIUM,
        is_holiday=False,
        business_hours=True,
    )
    calculated, breakdown, warnings = apply_context_factors(10.0, context)
    assert round(calculated, 2) == 6.4
    assert warnings == []
    assert round(breakdown["total_factor"], 2) == 0.64


def test_apply_context_factors_custom_warning():
    context = SLAContext(custom_factors={"invalid": -1})
    calculated, breakdown, warnings = apply_context_factors(5.0, context)
    assert warnings
    assert calculated > 0
