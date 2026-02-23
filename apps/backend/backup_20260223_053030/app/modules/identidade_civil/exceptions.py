"""
Exceptions Padronizadas - Módulo Identidade Civil

Todas as exceções do módulo devem herdar de HTTPException.
Nenhum raise ValueError ou return None silencioso.
"""
from fastapi import HTTPException


class NotFoundException(HTTPException):
    """Recurso não encontrado (404)."""
    
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=404, detail=detail)


class BusinessRuleException(HTTPException):
    """Violação de regra de negócio (400)."""
    
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class SovereigntyValidationException(HTTPException):
    """Falha na validação de soberania FUC (422)."""
    
    def __init__(self, detail: str = "Validação de soberania FUC falhou"):
        super().__init__(status_code=422, detail=detail)


class UnauthorizedOperationException(HTTPException):
    """Operação não autorizada (403)."""
    
    def __init__(self, detail: str = "Operação não autorizada para este perfil"):
        super().__init__(status_code=403, detail=detail)


class DuplicateResourceException(HTTPException):
    """Recurso duplicado (409)."""
    
    def __init__(self, detail: str = "Recurso já existe"):
        super().__init__(status_code=409, detail=detail)
