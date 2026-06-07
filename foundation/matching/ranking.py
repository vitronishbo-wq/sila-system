"""Ranking Module - Re-ranks and optimizes recommendation ordering"""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import MatchResult, StudentProfile


class RankingOptimizer:
    """
    Optimizes the ranking of match results.

    Applies various ranking strategies and can reorder results
    based on different criteria.
    """

    def rank_by_diversity(
        self, results: list[MatchResult]
    ) -> list[MatchResult]:
        """
        Re-rank results to maximize diversity.

        Ensures recommendations don't cluster around similar institutions.
        """
        # Simple diversity: alternate between high-quality and good-value
        ranked = []
        high_quality = [r for r in results if r.match_score >= 80]
        decent = [r for r in results if 60 <= r.match_score < 80]

        # Interleave
        for i in range(max(len(high_quality), len(decent))):
            if i < len(high_quality):
                ranked.append(high_quality[i])
            if i < len(decent):
                ranked.append(decent[i])

        return ranked

    def rank_by_distance(
        self,
        results: list[MatchResult],
        student_location: dict[str, str],
        distance_weight: float = 0.1,
    ) -> list[MatchResult]:
        """
        Re-rank results with distance as a factor.

        Boosts nearby institutions while maintaining match quality.
        """
        # This would require location data in MatchResult
        # For now, returns as-is (implementation would need model updates)
        return results

    def rank_by_availability(
        self, results: list[MatchResult]
    ) -> list[MatchResult]:
        """
        Re-rank results prioritizing those with more available slots.

        Institutions with more slots move up slightly.
        """
        # Sort by a combination of match score and slot availability.
        # If MatchResult contains `institution`, use its `available_slots`.
        def availability_key(r: MatchResult):
            slots = 0
            try:
                slots = getattr(r, "institution").available_slots if getattr(r, "institution") is not None else 0
            except Exception:
                slots = 0

            # Combine score and a stronger boost for availability (2 points per slot)
            return (r.match_score + (slots * 2.0))

        return sorted(results, key=availability_key, reverse=True)

    def apply_ranking_strategy(
        self,
        results: list[MatchResult],
        strategy: Callable[[list[MatchResult]], list[MatchResult]],
    ) -> list[MatchResult]:
        """
        Apply a custom ranking strategy to results.

        Args:
            results: List of match results
            strategy: Callable that takes and returns list of MatchResult

        Returns:
            Re-ranked results
        """
        return strategy(results)

    def add_penalty_for_repeated_failures(
        self,
        results: list[MatchResult],
        student: StudentProfile,
        penalty_per_previous_rejection: float = 0.05,
    ) -> list[MatchResult]:
        """
        Apply penalties for institutions where student has been rejected.

        (Requires historical rejection data from persistence layer)
        """
        # This would integrate with historical data
        return results

    def boost_accredited_institutions(
        self,
        results: list[MatchResult],
        boost_factor: float = 1.1,
    ) -> list[MatchResult]:
        """
        Boost ranking of accredited institutions.

        (Requires accreditation status in MatchResult)
        """
        boosted = results.copy()
        # Would boost based on accreditation status
        return boosted


class ResponseFormatter:
    """Formats matching results for API responses."""

    @staticmethod
    def format_match_result(result: MatchResult) -> dict:
        """Format a single match result for API response."""
        return {
            "institution_id": result.institution_id,
            "name": result.institution_name,
            "match_score": round(result.match_score, 2),
            "compatibility_score": round(result.compatibility_score, 2),
            "rank": result.ranking_position,
            "reasons": result.reasons,
            "factors": {
                key: round(value, 2)
                for key, value in result.match_factors.items()
            },
        }

    @staticmethod
    def format_match_results(results: list[MatchResult]) -> list[dict]:
        """Format multiple match results for API response."""
        return [ResponseFormatter.format_match_result(r) for r in results]

    @staticmethod
    def format_with_explanations(results: list[MatchResult]) -> dict:
        """Format results with detailed explanations."""
        return {
            "total": len(results),
            "matches": ResponseFormatter.format_match_results(results),
            "explanation": "Resultados ordenados por compatibilidade e qualidade",
        }
