"""AGT Integration Exceptions"""


class AGTException(Exception):
    """Base exception for AGT errors"""
    def __init__(self, message: str, code: str = "AGT_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class AGTTimeoutError(AGTException):
    """Timeout in AGT communication"""
    def __init__(self, message: str = "Timeout in AGT communication"):
        super().__init__(message, "AGT_TIMEOUT")


class AGTAuthenticationError(AGTException):
    """Authentication error with AGT"""
    def __init__(self, message: str = "Authentication failure with AGT"):
        super().__init__(message, "AGT_AUTH_ERROR")


class AGTNotFoundError(AGTException):
    """Resource not found in AGT"""
    def __init__(self, message: str = "Resource not found in AGT"):
        super().__init__(message, "AGT_NOT_FOUND")


class AGTRateLimitError(AGTException):
    """Rate limit exceeded in AGT"""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(message, "AGT_RATE_LIMIT")


class AGTValidationError(AGTException):
    """Validation error in AGT"""
    def __init__(self, message: str, errors: list = None):
        self.errors = errors or []
        super().__init__(message, "AGT_VALIDATION_ERROR")
