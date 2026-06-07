"""Base domain exception class"""

from typing import Any


class DomainException(Exception):
    """
    Base exception for all domain-level errors.

    Provides standardized error tracking and context information.
    """

    def __init__(
        self, message: str, code: str = "DOMAIN_ERROR", context: dict[str, Any] | None = None
    ):
        """
        Initialize domain exception.

        Args:
            message: Human-readable error message
            code: Machine-readable error code
            context: Additional context information
        """
        self.message = message
        self.code = code
        self.context = context or {}

        # Format full message with code
        full_message = f"[{code}] {message}"
        if self.context:
            full_message += f" | Context: {self.context}"

        super().__init__(full_message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/API responses"""
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }


__all__ = ["DomainException"]
