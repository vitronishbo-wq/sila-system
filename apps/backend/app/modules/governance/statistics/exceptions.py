class EstatisticaError(Exception):
    """Base exception for estatistica module."""

class EstatisticaValidationError(EstatisticaError):
    """Raised when domain or request validation fails."""

class EstatisticaNotFoundError(EstatisticaError):
    """Raised when an entity is not found."""

class EstatisticaConflictError(EstatisticaError):
    """Raised on uniqueness or state conflicts."""

class EstatisticaDataSourceError(EstatisticaError):
    """Raised for upstream data source failures."""