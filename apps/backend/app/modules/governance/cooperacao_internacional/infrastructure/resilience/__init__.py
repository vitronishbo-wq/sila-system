from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.resilience.circuit_breaker import (
    CircuitOpenError,
    circuit_breaker,
)

__all__ = ["circuit_breaker", "CircuitOpenError"]
