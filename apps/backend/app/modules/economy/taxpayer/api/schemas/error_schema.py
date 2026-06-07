from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Detalhe de erro"""

    field: str | None = None
    message: str
    code: str | None = None


class ErrorResponse(BaseModel):
    """Schema para resposta de erro"""

    detail: str = Field(..., description="Mensagem de erro")
    code: str | None = Field(None, description="Código do erro")
    errors: list[ErrorDetail] | None = Field(None, description="Erros detalhados")


class ValidationErrorResponse(ErrorResponse):
    """Schema para erro de validação"""

    errors: list[ErrorDetail] = Field(..., description="Erros de validação")
