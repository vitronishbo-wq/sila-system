from fastapi import HTTPException, status
from typing import Optional, Dict, Any, List


class TaxpayerException(HTTPException):
    """Exceção base para erros do módulo taxpayer"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str = "TAXPAYER_ERROR",
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code
        self.extra = kwargs


class NotFoundError(TaxpayerException):
    """Recurso não encontrado"""
    
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado: {resource_id}",
            code="NOT_FOUND",
            resource=resource,
            resource_id=resource_id
        )


class ValidationError(TaxpayerException):
    """Erro de validação"""
    
    def __init__(self, message: str, errors: List[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
            code="VALIDATION_ERROR",
            errors=errors or []
        )


class ConflictError(TaxpayerException):
    """Conflito de dados"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
            code="CONFLICT",
            field=field
        )


class UnauthorizedError(TaxpayerException):
    """Não autorizado"""
    
    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            code="UNAUTHORIZED",
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenError(TaxpayerException):
    """Acesso proibido"""
    
    def __init__(self, message: str = "Acesso negado"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            code="FORBIDDEN"
        )


class RateLimitError(TaxpayerException):
    """Rate limit excedido"""
    
    def __init__(self, retry_after: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas requisições. Tente novamente mais tarde.",
            code="RATE_LIMIT_EXCEEDED",
            headers={"Retry-After": str(retry_after)}
        )


class AGTIntegrationError(TaxpayerException):
    """Erro na integração com AGT"""
    
    def __init__(self, message: str, agt_error: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro na comunicação com AGT: {message}",
            code="AGT_ERROR",
            agt_error=agt_error
        )
