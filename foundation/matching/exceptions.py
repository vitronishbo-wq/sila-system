"""Exceptions for Matching Engine"""


class MatchingException(Exception):
    """Base exception for matching engine"""

    pass


class NoCompatibleInstitutionsError(MatchingException):
    """Raised when no compatible institutions found for a student"""

    pass


class InvalidStudentProfileError(MatchingException):
    """Raised when student profile is invalid"""

    pass


class InvalidInstitutionProfileError(MatchingException):
    """Raised when institution profile is invalid"""

    pass


class IneligibleForInstitutionError(MatchingException):
    """Raised when student is ineligible for institution"""

    pass


class MatchingEngineError(MatchingException):
    """Raised when matching engine fails"""

    pass
