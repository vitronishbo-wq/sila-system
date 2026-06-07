from typing import Optional

from pydantic import BaseModel, Field


class VerificarDocumentoRequest(BaseModel):
    tipo: str = Field(..., description="Tipo de documento (bi, passport, certificado_nascimento, ...)")
    conteudo_base64: str = Field(..., description="Conteudo do documento em base64")


class VerificarDocumentoResponse(BaseModel):
    valido: bool
    status: str
    metodo: str
    confianca_global: float
    problemas: list[str] = []


class TipoDocumentoResponse(BaseModel):
    tipo: str
    nome: str
    suportado: bool
