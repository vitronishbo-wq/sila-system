from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ErrorDetail(BaseModel):
    """Detalhe de erro"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema para resposta de erro"""
    detail: str = Field(..., description="Mensagem de erro")
    code: Optional[str] = Field(None, description="Código do erro")
    errors: Optional[List[ErrorDetail]] = Field(None, description="Erros detalhados")


class ValidationErrorResponse(ErrorResponse):
    """Schema para erro de validação"""
    errors: List[ErrorDetail] = Field(..., description="Erros de validação")
