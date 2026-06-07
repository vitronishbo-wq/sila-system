from typing import Optional

from pydantic import BaseModel, Field


class RegistoNascimentoRequest(BaseModel):
    nome_completo: str = Field(..., min_length=3)
    data_nascimento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    genero: str = Field(..., pattern=r"^[MF]$")
    naturalidade: str = Field(..., min_length=2)
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    provincia: str = Field(..., min_length=2)
    municipio: str = Field(..., min_length=2)


class RegistoNascimentoResponse(BaseModel):
    id: str
    status: str
    mensagem: str = "Nascimento registado com sucesso"


class RegistoObitoRequest(BaseModel):
    falecido_nome: str = Field(..., min_length=3)
    falecido_bi: str = Field(..., min_length=6)
    data_obito: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    causa: Optional[str] = None
    local_obito: Optional[str] = None
    provincia: str = Field(..., min_length=2)
    municipio: str = Field(..., min_length=2)


class RegistoObitoResponse(BaseModel):
    id: str
    status: str
    mensagem: str = "Obito registado com sucesso"


class ConsultaNascimentoResponse(BaseModel):
    id: str
    nome_completo: str
    data_nascimento: str
    genero: str
    naturalidade: str
    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None
    provincia: str
    municipio: str
    status: str
