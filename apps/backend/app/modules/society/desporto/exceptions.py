class DesportoError(Exception):
    """Base exception for desporto module."""

class EntidadeNaoEncontradaError(DesportoError):
    """Raised when a domain entity is not found."""

class RegraNegocioError(DesportoError):
    """Raised when a business rule is violated."""

class IntegracaoExternaError(DesportoError):
    """Raised when an external integration fails."""