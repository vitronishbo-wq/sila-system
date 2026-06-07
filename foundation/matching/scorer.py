"""Matching Scorer - Calculates compatibility scores"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import InstitutionProfile, StudentProfile



class MatchingScorer:
    """
    Calculates match scores between students and institutions.

    Uses a weighted scoring system considering:
    - Distance/Location
    - Academic Performance
    - Institution Capacity
    - Student History
    - Fee Compatibility
    - Special Needs Match
    - Institution Quality
    """

    # Weight configuration
    WEIGHTS = {
        "distance": 0.15,
        "academic_alignment": 0.20,
        "institution_capacity": 0.10,
        "student_history": 0.10,
        "affordability": 0.15,
        "special_needs": 0.10,
        "institution_quality": 0.15,
        "slot_availability": 0.05,
    }

    def calculate_match_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate overall match score (0-100).

        Args:
            student: Student profile
            institution: Institution profile

        Returns:
            Match score between 0 and 100
        """
        factors = self.get_match_factors(student, institution)

        # Weighted sum
        score = sum(factors.get(key, 0) * weight for key, weight in self.WEIGHTS.items())

        return min(100.0, max(0.0, score))

    def get_match_factors(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> dict[str, float]:
        """
        Get individual match factors (0-100 scale).

        Args:
            student: Student profile
            institution: Institution profile

        Returns:
            Dictionary of factor scores
        """
        return {
            "distance": self._calculate_distance_score(student, institution),
            "academic_alignment": self._calculate_academic_alignment(student, institution),
            "institution_capacity": self._calculate_capacity_score(
                student, institution
            ),
            "student_history": self._calculate_student_history_score(student),
            "affordability": self._calculate_affordability_score(student, institution),
            "special_needs": self._calculate_special_needs_score(student, institution),
            "institution_quality": self._calculate_quality_score(institution),
            "slot_availability": self._calculate_slot_availability_score(
                student, institution
            ),
        }

    def _calculate_distance_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate distance-based score.

        Closer institutions score higher.
        Same municipality: 100
        Adjacent municipality: 75
        Same province: 50
        Different province: 25
        """
        student_prov = student.location.get("province", "")
        student_mun = student.location.get("municipality", "")
        student_dist = student.location.get("district", "")

        inst_prov = institution.location.get("province", "")
        inst_mun = institution.location.get("municipality", "")

        if student_prov == inst_prov:
            if student_mun == inst_mun:
                return 100.0
            else:
                return 75.0
        else:
            return 25.0

    def _calculate_academic_alignment(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate academic alignment between student and institution.

        Compares student performance with institution's average performance.
        """
        student_perf = student.academic_performance
        inst_perf = institution.academic_performance

        # If student performance is close to institution performance: high score
        diff = abs(student_perf - inst_perf)

        # Convert difference to score (0-100)
        # Difference of 20 or more: 0 score
        # Difference of 0: 100 score
        if diff >= 20:
            return 0.0
        else:
            return 100.0 * (1.0 - (diff / 20.0))

    def _calculate_capacity_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate score based on institution capacity and occupancy.

        Full institutions: 20
        Almost full (>80%): 50
        Moderate occupancy: 75
        Plenty of space: 100
        """
        if institution.available_slots == 0:
            return 0.0

        occupancy_rate = 1.0 - (institution.available_slots / max(1, institution.available_slots + 1))

        if occupancy_rate > 0.95:
            return 0.0
        elif occupancy_rate > 0.80:
            return 50.0
        elif occupancy_rate > 0.50:
            return 75.0
        else:
            return 100.0

    def _calculate_student_history_score(self, student: StudentProfile) -> float:
        """
        Calculate score based on student's transfer history.

        Students without previous transfers: 100
        One transfer: 80
        Two transfers: 50
        Three or more transfers: 20
        """
        transfers = student.previous_transfers

        if transfers == 0:
            return 100.0
        elif transfers == 1:
            return 80.0
        elif transfers == 2:
            return 50.0
        else:
            return max(0.0, 80.0 - (transfers * 15.0))

    def _calculate_affordability_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate affordability score based on budget compatibility.

        Within budget: 100
        10-20% above budget: 75
        20-50% above budget: 50
        50%+ above budget: 0
        """
        if student.available_budget <= 0:
            return 50.0  # Unknown budget

        if institution.monthly_fee <= student.available_budget:
            return 100.0

        excess_percentage = (institution.monthly_fee - student.available_budget) / student.available_budget

        if excess_percentage <= 0.1:
            return 90.0
        elif excess_percentage <= 0.2:
            return 75.0
        elif excess_percentage <= 0.5:
            return 50.0
        else:
            return 0.0

    def _calculate_special_needs_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate special needs compatibility score.

        No special needs: 100
        Needs and institution supports: 100
        Needs but institution doesn't: 0
        """
        if not student.special_needs:
            return 100.0

        if not institution.supports_special_needs:
            return 0.0

        # Check if institution supports the specific needs
        match_count = 0
        for need in student.special_needs:
            if need in institution.special_needs_types:
                match_count += 1

        if match_count == 0:
            return 30.0  # Partial support possible

        return 100.0 * (match_count / len(student.special_needs))

    def _calculate_quality_score(self, institution: InstitutionProfile) -> float:
        """
        Calculate institution quality score.

        Based on rating, approval rate, and accreditation.
        """
        quality_score = 0.0

        # Rating component (max 40 points)
        quality_score += (institution.rating / 5.0) * 40.0

        # Approval rate component (max 30 points)
        quality_score += institution.approval_rate * 30.0

        # Transfer acceptance rate component (max 20 points)
        quality_score += institution.transfer_acceptance_rate * 20.0

        return min(100.0, quality_score)

    def _calculate_slot_availability_score(
        self, student: StudentProfile, institution: InstitutionProfile
    ) -> float:
        """
        Calculate score based on slot availability.

        No slots: 0
        Few slots (1-3): 30
        Some slots (4-10): 70
        Many slots (10+): 100
        """
        slots = institution.available_slots

        if slots == 0:
            return 0.0
        elif slots <= 3:
            return 30.0
        elif slots <= 10:
            return 70.0
        else:
            return 100.0
