"""Compatibility Calculator - Determines if student-institution pairs are compatible"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import InstitutionProfile, StudentProfile



class CompatibilityCalculator:
    """
    Determines compatibility between students and institutions.

    Identifies blocking factors, warnings, and required actions.
    """

    # Hard constraints that block compatibility
    BLOCKING_FACTORS = {
        "no_slots": "Instituição não tem vagas disponíveis",
        "special_needs_not_supported": "Instituição não suporta as necessidades especiais",
        "budget_exceeded": "Propina está muito acima do orçamento",
        "academic_mismatch_severe": "Desempenho acadêmico muito abaixo da instituição",
        "institution_inactive": "Instituição não está ativa no marketplace",
    }

    # Soft constraints that warn but don't block
    WARNINGS = {
        "expensive": "Propina está acima do orçamento",
        "long_distance": "Instituição fica longe da sua localização",
        "low_approval_rate": "Taxa de aprovação é baixa",
        "multiple_transfers": "Histórico de múltiplas transferências",
    }

    def is_compatible(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> bool:
        """
        Quick compatibility check (hard constraints only).

        Returns True if no blocking factors exist.
        """
        return len(self.get_blocking_factors(student, institution)) == 0

    def calculate_compatibility(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate compatibility score (0-100).

        Based on:
        - Number of blocking factors (decreases score)
        - Number of warnings (slightly decreases score)
        """
        base_score = 100.0

        blocking = len(self.get_blocking_factors(student, institution))
        warnings = len(self.get_warnings(student, institution))

        base_score -= blocking * 30.0
        base_score -= warnings * 5.0

        return max(0.0, base_score)

    def get_blocking_factors(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> list[str]:
        """
        Get list of blocking factors that prevent compatibility.

        These are hard constraints.
        """
        factors = []

        # No available slots
        if institution.available_slots == 0:
            factors.append(self.BLOCKING_FACTORS["no_slots"])

        # Special needs not supported
        if student.special_needs and not institution.supports_special_needs:
            factors.append(self.BLOCKING_FACTORS["special_needs_not_supported"])

        # Budget check (only if student has specified budget)
        if (
            student.available_budget > 0
            and institution.monthly_fee > student.available_budget * 1.5
        ):
            factors.append(self.BLOCKING_FACTORS["budget_exceeded"])

        # Academic mismatch (student performing way below institution)
        if (
            institution.academic_performance - student.academic_performance > 30
        ):
            factors.append(self.BLOCKING_FACTORS["academic_mismatch_severe"])

        return factors

    def get_warnings(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> list[str]:
        """
        Get list of warnings (soft constraints).

        These don't block but inform the student.
        """
        warnings = []

        # Budget warning (10-50% above budget)
        if student.available_budget > 0:
            if institution.monthly_fee > student.available_budget:
                excess = (institution.monthly_fee - student.available_budget)
                excess_pct = (excess / student.available_budget) * 100
                if excess_pct <= 50:
                    warnings.append(
                        f"{self.WARNINGS['expensive']} ({excess_pct:.0f}% acima)"
                    )

        # Distance warning (different province)
        if student.location.get("province") != institution.location.get("province"):
            warnings.append(self.WARNINGS["long_distance"])

        # Low approval rate warning
        if institution.approval_rate < 0.7:
            warnings.append(
                f"{self.WARNINGS['low_approval_rate']} ({institution.approval_rate*100:.0f}%)"
            )

        # Multiple transfers warning
        if student.previous_transfers >= 2:
            warnings.append(
                f"{self.WARNINGS['multiple_transfers']} ({student.previous_transfers} transferências)"
            )

        return warnings

    def get_required_actions(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> list[str]:
        """
        Get list of required actions for the student.

        Actionable items to complete the application.
        """
        actions = []

        # Academic preparation needed
        if (
            institution.academic_performance - student.academic_performance > 15
        ):
            actions.append("Considere preparação acadêmica adicional")

        # Documentation for special needs
        if student.special_needs:
            actions.append("Prepare documentação para necessidades especiais")

        # Budget planning
        if (
            student.available_budget > 0
            and institution.monthly_fee > student.available_budget
        ):
            actions.append("Planeje financiamento ou bolsas disponíveis")

        # Application timing
        if institution.available_slots <= 3:
            actions.append(
                "Aplique rapidamente - poucas vagas disponíveis"
            )

        return actions
