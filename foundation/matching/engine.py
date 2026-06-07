"""Matching Engine for Educational Marketplace

Automatically recommends the best schools/courses/vacancies based on
student profile, preferences, and institutional compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .compatibility import CompatibilityCalculator
from .scorer import MatchingScorer
from .ranking import RankingOptimizer


@dataclass
class StudentProfile:
    """Student profile for matching"""

    student_id: str
    age: int
    academic_performance: float  # 0-100
    special_needs: list[str] = field(default_factory=list)
    location: dict[str, str] = field(
        default_factory=lambda: {"province": "", "municipality": "", "district": ""}
    )
    available_budget: float = 0.0
    preferred_modalities: list[str] = field(default_factory=list)
    educational_level: Optional[str] = None
    previous_transfers: int = 0


@dataclass
class InstitutionProfile:
    """Institution profile for matching"""

    institution_id: str
    name: str
    type: str
    location: dict[str, str]
    available_slots: int
    monthly_fee: float
    rating: float
    approval_rate: float
    academic_performance: float
    specializations: list[str]
    supports_special_needs: bool
    special_needs_types: list[str]
    teaching_modalities: list[str]
    transfer_acceptance_rate: float


@dataclass
class MatchResult:
    """Result of a match operation"""

    institution_id: str
    institution_name: str
    match_score: float  # 0-100
    compatibility_score: float
    ranking_position: int
    reasons: list[str] = field(default_factory=list)
    match_factors: dict[str, float] = field(default_factory=dict)
    institution: InstitutionProfile | None = None


class MatchingEngine:
    """
    Orchestrates matching logic between students and institutions.

    Uses compatibility rules and scoring algorithms to provide
    personalized recommendations.
    """

    def __init__(
        self,
        scorer: Optional[MatchingScorer] = None,
        compatibility: Optional[CompatibilityCalculator] = None,
    ):
        self.scorer = scorer or MatchingScorer()
        self.compatibility = compatibility or CompatibilityCalculator()

    async def find_matches(
        self,
        session: AsyncSession,
        student: StudentProfile,
        institutions: list[InstitutionProfile],
        max_results: int = 10,
    ) -> list[MatchResult]:
        """
        Find compatible institutions for a student.

        Args:
            session: Database session
            student: Student profile
            institutions: List of institution profiles
            max_results: Maximum number of results

        Returns:
            Sorted list of MatchResult objects
        """
        results = []

        for institution in institutions:
            # Check basic compatibility
            if not self.compatibility.is_compatible(student, institution):
                continue

            # Calculate match score
            match_score = self.scorer.calculate_match_score(student, institution)

            # Get detailed factors
            factors = self.scorer.get_match_factors(student, institution)

            # Generate explanations
            reasons = self._generate_reasons(student, institution, factors)

            result = MatchResult(
                institution_id=institution.institution_id,
                institution_name=institution.name,
                match_score=match_score,
                compatibility_score=self.compatibility.calculate_compatibility(
                    student, institution
                ),
                ranking_position=0,  # Will be set after sorting
                reasons=reasons,
                match_factors=factors,
                institution=institution,
            )
            results.append(result)

        # Sort by match score (descending) initially
        results.sort(key=lambda x: x.match_score, reverse=True)

        # Apply ranking optimizer strategies (availability first)
        try:
            optimizer = RankingOptimizer()
            results = optimizer.rank_by_availability(results)
        except Exception:
            # If ranking fails, fall back to score-sorted results
            pass

        # Update ranking positions and limit results
        for idx, result in enumerate(results[:max_results]):
            result.ranking_position = idx + 1

        return results[:max_results]

    async def check_eligibility(
        self,
        session: AsyncSession,
        student: StudentProfile,
        institution: InstitutionProfile,
    ) -> dict[str, Any]:
        """
        Check if a student is eligible for an institution.

        Args:
            session: Database session
            student: Student profile
            institution: Institution profile

        Returns:
            Eligibility details with reasons for approval/rejection
        """
        is_compatible = self.compatibility.is_compatible(student, institution)

        return {
            "eligible": is_compatible,
            "compatibility_score": self.compatibility.calculate_compatibility(
                student, institution
            ),
            "blocking_factors": self.compatibility.get_blocking_factors(
                student, institution
            ),
            "warnings": self.compatibility.get_warnings(student, institution),
            "required_actions": self.compatibility.get_required_actions(
                student, institution
            ),
        }

    def _generate_reasons(
        self,
        student: StudentProfile,
        institution: InstitutionProfile,
        factors: dict[str, float],
    ) -> list[str]:
        """Generate human-readable reasons for the match."""
        reasons = []

        # Factors are expressed on a 0-100 scale; use thresholds accordingly
        if factors.get("academic_alignment", 0) >= 80.0:
            reasons.append("academicamente compatível")

        # 'distance' factor indicates proximity (higher is better)
        if factors.get("distance", 0) >= 70.0:
            reasons.append("perto da sua localização")

        if factors.get("affordability", 0) >= 80.0:
            reasons.append("compatível com seu orçamento")

        if institution.supports_special_needs and student.special_needs:
            reasons.append("suporta suas necessidades especiais")

        if factors.get("slot_availability", 0) >= 50.0:
            reasons.append(f"{institution.available_slots} vagas disponíveis")

        if institution.rating >= 4.0:
            reasons.append(f"classificação alta ({institution.rating:.1f}/5.0)")

        if institution.approval_rate > 0.9:
            reasons.append(f"alta taxa de aprovação ({institution.approval_rate*100:.0f}%)")

        return reasons
