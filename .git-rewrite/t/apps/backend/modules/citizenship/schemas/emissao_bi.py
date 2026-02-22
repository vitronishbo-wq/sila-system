# EmissaoBi Schemas
# Sistema Integrado Local de Administração (SILA)

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class EmissaoBiCreate(BaseModel):
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None


class EmissaoBiUpdate(BaseModel):
    nome: Optional[str] = None
    nome_en: Optional[str] = None
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: Optional[bool] = None
    status: Optional[str] = None
    dados_adicionais: Optional[Dict[str, Any]] = None


class EmissaoBiRead(BaseModel):
    id: int
    nome: str
    nome_en: str
    descricao: Optional[str] = None
    descricao_en: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    status: str
    dados_adicionais: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
