"""
Exceções Centralizadas do SILA.

Importar:
    from apps.backend.app.core.exceptions import (
        SilaException,
        NotFoundException,
        BusinessLogicException,
        ...
    )

Consolidated custom exceptions for all request services.

These exceptions replace scattered HTTPException raising throughout the codebase,
providing a single source of truth for error handling patterns.

Usage:
    from apps.backend.app.core.exceptions import RequestNotFoundError

    raise RequestNotFoundError(request_id)  # Automatically converts to HTTP 404
"""

from uuid import UUID

from fastapi import HTTPException, status

from .base import (
    BusinessLogicException,
    ConflictException,
    ExternalServiceException,
    ForbiddenException,
    InvalidRequestError,
    NotFoundException,
    SilaException,
    UnauthorizedException,
    ValidationException,
)

__all__ = [
    "SilaException",
    "NotFoundException",
    "ValidationException",
    "BusinessLogicException",
    "UnauthorizedException",
    "ForbiddenException",
    "ConflictException",
    "ExternalServiceException",
    "InvalidRequestError",
]


class BaseRequestException(Exception):
    """Base exception for request service operations."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Erro interno do servidor"

    def __init__(self, message: str | None = None, **kwargs):
        if message:
            self.detail = message
        self.kwargs = kwargs
        super().__init__(self.detail)

    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException."""
        return HTTPException(status_code=self.status_code, detail=self.detail)


class RequestNotFoundError(BaseRequestException):
    """Request with given ID not found."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Pedido não encontrado"

    def __init__(self, request_id: UUID, **kwargs):
        message = f"Pedido {request_id} não encontrado"
        super().__init__(message, **kwargs)


class CitizenNotFoundError(BaseRequestException):
    """Citizen with given ID not found."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Cidadão não encontrado"

    def __init__(self, citizen_id: UUID, **kwargs):
        message = f"Cidadão {citizen_id} não encontrado"
        super().__init__(message, **kwargs)


class ResourceNotFoundError(BaseRequestException):
    """Generic resource not found error."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Recurso não encontrado"

    def __init__(self, resource_type: str, resource_id: str, **kwargs):
        message = f"{resource_type} {resource_id} não encontrado"
        super().__init__(message, **kwargs)


class AccessDeniedError(BaseRequestException):
    """User does not have access to this resource."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Acesso negado"

    def __init__(self, action: str = "acessar este recurso", **kwargs):
        message = f"Não autorizado para {action}"
        super().__init__(message, **kwargs)


class UnauthorizedError(BaseRequestException):
    """User is not authorized to perform this action."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Não autorizado"

    def __init__(self, action: str = "realizar esta ação", **kwargs):
        message = f"Não autorizado a {action}"
        super().__init__(message, **kwargs)


class InsufficientPermissionsError(BaseRequestException):
    """User has insufficient permissions."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permissões insuficientes"

    def __init__(self, permission: str = "", **kwargs):
        message = f"Permissões insuficientes para: {permission}".rstrip()
        super().__init__(message, **kwargs)


class InvalidRequestError(BaseRequestException):
    """Request data is invalid."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Dados de pedido inválidos"

    def __init__(self, field: str = "", reason: str = "", **kwargs):
        if field and reason:
            message = f"Campo '{field}' inválido: {reason}"
        elif reason:
            message = f"Pedido inválido: {reason}"
        else:
            message = "Dados de pedido inválidos"
        super().__init__(message, **kwargs)


class ValidationError(BaseRequestException):
    """Request validation failed."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Validação falhou"

    def __init__(self, message: str, **kwargs):
        super().__init__(f"Validação falhou: {message}", **kwargs)


class StatusTransitionError(BaseRequestException):
    """Invalid status transition requested."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Transição de status inválida"

    def __init__(self, current_status: str, target_status: str, **kwargs):
        message = f"Transição de {current_status} para {target_status} não permitida"
        super().__init__(message, **kwargs)


class ConflictError(BaseRequestException):
    """Request conflicts with current state."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Conflito com estado atual"

    def __init__(self, reason: str = "", **kwargs):
        message = f"Conflito: {reason}" if reason else "Conflito com estado atual"
        super().__init__(message, **kwargs)


class InvalidStateError(BaseRequestException):
    """Request is in invalid state for this operation."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Estado inválido para esta operação"

    def __init__(self, current_state: str, operation: str, **kwargs):
        message = f"Pedido em estado '{current_state}' não permite {operation}"
        super().__init__(message, **kwargs)


class AlreadyProcessedError(BaseRequestException):
    """Request has already been processed."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Pedido já foi processado"

    def __init__(self, request_id: UUID, **kwargs):
        message = f"Pedido {request_id} já foi processado"
        super().__init__(message, **kwargs)


class ServiceError(BaseRequestException):
    """Internal service error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Erro interno do serviço"

    def __init__(self, service_name: str = "", operation: str = "", **kwargs):
        if service_name and operation:
            message = f"Erro ao {operation} em {service_name}"
        else:
            message = "Erro interno do serviço"
        super().__init__(message, **kwargs)


class WorkflowError(BaseRequestException):
    """Workflow engine error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Erro no fluxo de trabalho"

    def __init__(self, workflow_id: str = "", reason: str = "", **kwargs):
        message = (
            f"Erro no fluxo {workflow_id}: {reason}" if workflow_id else f"Erro no fluxo: {reason}"
        )
        super().__init__(message, **kwargs)


class NotificationError(BaseRequestException):
    """Notification service error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Erro ao enviar notificação"

    def __init__(self, reason: str = "", **kwargs):
        message = (
            f"Erro ao enviar notificação: {reason}" if reason else "Erro ao enviar notificação"
        )
        super().__init__(message, **kwargs)


def exception_to_http(exc: Exception) -> HTTPException:
    """
    Convert any exception to HTTPException.

    If it's a BaseRequestException, converts using its rules.
    Otherwise, returns generic 500 error.

    Usage in exception handler:
        @app.exception_handler(Exception)
        async def universal_exception_handler(request, exc):
            return exception_to_http(exc).to_http_exception()
    """
    if isinstance(exc, BaseRequestException):
        return exc.to_http_exception()
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor"
    )
