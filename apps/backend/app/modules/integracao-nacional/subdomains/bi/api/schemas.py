from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BiValidarRequest(BaseModel):
    bi_numero: str = Field(..., min_length=6, max_length=14, description="Numero do Bilhete de Identidade")


class BiVerificacaoResponse(BaseModel):
    bi_numero: str
    valido: bool
    status: str
    cidadao_encontrado: bool
    mensagem: Optional[str] = None
    verificacao_timestamp: datetime = Field(default_factory=datetime.utcnow)


class BiConsultarRequest(BaseModel):
    bi_numero: str = Field(..., min_length=6, max_length=14)


class BiConsultaResponse(BaseModel):
    bi_numero: str
    encontrado: bool
    full_name: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    filiation_pai: Optional[str] = None
    filiation_mae: Optional[str] = None
    nationality: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    emission_date: Optional[str] = None
    expiration_date: Optional[str] = None
