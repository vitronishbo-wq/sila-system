"""
Barramentos de Exceções Centralizadas do SILA

Todas as exceções do sistema herdam de SilaException para:
✓ Estrutura uniforme (message + code)
✓ Facilitar tratamento em middleware
✓ Evitar duplicação de lógica de erro
✓ Padrão consistente de HTTP status codes
"""

from typing import Any


class SilaException(Exception):
    """
    Exceção base para todo o sistema SILA.

    Fornece:
    - message: Mensagem legível
    - code: Código de erro máquina-legível
    - status_code: HTTP status code associado
    - details: Detalhes adicionais (opcional)

    Exemplo:
        raise SilaException(
            message="Validação falhou",
            code="VALIDATION_ERROR",
            status_code=400
        )
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Serializa exceção para resposta HTTP"""
        return {
            "error": self.code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


class NotFoundException(SilaException):
    """Recurso não encontrado (HTTP 404)"""

    def __init__(
        self, message: str = "Recurso não encontrado", details: dict[str, Any] | None = None
    ):
        super().__init__(message=message, code="NOT_FOUND", status_code=404, details=details)


class ValidationException(SilaException):
    """Validação falhou (HTTP 400)"""

    def __init__(self, message: str = "Validação falhou", details: dict[str, Any] | None = None):
        super().__init__(message=message, code="VALIDATION_ERROR", status_code=400, details=details)


class BusinessLogicException(SilaException):
    """Violação de regra de negócio (HTTP 422)"""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message=message, code="BUSINESS_RULE_VIOLATION", status_code=422, details=details
        )


class UnauthorizedException(SilaException):
    """Credenciais inválidas ou faltando (HTTP 401)"""

    def __init__(self, message: str = "Não autorizado", details: dict[str, Any] | None = None):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=401, details=details)


class ForbiddenException(SilaException):
    """Permissão insuficiente (HTTP 403)"""

    def __init__(self, message: str = "Acesso proibido", details: dict[str, Any] | None = None):
        super().__init__(message=message, code="FORBIDDEN", status_code=403, details=details)


class ConflictException(SilaException):
    """Conflito de recursos (dupla entidade, etc) (HTTP 409)"""

    def __init__(self, message: str = "Recurso em conflito", details: dict[str, Any] | None = None):
        super().__init__(message=message, code="CONFLICT", status_code=409, details=details)


class ExternalServiceException(SilaException):
    """Falha ao chamar serviço externo (HTTP 502/503)"""

    def __init__(
        self, message: str = "Serviço externo indisponível", details: dict[str, Any] | None = None
    ):
        super().__init__(
            message=message, code="EXTERNAL_SERVICE_ERROR", status_code=503, details=details
        )


class InvalidRequestError(SilaException):
    """Requisição inválida ou malformada (HTTP 400)"""

    def __init__(self, message: str = "Requisição inválida", details: dict[str, Any] | None = None):
        super().__init__(message=message, code="INVALID_REQUEST", status_code=400, details=details)


__all__ = [
    "SilaException",
    "NotFoundException",
    "ValidationException",
    "BusinessLogicException",
    "UnauthorizedException",
    "ForbiddenException",
    "ConflictException",
    "ExternalServiceException",
]
