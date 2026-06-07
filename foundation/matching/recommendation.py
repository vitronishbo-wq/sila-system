"""Recommendation Engine - Personalized recommendations based on matching results"""

from __future__ import annotations

from dataclasses import dataclass, field

from .engine import InstitutionProfile, MatchResult, StudentProfile, MatchingEngine


@dataclass
class RecommendationContext:
    """Context for generating recommendations"""

    student: StudentProfile
    match_results: list[MatchResult]
    institutions: list[InstitutionProfile]
    personalization_data: dict = field(default_factory=dict)


@dataclass
class PersonalizedRecommendation:
    """A personalized recommendation for a student"""

    primary_match: MatchResult
    alternative_matches: list[MatchResult]
    reasoning: str
    suggested_actions: list[str]
    timeline: str
    success_probability: float


class RecommendationEngine:
    """
    Generates personalized recommendations based on matching results.

    Provides context-aware suggestions and action plans for students.
    """

    def __init__(self, matching_engine: MatchingEngine | None = None):
        self.matching_engine = matching_engine or MatchingEngine()

    async def generate_recommendation(
        self,
        context: RecommendationContext,
    ) -> PersonalizedRecommendation | None:
        """
        Generate a personalized recommendation for the student.

        Args:
            context: Recommendation context with student and matches

        Returns:
            PersonalizedRecommendation or None if no good matches
        """
        if not context.match_results:
            return None

        primary = context.match_results[0]
        alternatives = context.match_results[1:3]

        # Generate reasoning
        reasoning = self._generate_reasoning(context.student, primary)

        # Suggested actions
        actions = self._generate_actions(context.student, primary)

        # Timeline
        timeline = self._estimate_timeline(primary)

        # Success probability
        success_prob = self._estimate_success_probability(context.student, primary)

        return PersonalizedRecommendation(
            primary_match=primary,
            alternative_matches=alternatives,
            reasoning=reasoning,
            suggested_actions=actions,
            timeline=timeline,
            success_probability=success_prob,
        )

    def _generate_reasoning(
        self, student: StudentProfile, match: MatchResult
    ) -> str:
        """Generate readable reasoning for the recommendation."""
        parts = []

        parts.append(f"A {match.institution_name} é recomendada para você:")

        if match.reasons:
            reasons_text = ", ".join(match.reasons)
            parts.append(f"Porque: {reasons_text}")

        score_text = self._score_to_text(match.match_score)
        parts.append(f"Compatibilidade: {score_text} ({match.match_score:.0f}%)")

        return " ".join(parts)

    def _generate_actions(
        self, student: StudentProfile, match: MatchResult
    ) -> list[str]:
        """Generate action items for the student."""
        actions = []

        # Priority based on match score
        if match.match_score >= 85:
            actions.append("Aplique imediatamente")
        elif match.match_score >= 70:
            actions.append("Considere aplicar em breve")
        else:
            actions.append("Explore outras opções primeiro")

        # Location-based action
        if "perto" not in " ".join(match.reasons):
            actions.append("Planeje logística de deslocamento")

        # Financial action
        if "orçamento" in " ".join(match.reasons):
            pass  # Already noted as compatible
        else:
            actions.append("Confirme compatibilidade financeira")

        # Documentation
        actions.append("Prepare documentação de candidatura")

        return actions

    def _estimate_timeline(self, match: MatchResult) -> str:
        """Estimate timeline for application and admission."""
        if match.match_score >= 90:
            return "Admissão esperada em 2-3 semanas"
        elif match.match_score >= 75:
            return "Admissão esperada em 4-6 semanas"
        elif match.match_score >= 60:
            return "Admissão esperada em 6-8 semanas"
        else:
            return "Admissão é incerta - mais informações necessárias"

    def _estimate_success_probability(
        self, student: StudentProfile, match: MatchResult
    ) -> float:
        """Estimate success probability for this match."""
        # Based on match score and compatibility
        prob = match.match_score / 100.0

        # Adjust based on previous transfer history
        if student.previous_transfers > 0:
            prob *= (1.0 - (student.previous_transfers * 0.1))

        return max(0.0, min(1.0, prob))

    def _score_to_text(self, score: float) -> str:
        """Convert numerical score to text."""
        if score >= 90:
            return "Excelente"
        elif score >= 80:
            return "Muito Boa"
        elif score >= 70:
            return "Boa"
        elif score >= 60:
            return "Regular"
        else:
            return "Baixa"
