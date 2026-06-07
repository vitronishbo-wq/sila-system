"""Foundation Matching Module

Provides matching and recommendation engines for the educational marketplace.

Exports:
- MatchingEngine: Core matching logic
- MatchingScorer: Scoring algorithms
- CompatibilityCalculator: Compatibility checks
- RecommendationEngine: Personalized recommendations
- RankingOptimizer: Result ranking and optimization
"""

from .compatibility import CompatibilityCalculator
from .engine import (
    InstitutionProfile,
    MatchResult,
    MatchingEngine,
    StudentProfile,
)
from .ranking import RankingOptimizer, ResponseFormatter
from .recommendation import (
    PersonalizedRecommendation,
    RecommendationContext,
    RecommendationEngine,
)
from .scorer import MatchingScorer

__all__ = [
    # Engine
    "MatchingEngine",
    "StudentProfile",
    "InstitutionProfile",
    "MatchResult",
    # Scorer
    "MatchingScorer",
    # Compatibility
    "CompatibilityCalculator",
    # Recommendation
    "RecommendationEngine",
    "RecommendationContext",
    "PersonalizedRecommendation",
    # Ranking
    "RankingOptimizer",
    "ResponseFormatter",
]
