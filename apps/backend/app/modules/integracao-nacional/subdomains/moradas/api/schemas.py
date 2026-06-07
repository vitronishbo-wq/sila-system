from typing import Optional

from pydantic import BaseModel, Field


class MoradaNormalizarRequest(BaseModel):
    endereco: str = Field(..., min_length=5, description="Endereco completo para normalizar")


class MoradaNormalizadaResponse(BaseModel):
    original: str
    linha1: str
    bairro: Optional[str] = None
    comuna: Optional[str] = None
    municipio: Optional[str] = None
    provincia: Optional[str] = None
    confidence: float = 0.0


class MoradaValidarRequest(BaseModel):
    endereco: str = Field(..., min_length=5)


class MoradaValidacaoResponse(BaseModel):
    valida: bool
    confianca: float
    problemas: list[str] = []
    sugestoes: list[str] = []
