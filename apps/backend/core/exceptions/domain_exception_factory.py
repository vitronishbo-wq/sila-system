"""
DomainExceptionFactory - Generate domain exception classes
Consolidates 26 domain_exception.py phantom files (P0-B)
"""


class DomainExceptionFactory:
    """Factory for creating standardized DomainException base classes"""

    @staticmethod
    def create_domain_exception() -> type[Exception]:
        """Create the unified DomainException class"""

        class DomainException(Exception):
            """
            Base exception for all domain-level errors.

            Provides standardized error tracking and context information.
            """

            def __init__(
                self, message: str, code: str = "DOMAIN_ERROR", context: dict | None = None
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

            def to_dict(self) -> dict:
                """Convert exception to dictionary for logging/API responses"""
                return {
                    "error": self.__class__.__name__,
                    "code": self.code,
                    "message": self.message,
                    "context": self.context,
                }

        return DomainException


# Singleton instance
DomainException = DomainExceptionFactory.create_domain_exception()

__all__ = ["DomainException", "DomainExceptionFactory"]
