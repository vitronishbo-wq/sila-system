import pytest

from foundation.matching.engine import (
    StudentProfile,
    InstitutionProfile,
    MatchingEngine,
)
from foundation.matching.scorer import MatchingScorer
from foundation.matching.compatibility import CompatibilityCalculator


def make_student():
    return StudentProfile(
        student_id="s1",
        age=18,
        academic_performance=75.0,
        special_needs=[],
        location={"province": "A", "municipality": "M1", "district": "D1"},
        available_budget=200.0,
        previous_transfers=0,
    )


def make_institution(idx=1, province="A", slots=5, fee=180.0):
    return InstitutionProfile(
        institution_id=f"i{idx}",
        name=f"Inst {idx}",
        type="university",
        location={"province": province, "municipality": "M1"},
        available_slots=slots,
        monthly_fee=fee,
        rating=4.2,
        approval_rate=0.85,
        academic_performance=70.0,
        specializations=["eng"],
        supports_special_needs=False,
        special_needs_types=[],
        teaching_modalities=["presential"],
        transfer_acceptance_rate=0.8,
    )


def test_scorer_basic():
    scorer = MatchingScorer()
    student = make_student()
    inst = make_institution()

    score = scorer.calculate_match_score(student, inst)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0

    factors = scorer.get_match_factors(student, inst)
    assert "distance" in factors
    assert "affordability" in factors


def test_compatibility_blocking():
    comp = CompatibilityCalculator()
    student = make_student()
    # institution with no slots
    inst = make_institution(slots=0)
    assert not comp.is_compatible(student, inst)
    blocks = comp.get_blocking_factors(student, inst)
    assert any("vagas" in b or "vagas" in b.lower() or "vagas" in b for b in blocks) or len(blocks) > 0


@pytest.mark.asyncio
async def test_engine_find_matches():
    engine = MatchingEngine()
    student = make_student()
    institutions = [
        make_institution(idx=1, slots=2, fee=180.0),
        make_institution(idx=2, province="B", slots=10, fee=180.0),
        make_institution(idx=3, slots=0),
    ]

    # pass session as None; engine doesn't use it currently
    results = await engine.find_matches(None, student, institutions, max_results=5)
    assert isinstance(results, list)
    # Should filter out institutions with 0 slots
    assert all(r.institution_id != "i3" for r in results)

    # Ranking positions should be set
    for r in results:
        assert r.ranking_position >= 1

    # Because of availability boost, institution with more slots (i2) should be ranked first
    if len(results) >= 2:
        assert results[0].institution_id == "i2"
