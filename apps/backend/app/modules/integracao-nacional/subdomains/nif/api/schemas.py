from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NifValidarRequest(BaseModel):
    nif: str = Field(..., min_length=10, max_length=10, description="Numero de Identificacao Fiscal (10 digitos)")


class NifVerificacaoResponse(BaseModel):
    nif: str
    valido: bool
    status: str
    contribuinte_encontrado: bool
    mensagem: Optional[str] = None
    verificacao_timestamp: datetime = Field(default_factory=datetime.utcnow)


class NifConsultarRequest(BaseModel):
    nif: str = Field(..., min_length=10, max_length=10)


class NifConsultaResponse(BaseModel):
    nif: str
    encontrado: bool
    full_name: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    bi_numero: Optional[str] = None
    morada: Optional[str] = None
    atividade_economica: Optional[str] = None
