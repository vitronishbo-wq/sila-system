from abc import ABC, abstractmethod
from typing import Any


class EligibilityRule(ABC):
    """Base class for eligibility rules.

    A rule evaluates a request context and returns a tuple (bool, reason).
    """

    @abstractmethod
    def evaluate(self, context: dict[str, Any]) -> (bool, str):
        raise NotImplementedError()


class RuleResult:
    def __init__(self, passed: bool, reason: str = ""):
        self.passed = passed
        self.reason = reason
